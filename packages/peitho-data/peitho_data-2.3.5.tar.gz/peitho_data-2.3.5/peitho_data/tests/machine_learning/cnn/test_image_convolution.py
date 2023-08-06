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
from unittest import TestCase

from peitho_data.machine_learning.cnn.image_convolution import image_convolution

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class TestImageConvolution(TestCase):
    def test_image_convolution(self):

        image_convolution(
            os.path.join(THIS_DIR, "convolution-test-image.png"),
            [[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]],
            os.path.join(THIS_DIR, "convolution-test-image-output.png")
        )
