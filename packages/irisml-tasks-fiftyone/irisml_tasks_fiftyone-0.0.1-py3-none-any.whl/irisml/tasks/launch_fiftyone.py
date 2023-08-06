import dataclasses
import logging
import pathlib
import tempfile
import time
import typing
import torch

# fiftyone import has a side effect that replaces all current loggers with a dumb logger.
current_handlers = logging.getLogger().handlers.copy()
current_level = logging.getLogger().getEffectiveLevel()
import fiftyone  # noqa: E402
logging.getLogger().handlers = current_handlers
logging.getLogger().setLevel(current_level)
import irisml.core  # noqa: E402

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Launch a fiftyone app.

    This task will wait for the specified time, then returns an output. You can also finish the task by sending a SIGINT signal.

    Config:
        task_type (str): The type of the task. One of ``multiclass_classification``, ``multilabel_classification``, or ``object_detection``.
        duration (int): The duration of the task in seconds.
    """
    VERSION = '0.2.0'
    CACHE_ENABLED = False

    @dataclasses.dataclass
    class Inputs:
        dataset: torch.utils.data.Dataset
        predictions: typing.Optional[typing.List[torch.Tensor]] = None
        class_names: typing.Optional[typing.List[str]] = None

    @dataclasses.dataclass
    class Config:
        task_type: typing.Literal['multiclass_classification', 'multilabel_classification', 'object_detection'] = 'object_detection'
        duration: int = 180

    def execute(self, inputs):
        if inputs.predictions:
            if len(inputs.dataset) != len(inputs.predictions):
                raise RuntimeError(f"The number of samples and prediction results doesn't match: Expected: {len(inputs.dataset)} Actual: {len(inputs.predictions)}.")

        with tempfile.TemporaryDirectory() as temp_dir:
            dataset = Task.convert_to_fiftyone_dataset(inputs.dataset, inputs.predictions, inputs.class_names, self.config.task_type, pathlib.Path(temp_dir))
            session = fiftyone.launch_app(dataset)
            # session.wait()  # This method blocks forever on WSL.
            try:
                logger.info(f"Sleeping for {self.config.duration} seconds. Press Ctrl-C to finish the task now.")
                time.sleep(self.config.duration)
            except KeyboardInterrupt:
                logger.info("Received a SIGINT. Finishing the task.")
            session.close()

        return self.Outputs()

    @staticmethod
    def convert_to_fiftyone_dataset(input_dataset, predictions, class_names, task_type, directory):
        if not class_names:
            class_names = getattr(input_dataset, 'labels', [])
        dataset = fiftyone.Dataset()

        for i, (image, targets) in enumerate(input_dataset):
            image_filepath = directory / f'{i}.jpg'
            image.save(image_filepath)
            sample = fiftyone.Sample(image_filepath, ground_truth=Task._make_fo_labels(targets, task_type, class_names))
            if predictions:
                sample['prediction'] = Task._make_fo_predictions(predictions[i], task_type, class_names)
            dataset.add_sample(sample)

        return dataset

    @staticmethod
    def _make_fo_labels(targets, task_type, label_names):
        def get_name(class_id: typing.Union[int, float]):
            class_id = int(class_id)
            return label_names[class_id] if class_id < len(label_names) else f'label_{class_id}'

        if task_type == 'multiclass_classification':
            label_id = targets if isinstance(targets, int) else targets[0]
            return fiftyone.Classification(label=get_name(label_id))
        elif task_type == 'multilabel_classification':
            return fiftyone.Classifications(classifications=[fiftyone.Classification(label=get_name(i)) for i in targets])
        elif task_type == 'object_detection':
            return fiftyone.Detections(detections=[fiftyone.Detection(label=get_name(class_id), bounding_box=[x, y, x2 - x, y2 - y]) for class_id, x, y, x2, y2 in targets])
        else:
            logger.warning(f"Failed to parse {targets} as {task_type} data.")

    @staticmethod
    def _make_fo_predictions(targets, task_type, label_names):
        def get_name(class_id: typing.Union[int, float]):
            class_id = int(class_id)
            return label_names[class_id] if class_id < len(label_names) else f'label_{class_id}'

        if task_type in ['multiclass_classification', 'multilabel_classification']:
            return fiftyone.Classifications(classifications=[fiftyone.Classification(label=get_name(i), confidence=p) for i, p in enumerate(targets)])
        elif task_type == 'object_detection':
            return fiftyone.Detections(detections=[fiftyone.Detection(label=get_name(class_id), bounding_box=[x, y, x2 - x, y2 - y], confidence=score)
                                                   for class_id, score, x, y, x2, y2 in targets])
        else:
            logger.warning(f"Failed to parse {targets} as {task_type} data.")
