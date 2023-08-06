import pathlib
import tempfile
import unittest
import PIL.Image
from irisml.tasks.launch_fiftyone import Task


class TestLaunchFiftyone(unittest.TestCase):
    def test_load_classification_dataset(self):
        fake_dataset = [(PIL.Image.new('RGB', (100, 100)), 1),
                        (PIL.Image.new('RGB', (100, 100)), 2),
                        (PIL.Image.new('RGB', (100, 100)), 3)]
        predictions = [[0, 1, 0, 0], [0, 0, 1, 0], [0, 1, 1, 1]]

        with tempfile.TemporaryDirectory() as temp_dir:
            dataset = Task.convert_to_fiftyone_dataset(fake_dataset, None, None, 'multiclass_classification', pathlib.Path(temp_dir))
            self._assert_dataset(dataset)
        with tempfile.TemporaryDirectory() as temp_dir:
            dataset = Task.convert_to_fiftyone_dataset(fake_dataset, predictions, None, 'multiclass_classification', pathlib.Path(temp_dir))
            self._assert_dataset(dataset)

    def test_load_detection_dataset(self):
        fake_dataset = [(PIL.Image.new('RGB', (100, 100)), [[0, 0.1, 0.1, 1, 1]]),
                        (PIL.Image.new('RGB', (100, 100)), []),
                        (PIL.Image.new('RGB', (100, 100)), [[0, 0.1, 0.1, 1, 1], [1, 0.2, 0.2, 0.8, 0.8]])]
        predictions = [[[0, 0.5, 0.1, 0.1, 1, 1]],
                       [[0, 0.1, 0.2, 0.2, 0.8, 0.8]],
                       []]
        with tempfile.TemporaryDirectory() as temp_dir:
            dataset = Task.convert_to_fiftyone_dataset(fake_dataset, None, None, 'object_detection', pathlib.Path(temp_dir))
            self._assert_dataset(dataset)
        with tempfile.TemporaryDirectory() as temp_dir:
            dataset = Task.convert_to_fiftyone_dataset(fake_dataset, predictions, None, 'object_detection', pathlib.Path(temp_dir))
            self._assert_dataset(dataset)

    def _assert_dataset(self, dataset):
        self.assertEqual(dataset.media_type, 'image')
        for s in dataset:
            self.assertTrue(pathlib.Path(s.filepath).exists())
