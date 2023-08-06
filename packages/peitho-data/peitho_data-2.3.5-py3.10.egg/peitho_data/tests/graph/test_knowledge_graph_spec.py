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

from peitho_data.graph.knowledge_graph_spec import _camel_case
from peitho_data.graph.knowledge_graph_spec import convert_spec_to_cypher_from_file

DATA_FILE = "convert-spec-to-cypher-test-data.json"


class TestFileBasedVisualization(TestCase):

    def test_specs_are_converted_to_correct_cypher(self):
        actual = convert_spec_to_cypher_from_file(
            os.path.join(os.path.dirname(__file__), DATA_FILE)
        )
        with open(os.path.join(os.path.dirname(__file__), "convert-spec-to-cypher-expected.cql")) as cql_file:
            expected = cql_file.read()
            self.assertEqual(expected, "".join(actual))

    def test_convert_spec_to_cypher_is_stateless(self):
        convert_spec_to_cypher_from_file(
            os.path.join(os.path.dirname(__file__), DATA_FILE)
        )
        actual = convert_spec_to_cypher_from_file(
            os.path.join(os.path.dirname(__file__), DATA_FILE)
        )
        with open(os.path.join(os.path.dirname(__file__), "convert-spec-to-cypher-expected.cql")) as cql_file:
            expected = cql_file.read()
            self.assertEqual(expected, "".join(actual))

    def test__camel_case(self):
        input_to_expected_output = [
            ("JavaScript", "javascript"),
            ("Foo-Bar", "fooBar"),
            ("foo_bar", "fooBar"),
            ("--foo.bar", "foo.Bar"),
            ("Foo-BAR", "fooBar"),
            ("fooBAR", "foobar"),
            ("foo bar", "fooBar")
        ]

        for input, expected in input_to_expected_output:
            self.assertEqual(expected, _camel_case(input))
