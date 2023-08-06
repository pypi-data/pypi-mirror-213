import os
from unittest import TestCase

import matplotlib.pyplot as plt

from peitho_data.graph.visualization.file_based_visualization import visualize_using_networkx


class TestFileBasedVisualization(TestCase):

    def test_visualize_using_networkx_throws_no_error(self):
        data_file_path = os.path.join(os.path.dirname(__file__), "test-data.json")
        plt.ion()  # https://stackoverflow.com/a/11141305/14312712
        visualize_using_networkx(data_file_path)
        plt.close()
