# AWS service schema data handling

## Problem statement

1. OpenAPI schemas for AWS services are available from the OpenAPI Directory but are missing exceptions.

2. Pydantic model code can be generated from OpenAPI schemas using the `datamodel-code-generator` package.

3. The `boto3` library ingests/outputs JSON objects with no awareness of the underlying service schema,
   Pydantic models representing the services' data models eliminate manual handling at API call points,
   give model types semantic interpretation, avoid need for manually writing custom container
   classes for these standard formats, and reduce the code smell of 'primitive obsession' (`dict` overuse).

  - e.g. specific errors, but unclear if possible by this approach

4. The `boto3` library can be wrapped at the client level, and operations mapped to Pydantic models
   so as to parse both calls (inputs) and responses (outputs).

## Solution

- Wrap `boto3` so that the `__getattr__` calls which produce calls to any name in the `_PY_TO_OP` enum of
  API operations is wrapped by the appropriate Pydantic model.

- Produce Pydantic models by `datamodel-code-generator` on the OpenAPI schema derived from the v2 JS SDK

- Supplement the Pydantic models with exception types.

Whether the v3 types will be added at the OpenAPI schema stage or after (i.e. before or after
`datamodel-code-generator` processes the OpenAPI schema) is still unclear. It will become clear once
I assess how trivial the exception types are. I suspect they may reliably be `message: str`-bearing
singletons, perhaps with pattern constraints.
