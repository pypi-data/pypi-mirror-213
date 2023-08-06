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
import os
import pathlib as pl
from unittest import TestCase

from peitho_data import word_cloud


class TestWordCloud(TestCase):
    def test_create_word_cloud_image(self):
        word_cloud.create_word_cloud_image(
            open("peitho_data/tests/pride-and-prejudice.txt", "r").read(),
            "peitho_data/tests/actual_word_cloud.png",
            "peitho_data/tests/alice_mask.png",
        )
        if not pl.Path("peitho_data/tests/actual_word_cloud.png").resolve().is_file():
            raise AssertionError(
                "File does not exist: %s"
                % str("peitho_data/tests/actual_word_cloud.png")
            )
        os.remove("peitho_data/tests/actual_word_cloud.png")
