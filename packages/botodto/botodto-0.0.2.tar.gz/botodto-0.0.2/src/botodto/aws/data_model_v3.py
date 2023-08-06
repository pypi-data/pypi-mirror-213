from __future__ import annotations

from enum import Enum
from functools import partial
from pprint import pprint as _pprint
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

from ..utils.json_utils import ingest_json

pprint = partial(_pprint, sort_dicts=False)


class ShapeMember(BaseModel):
    __root__: dict[str, Optional[str]]


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


class TargetTrait(BaseModel):
    required: Optional[dict[str, str]] = Field(alias="smithy.api#required")
    enumValue: Optional[str] = Field(alias="smithy.api#enumValue")
    default: Optional[Any] = Field(alias="smithy.api#default")
    # documentation: str = Field(..., alias="smithy.api#documentation")


class TraitWithNamedTarget(BaseModel):
    target: str
    traits: Optional[TargetTrait]  # Optional[dict]  # Optional[dict[str, Trait]]


class SpecialShapeMember(BaseModel):
    __root__: dict[str, Optional[TraitWithNamedTarget]]


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
    members: Optional[SpecialShapeMember]
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


def read_source():
    _smithy_json = "v3-smithy.json"
    j_smithy = ingest_json(_smithy_json)
    return j_smithy


def check_rehydrate(model: BaseModel, source: dict) -> bool:
    rehydrated = model.dict(by_alias=True, exclude_unset=True)
    return rehydrated == source


def inspect_source():
    source = read_source()
    shape_it = iter(source["shapes"].items())
    next(shape_it)  # Discard service shape
    rest_of_shapes = [*shape_it]
    for s_name, s in rest_of_shapes:
        if "members" in s:
            members_info = s["members"]
            members_vals = list(members_info.values())
            members_vals_keys = [k for d in members_vals for k, v in d.items()]
            check = tuple([k in members_vals_keys for k in ["traits", "target"]])
            if check[0]:
                for subdict in members_vals:
                    if traits_dict := subdict.get("traits", {}):
                        traits_dict.pop("smithy.api#documentation", None)
                        if traits_dict:
                            try:
                                tt = TargetTrait.parse_obj(traits_dict)
                                rehydrate = check_rehydrate(tt, traits_dict)
                                if not rehydrate:
                                    print(f"Did not rehydrate {tt} into {traits_dict}")
                            except Exception as exc:
                                print(f"Raised {exc}")
                            pass
    return


def view_shape_source(shape_name="com.amazonaws.sfn#AWSStepFunctions"):
    j_smithy = read_source()
    return j_smithy["shapes"][shape_name]


def view_shape_info(shape_key: str = "operations", subkey: str | None = None):
    j_smithy = read_source()
    for v in [*j_smithy["shapes"].values()]:
        if v["type"] == "service" and shape_key in v:
            if subkey is None:
                print(v[shape_key])
            else:
                if subkey in v[shape_key]:
                    print(v[shape_key][subkey])


def build_model():
    j_smithy = read_source()
    smithy_model = v3Json.parse_obj(j_smithy)
    return smithy_model


def extract_shapes():
    smithy_model = build_model()
    _shape_iterator = (v for v in smithy_model.shapes.values())
    service_shape = next(_shape_iterator)
    nonservice_shapes = [s for s in _shape_iterator]
    return service_shape, nonservice_shapes


# service_shape, nonservice_shapes = extract_shapes()
