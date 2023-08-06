import json

from .path_utils import data_dir

__all__ = ["ingest_json"]


def ingest_json(filename):
    path = data_dir / filename
    return json.loads(path.read_text())
