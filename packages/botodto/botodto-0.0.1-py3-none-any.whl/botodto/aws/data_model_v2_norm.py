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


class HTTPInfo(BaseModel):
    method: str
    requestUri: str


class MemberInfo(BaseModel):
    shape: Optional[str]
    type: Optional[str]


class ShapeReference(BaseModel):
    shape: str


class Output(BaseModel):
    type: str


class Operation(BaseModel):
    name: str
    http: HTTPInfo
    input: ShapeReference
    output: ShapeReference
    errors: list[ShapeReference]
    documentation: str
    idempotent: Optional[bool]


class Operations(BaseModel):
    __root__: dict[str, Operation]


class v2NormalJson(BaseModel):
    version: float
    metadata: dict
    operations: Operations
    shapes: dict[str, Shape]

_norm_json = "v2-normal.json"
j_norm = ingest_json(_norm_json)
norm_model = v2NormalJson.parse_obj(j_norm)
