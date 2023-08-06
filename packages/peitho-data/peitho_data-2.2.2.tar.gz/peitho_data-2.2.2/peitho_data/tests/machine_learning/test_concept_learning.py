from unittest import TestCase

from peitho_data.machine_learning.concept_learning import find_S


class TestFindS(TestCase):
    def test_find_S_with_numeric_binary_labels(self):
        training_examples = [
            ["sunny", "warm", "normal", "strong", "warm", "same"],
            ["sunny", "warm", "high", "strong", "warm", "same"],
            ["rainy", "cold", "high", "strong", "warm", "change"],
            ["sunny", "warm", "high", "strong", "cool", "change"]
        ]
        training_labels = [1, 1, 0, 1]

        self.assertEqual(["sunny", "warm", "?", "strong", "?", "?"], find_S(training_examples, training_labels))
