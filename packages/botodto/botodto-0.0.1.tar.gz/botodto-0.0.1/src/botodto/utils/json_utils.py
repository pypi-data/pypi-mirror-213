import json


def ingest(filename):
    path = data_dir / filename
    return json.loads(path.read_text())
