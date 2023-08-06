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

def find_S(training_instances: list[list[str]], training_labels: list[int]) -> list[str]:
    """
    Implements the Find-S Algorithm for finding the most specific hypothesis based on a given set of training
    instances and labels.

    For example, given the following training dataset,

    ========= ======== ============ ========== ========= ============ =============
     Sky       Temp     Humidity     Wind       Water     Forecast     EnjoySport
    ========= ======== ============ ========== ========= ============ =============
     Sunny     Warm     Normal       Strong     Warm      Same         Yes
     Sunny     Warm     High         Strong     Warm      Same         Yes
     Rainy     Cold     High         Strong     Warm      Change       No
     Sunny     Warm     High         Strong     Cool      Change       Yes
    ========= ======== ============ ========== ========= ============ =============

    The training instances are passed in as::

        [
            ["sunny", "warm", "normal", "strong", "warm", "same"],
            ["sunny", "warm", "high", "strong", "warm", "same"],
            ["rainy", "cold", "high", "strong", "warm", "change"],
            ["sunny", "warm", "high", "strong", "cool", "change"]
        ]

    The training labels are passed in as::

        [1, 1, 0, 1]

    :param training_instances:  A list of training samples
    :param training_labels:  A list of positive and negative labels

    :return: a maximally specific hypothesis based on the training dataset
    """
    hypothesis = [""] * len(training_instances[0])

    for idx, label in enumerate(training_labels):
        if label == 1:
            positive_example = training_instances[idx]
            for i, attribute in enumerate(positive_example):
                if hypothesis[i] == "" or hypothesis[i] == positive_example[i]:
                    hypothesis[i] = positive_example[i]
                else:
                    hypothesis[i] = "?"

    return hypothesis
