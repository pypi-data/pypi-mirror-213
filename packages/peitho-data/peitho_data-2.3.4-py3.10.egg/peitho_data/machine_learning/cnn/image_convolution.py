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
import cv2
import numpy as np


def _process_image(image: str):
    """
    Pre-process an image by converting it to grayscale.

    In order to get the best results with the following 2D convolution, image should be processed in grayscale

    :param image:  The absolute/relative path of the image to pre-processed

    :return: the processed graysacle image instance
    """
    return cv2.cvtColor(src=cv2.imread(image), code=cv2.COLOR_BGR2GRAY)


def _convolve_2d(image, kernel, padding=0, strides=1):
    kernel = np.flipud(np.fliplr(kernel))  # cross correlation

    # Gather Shapes of Kernel + Image + Padding
    x_kern_shape = kernel.shape[0]
    y_kern_shape = kernel.shape[1]
    x_img_shape = image.shape[0]
    y_img_shape = image.shape[1]

    # Shape of Output Convolution
    x_output = int(((x_img_shape - x_kern_shape + 2 * padding) / strides) + 1)
    y_output = int(((y_img_shape - y_kern_shape + 2 * padding) / strides) + 1)
    output = np.zeros((x_output, y_output))

    # Apply Equal Padding to All Sides
    if padding != 0:
        image_padded = np.zeros((image.shape[0] + padding * 2, image.shape[1] + padding * 2))
        image_padded[int(padding):int(-1 * padding), int(padding):int(-1 * padding)] = image
        print(image_padded)
    else:
        image_padded = image

    # Iterate through image
    for y in range(image.shape[1]):
        # Exit Convolution
        if y > image.shape[1] - y_kern_shape:
            break
        # Only Convolve if y has gone down by the specified Strides
        if y % strides == 0:
            for x in range(image.shape[0]):
                # Go to next row once kernel is out of bounds
                if x > image.shape[0] - x_kern_shape:
                    break
                try:
                    # Only Convolve if x has moved by the specified Strides
                    if x % strides == 0:
                        output[x, y] = (kernel * image_padded[x: x + x_kern_shape, y: y + y_kern_shape]).sum()
                except:  # noqa: E722
                    break

    return output


def image_convolution(input_image_path: str, kernel: list[list[int]], output_image_path: str):
    """
    Convolutes a specified image with the provided kernel.

    For example, the following image

    .. image:: https://github.com/QubitPi/peitho-data/blob/master/peitho_data/tests/machine_learning/cnn/convolution-test-image.png?raw=true

    is convoluted to

    .. image:: https://github.com/QubitPi/peitho-data/blob/master/peitho_data/tests/machine_learning/cnn/convolution-test-image-output.png?raw=true

    Example usage::

        image_convolution('input.png', [[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]], "output.png")

    - the default padding around the image is 0
    - the stride is 1

    The method will apply `cross correlation <https://en.wikipedia.org/wiki/Convolution>`_ to the specified
    kernel using NumPy by flipping the kernel matrix horizontally then vertically.

    .. NOTE:: Why do we apply "cross correlation" instead of "convolution" here?

       Some features of convolution are similar to `cross correlation <https://en.wikipedia.org/wiki/Convolution>`_: for
       real-valued functions, of a continuous or discrete variable, convolution differs from cross-correlation only in
       that either :math:`f(x)` or :math:`g(x)` is reflected about the y-axis in convolution but NOT in
       cross-correlation; thus **convolution is a cross-correlation of** :math:`g(-x)` **and** :math:`f(x)`**, or**
       :math:`f(-x)` **and** :math:`g(x)`.

       .. image:: ../img/comparison-convolution-correlation.png
         :align: center

       If we look at the example in :ref:`the-convolution-step`, we will notice that there is no flip of the kernel
       :math:`g` like we did for the :ref:`discrete-convolution-example`. This is a matter of notation.
       :ref:`the-convolution-step` should be called cross-correlation, it is not a true convolution. However,
       computationally this difference does not affect the performance of the algorithm because the kernel is being
       trained such that its weights are best suited for the operation, thus adding the flip operation would simply make
       the algorithm learn the weights in different cells of the kernel to accommodate the flip. So we can omit the flip
       (`reference: Convolution and Cross Correlation in CNN <https://datascience.stackexchange.com/a/40545>`_)

    :param input_image_path:  The absolute/relative path to the image to be convoluted
    :param kernel:  A 2D integer matrix specifying the convolution kernel
    :param output_image_path:  The absolute/relative path to the convoluted image
    """  # noqa: E501
    cv2.imwrite(output_image_path, _convolve_2d(_process_image(input_image_path), np.array(kernel), padding=2))
