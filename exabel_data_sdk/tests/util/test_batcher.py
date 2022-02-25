import unittest

from exabel_data_sdk.util.batcher import batcher


class TestBatcher(unittest.TestCase):
    def test_batcher(self):
        expected = [
            (0, 1, 2),
            (3, 4, 5),
        ]
        result = list(batcher(range(6), 3))
        self.assertListEqual(expected, result)

    def test_batcher_indivisible_batch(self):
        expected = [
            (0, 1, 2),
            (3,),
        ]
        result = list(batcher(range(4), 3))
        self.assertListEqual(expected, result)
