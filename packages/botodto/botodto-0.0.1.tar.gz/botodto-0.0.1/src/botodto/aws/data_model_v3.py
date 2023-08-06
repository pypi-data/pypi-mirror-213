from __future__ import annotations

import json
from enum import Enum
from functools import partial
from pathlib import Path
from pprint import pprint as _pprint
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

from ..utils.json_utils import ingest_json

pprint = partial(_pprint, sort_dicts=False)


class ShapeMember(BaseModel):
    __root__ = dict[str, Optional[str]]


class Pagination(BaseModel):
    inputToken: str
    outputToken: str
    items: str
    pageSize: str


class Range(BaseModel):
    min: Optional[int]
    max: Optional[int]


class Endpoint(BaseModel):
    hostPrefix: str


class AwsApiService(BaseModel):
    sdkId: str
    arnNamespace: str
    cloudFormationName: str
    cloudTrailEventSource: str
    endpointPrefix: str


class SigV4(BaseModel):
    name: str


class XmlNamespace(BaseModel):
    uri: str


class ServiceTrait(BaseModel):
    service: AwsApiService = Field(..., alias="aws.api#service")
    sigv4: SigV4 = Field(..., alias="aws.auth#sigv4")
    awsJson: dict = Field(..., alias="aws.protocols#awsJson1_0")
    # documentation: str = Field(..., alias="smithy.api#documentation")
    title: str = Field(..., alias="smithy.api#title")
    xmlNamespace: XmlNamespace = Field(..., alias="smithy.api#xmlNamespace")
    # endpointRuleSet: dict = Field(alias="smithy.rules#endpointRuleSet")


class Trait(BaseModel):
    pattern: Optional[str] = Field(alias="aws.api#pattern")
    range: Optional[Range] = Field(alias="aws.api#range")
    idempotent: Optional[dict] = Field(alias="aws.api#idempotent")
    sensitive: Optional[dict] = Field(alias="aws.api#sensitive")
    default: Optional[bool] = Field(alias="aws.api#default")
    httpError: Optional[int] = Field(alias="aws.api#httpError")
    length: Optional[Range] = Field(alias="aws.api#length")
    paginated: Optional[Pagination] = Field(alias="aws.api#paginated")
    error: Optional[str] = Field(alias="aws.api#error")
    endpoint: Optional[Endpoint] = Field(alias="aws.api#endpoint")


class TargetReference(BaseModel):
    target: str


class ServiceShape(BaseModel):
    type: Literal["service"]
    version: str
    operations: list[TargetReference]
    traits: ServiceTrait


class ShapeType(Enum):
    BOOLEAN = "boolean"
    ENUM = "enum"
    FLOAT = "float"
    INTEGER = "integer"
    LIST = "list"
    LONG = "long"
    OPERATION = "operation"
    STRING = "string"
    STRUCTURE = "structure"
    TIMESTAMP = "timestamp"


class Shape(BaseModel):
    type: ShapeType
    members: Optional[ShapeMember]
    member: Optional[ShapeMember]
    errors: Optional[list[TargetReference]]
    input: Optional[TargetReference]
    output: Optional[TargetReference]
    traits: Optional[Trait]


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
    # documentation: str
    idempotent: Optional[bool]


class Operations(BaseModel):
    __root__: dict[str, Operation]


class v3Json(BaseModel):
    smithy: float
    metadata: dict
    shapes: dict[str, ServiceShape | Shape]


_smithy_json = "v3-smithy.json"
j_smithy = ingest_json(_smithy_json)


def view_shape_source(shape_name="com.amazonaws.sfn#AWSStepFunctions"):
    return j_smithy["shapes"][shape_name]


def view_shape_info(shape_key: str = "operations", subkey: str | None = None):
    for v in [*j_smithy["shapes"].values()]:
        if v["type"] == "service" and shape_key in v:
            if subkey is None:
                print(v[shape_key])
            else:
                if subkey in v[shape_key]:
                    print(v[shape_key][subkey])


smithy_model = v3Json.parse_obj(j_smithy)
_shape_iterator = (v for v in smithy_model.shapes.values())
service_shape = next(_shape_iterator)
nonservice_shapes = [s for s in _shape_iterator]
