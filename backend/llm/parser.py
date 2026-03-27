# backend/llm/parser.py

from jsonschema import validate, ValidationError


def validate_schema(data: dict, schema: dict) -> dict:
    """
    Validate LLM output against schema
    """
    try:
        validate(instance=data, schema=schema)
        return data
    except ValidationError as e:
        raise ValueError(f"Schema validation failed:\n{e.message}")


def safe_parse(llm_output: dict, schema: dict) -> dict:
    """
    Full pipeline:
    - Validate structure
    - Return clean data
    """
    if not isinstance(llm_output, dict):
        raise ValueError("LLM output is not a dictionary")

    return validate_schema(llm_output, schema)