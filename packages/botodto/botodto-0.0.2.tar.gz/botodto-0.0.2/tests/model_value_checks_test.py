"""
Tests for complete model integrity.
"""
from botodto.aws.data_model_v2_min import build_model as build_model_min
from botodto.aws.data_model_v2_min import v2MinJson
from botodto.aws.data_model_v2_norm import build_model as build_model_norm
from botodto.aws.data_model_v2_norm import v2NormalJson
from botodto.aws.data_model_v3 import build_model as build_model_v3
from botodto.aws.data_model_v3 import v3Json


def test_v2_min_value_check():
    model = build_model_min()
    assert isinstance(model, v2MinJson)
    assert model.shapes  # ["ActivityList"].member is not None


def test_v2_norm_ActivityList_value_check():
    model = build_model_norm()
    assert isinstance(model, v2NormalJson)
    shape_member = model.shapes["ActivityList"].member
    assert shape_member.shape == "ActivityListItem"


def test_v3_value_check():
    model = build_model_v3()
    assert isinstance(model, v3Json)
    service_shape = model.shapes["com.amazonaws.sfn#AWSStepFunctions"]
    assert service_shape.type == "service"
    assert len(service_shape.operations) == 26
    assert service_shape.operations[0].target == "com.amazonaws.sfn#CreateActivity"
