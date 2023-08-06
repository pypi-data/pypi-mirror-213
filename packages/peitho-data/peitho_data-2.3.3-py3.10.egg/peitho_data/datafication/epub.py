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
from typing import List

import ebooklib
from bs4 import BeautifulSoup
from ebooklib import epub


def __epub_to_html(epub_path: str) -> list:
    """
    Reads and output contents of a specified EPUB file in HTML form

    :param epub_path:  The full path to the input file
    :return: a new list
    """
    book = epub.read_epub(epub_path)
    htmls = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            htmls.append(item.get_content())
    return htmls


def __html_to_txt(htmls) -> list:
    """
    Given a list of HTML elements encoding a EPUB file text content, extract those text contents and return them in a
    list

    :param htmls:  The provided HTML elements
    :return: a new list
    """
    txt = []
    for html in htmls:
        txt.append(BeautifulSoup(html, 'html.parser').get_text().replace('\n', ' '))
    return txt


def epub_to_txt(epub_path: str) -> List[str]:
    """
    Reads and output contents of a specified EPUB file in a list.

    :param epub_path:  The full path to the input file
    :return: a new list
    """
    return __html_to_txt(__epub_to_html(epub_path))


if __name__ == "__main__":
    pass
