import json
import re

"How to parse json"


def parse_json(string):
    return json.loads(string)


"How to construct json"


def construct_json(dict):
    return json.dumps(dict)


"""
Construct point from (lon, lat) coordinates
Ex. (1.0, 2.0) -> '{"lon":1.0,"lat":2.0}'
"""


def construct_coordinates(lon, lat):
    return json.dumps({
        "lon": lon,
        "lat": lat
    })


"""
Construct names started from capital letter
Ex. ["Paul", "mari", "Jerard"] -> '{"names":["Paul", "Jerard"]}'
"""


def construct_names(names):
    return None


"""
Group words by first letter
Ex.
["alpha", "omega", "accordeon"]
    ->
'{
    "a": ["alpha", "accordeon"],
    "o": ["omega"]
}'
"""


def group_strings(words):
    return None


"""
Extract all names, longer than 5 character
Ex.
{
    "names": [
        "Tom",
        "Rik",
        "Albert",
        "Camille"
    ]
}
    ->
["Albert", "Camille"]
"""


def extract_long_names(resp):
    return None


"""
Count words in a text
Ex.
"Hakuna Matata! What a wonderful phrase
Hakuna Matata! Ain't no passing craze
"
    ->
{
    'matata': 2,
    'a': 1,
    'what': 1,
    'wonderful': 1,
    'hakuna': 2,
    'no': 1,
    "ain't": 1,
    'phrase': 1,
    'passing': 1,
    'craze': 1
}
"""

def count_words(text):
    return None
