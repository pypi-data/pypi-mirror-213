r"""
:mod:`botodto` is a Data Transfer Object (DTO) codegen library to produce Pydantic
data models to wrap the AWS SDK library boto3."""

__all__ = ["aws"]

__author__ = "Louis Maddox"
__license__ = "MIT"
__description__ = "Pydantic interface codegen from Amazon Smithy JSON schemas"
__url__ = "https://github.com/lmmx/botodto"
__uri__ = __url__
__email__ = "louismmx@gmail.com"

from . import aws, api
