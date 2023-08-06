from pprint import pprint

from ..utils.path_utils import data_dir
from ..utils.json_utils import ingest_json

_min_json = "v2-min.json"
_norm_json = "v2-normal.json"
_smithy_json = "v3-smithy.json"

j_min = ingest_json(_min_json)
j_norm = ingest_json(_norm_json)
j_smithy = ingest_json(_smithy_json)


def strip_char(string, char):
    index = string.find(char)
    if index != -1:
        return string[index + 1 :]
    else:
        return string


def list_keys(json, trim_hash=False, pp=False):
    if trim_hash:
        json = [strip_char(j, "#") for j in json]
    if pp:
        pprint(list(json))
    else:
        return list(json)


def get_input(json):
    pprint(json["input"])


def get_output(json):
    pprint(json["output"])


norm_keys = list_keys(j_norm)
min_keys = list_keys(j_min)
smithy_keys = list_keys(j_smithy, trim_hash=True)
