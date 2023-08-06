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
from re import sub
from string import Template

DELETE_ALL_NODES_AND_LINKS = "MATCH (n) DETACH DELETE n;"

PROPERTY_TEMPLATE = '    $key: "$value"'

CREATE_NODE_TEMPLATE = """
CREATE ($id:Concept {
$properties
});
"""

CREATE_LILNK_TEMPLATE = """
MATCH (source:Concept), (target:Concept)
WHERE source.id = "$source_id" AND target.id = "$target_id"
CREATE (source)-[r:`$link_label`]->(target) RETURN type(r);
"""


def convert_spec_to_cypher(spec_json) -> list[str]:
    """
    Converts a knowledge graph spec to an equivalent set of Cypher queries, which produces the same graph defined in the
    spec.

    The knowledge graph spec is defined in https://qubitpi.github.io/knowledge-graph-spec/draft/. Note that this spec
    requires all link's "fields" have an attribute called "label". For example::

    {
        "nodes": [
            {
                "id": "team",
                "fields": {
                    "name": "Team Composition"
                }
            },
            {
                "id": "roles",
                "fields": {
                    "name": "Role"
                }
            }
        ],
        "links": [
            {
                "source": "team",
                "target": "roles",
                "fields": {
                    "label": "starts with"
                }
            }
        ]
    }

    is converted to::

    MATCH (n) DETACH DELETE n;
    CREATE (team:Concept {name: "Team Composition"});
    CREATE (roles:Concept {name: "Role"});
    MATCH (source:Concept), (target:Concept) WHERE source.name = "Team Composition" AND target.name = "Role"
        CREATE (source)-[r:`starts with`]->(target) RETURN type(r);

    :param spec_json: The Knowledge Graph Spec whose data structure is defined in
    https://qubitpi.github.io/knowledge-graph-spec/draft/#sec-Data-Structure

    :return: a list of Cypher queries prepended with a resetting query "MATCH (n) DETACH DELETE n;" that runs betfore
    all generated queries
    """
    cypher_queries = [DELETE_ALL_NODES_AND_LINKS, "\n"]

    for node in spec_json["nodes"]:
        cypher_queries.append(
            Template(CREATE_NODE_TEMPLATE).substitute(
                id=_camel_case(node["id"]),
                properties=',\n'.join(
                    [Template(PROPERTY_TEMPLATE).substitute(key="id", value=node["id"])] +
                    [Template(PROPERTY_TEMPLATE).substitute(key=k, value=v) for k, v in node["fields"].items()]

                )
            )
        )

    for link in spec_json["links"]:
        cypher_queries.append(
            Template(CREATE_LILNK_TEMPLATE).substitute(
                source_id=link["source"],
                target_id=link["target"],
                link_label=link["fields"]["label"]
            )
        )

    return cypher_queries


def convert_spec_to_cypher_from_file(spec_path: str) -> list[str]:
    """
    Converts a knowledge graph spec to an equivalent set of Cypher queries, which produces the same graph defined in the
    spec.

    The knowledge graph spec is defined in https://qubitpi.github.io/knowledge-graph-spec/draft/. Note that this spec
    requires all link's "fields" have an attribute called "label". For example::

    {
        "nodes": [
            {
                "id": "team",
                "fields": {
                    "name": "Team Composition"
                }
            },
            {
                "id": "roles",
                "fields": {
                    "name": "Role"
                }
            }
        ],
        "links": [
            {
                "source": "team",
                "target": "roles",
                "fields": {
                    "label": "starts with"
                }
            }
        ]
    }

    is converted to::

    MATCH (n) DETACH DELETE n;
    CREATE (team:Concept {name: "Team Composition"});
    CREATE (roles:Concept {name: "Role"});
    MATCH (source:Concept), (target:Concept) WHERE source.name = "Team Composition" AND target.name = "Role"
        CREATE (source)-[r:`starts with`]->(target) RETURN type(r);

    :return: a list of Cypher queries prepended with a resetting query "MATCH (n) DETACH DELETE n;" that runs betfore
    all generated queries

    :param spec_path: The relative/absolute path to the Knowledge Graph Spec JSON file

    :return: a list of Cypher queries prepended with a resetting query "MATCH (n) DETACH DELETE n;" that runs betfore
    all generated queries
    """
    with open(spec_path) as data_file:
        return convert_spec_to_cypher(json.load(data_file))


def _camel_case(string: str) -> str:
    """
    Converts a given string to Camelcase.

    This method should be used exclusively by Cypher related logic because Cypher is stupid enough to restrict ID to
    be either number of camel case, not even hyphened phrases like "person-tom"

    For example:

    - "JavaScript" is converted to "javascript"
    - "Foo-Bar" is converted to "fooBar"
    - "foo_bar" is converted to "fooBar"
    - "--foo.bar" is converted to "foo.Bar"
    - "Foo-BAR" is converted to "fooBar"
    - "fooBAR" is converted to "foobar"
    - "foo bar" is converted to "fooBar"

    :param string:  The string to convert

    :return: the same string in camel case format
    """

    # https://www.w3resource.com/python-exercises/string/python-data-type-string-exercise-96.php
    string = sub(r"(_|-)+", " ", string).title().replace(" ", "")
    return ''.join([string[0].lower(), string[1:]])


if __name__ == "__main__":
    pass
