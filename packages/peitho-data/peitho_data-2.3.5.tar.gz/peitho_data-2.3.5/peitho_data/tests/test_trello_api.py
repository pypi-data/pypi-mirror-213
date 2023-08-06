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
import json
import re
from unittest import TestCase

import requests
import requests_mock

from peitho_data import trello_api

GET_ATTACHMENTS_URL_REGEX_PATTERN = "api.trello.com/1/cards/.*/attachments\\?key=.*&token=.*"
DELETE_ATTACHMENT_URL_REGEX_PATTERN = "api.trello.com/1/cards/.*/attachments/.*\\?key=.*&token=.*"
POST_ATTACHMENT_URL_REGEX_PATTERN = "api.trello.com/1/cards/.*/attachments"

requests_mock.mock.case_sensitive = True
adapter = requests_mock.Adapter()
session = requests.Session()
session.mount('https://', adapter)


class TestTrelloApi(TestCase):

    def test_delete_attachment_by_name(self):
        card_id = "123"
        name = "Deprecation Extension Notice"

        with requests_mock.Mocker() as mock:
            mock.get(
                re.compile(GET_ATTACHMENTS_URL_REGEX_PATTERN),
                json=json.load(open("peitho_data/tests/get-card-attachments-response.json"))
            )

            mock.delete(re.compile(DELETE_ATTACHMENT_URL_REGEX_PATTERN), status_code=200)

            trello_api.delete_attachment_by_name(card_id, name)

    def test_delete_all_attachments(self):
        card_id = "123"

        with requests_mock.Mocker() as mock:
            mock.get(
                re.compile(GET_ATTACHMENTS_URL_REGEX_PATTERN),
                json=json.load(open("peitho_data/tests/get-card-attachments-response.json"))
            )

            mock.delete(re.compile(DELETE_ATTACHMENT_URL_REGEX_PATTERN), status_code=200)

            trello_api.delete_all_attachments(card_id)

    def test_upload_attachment(self):
        with requests_mock.Mocker() as mock:
            mock.post(re.compile(POST_ATTACHMENT_URL_REGEX_PATTERN), status_code=200)

            response = trello_api.upload_attachment(
                "123",
                "book.pdf",
                "peitho_data/tests/get-card-attachments-response.json"
            )

            assert response.status_code == 200
