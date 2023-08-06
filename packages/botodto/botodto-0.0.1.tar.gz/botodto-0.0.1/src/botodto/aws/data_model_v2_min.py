from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from pydantic import BaseModel

from ..utils.json_utils import ingest_json

class ShapeMember(BaseModel):
    __root__ = dict[str, Optional[str]]


class Shape(BaseModel):
    type: str
    required: Optional[list[str]]
    members: Optional[ShapeMember]
    pattern: Optional[str]
    member: Optional[ShapeMember]
    box: Optional[bool]
    sensitive: Optional[bool]
    min: Optional[int]
    max: Optional[int]
    documentation: Optional[str]
    enum: Optional[list[str]]


class Error(BaseModel):
    shape: str


class HTTPInfo(BaseModel):
    method: str
    requestUri: str


class MemberInfo(BaseModel):
    shape: Optional[str]
    type: Optional[str]


class Input(BaseModel):
    type: str
    required: Optional[list[str]]
    members: Optional[dict[str, Optional[MemberInfo]]]


class Output(BaseModel):
    type: str


class Operation(BaseModel):
    input: Optional[Input]
    output: Optional[Output]
    idempotent: Optional[bool]
    endpoint: Optional[dict[str, str]]


class Operations(BaseModel):
    __root__: dict[str, Operation]


class v2MinJson(BaseModel):
    version: float
    metadata: dict
    operations: Operations
    shapes: dict[str, Shape]


_min_json = "v2-min.json"
j_min = ingest_json(_min_json)
min_model = v2MinJson.parse_obj(j_min)
