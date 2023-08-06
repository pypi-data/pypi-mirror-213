"""
Tests for complete model integrity.
"""
from botodto.aws.data_model_v2_min import build_model as build_model_min
from botodto.aws.data_model_v2_min import v2MinJson
from botodto.aws.data_model_v2_norm import build_model as build_model_norm
from botodto.aws.data_model_v2_norm import v2NormalJson
from botodto.aws.data_model_v3 import build_model as build_model_v3
from botodto.aws.data_model_v3 import v3Json


def test_v2_min_build():
    model = build_model_min()
    assert isinstance(model, v2MinJson)


def test_v2_norm_build():
    model = build_model_norm()
    assert isinstance(model, v2NormalJson)


def test_v3_build():
    model = build_model_v3()
    assert isinstance(model, v3Json)
