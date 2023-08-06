# Copyright Jiaqi Liu
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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
