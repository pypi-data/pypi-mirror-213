import os
from unittest import TestCase

from peitho_data.datafication.epub import epub_to_txt


class TestEpub(TestCase):

    def test_get_resistance_info(self):
        assert "Test Content" in epub_to_txt(epub_path=os.path.join(os.path.dirname(__file__), "test-book.epub"))[1]
