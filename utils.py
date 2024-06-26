import json
from pathlib import Path

from jsonschema import ValidationError as JSONSchemaValidationError
from jsonschema import validate

from schema import SIMPLIFIED_SCHEMA, DataProcessingError


def read_json_file(file_path: Path) -> dict:
    try:
        return json.loads(file_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        msg = f"Error reading JSON file: {e}"
        raise DataProcessingError(msg)


def validate_json_schema(data: dict) -> None:
    try:
        validate(instance=data, schema=SIMPLIFIED_SCHEMA)
    except JSONSchemaValidationError as e:
        msg = f"JSON schema validation error: {e}"
        raise DataProcessingError(msg)


def write_output(file_path: Path, content: str) -> None:
    try:
        file_path.write_text(content, encoding="utf-8")
    except Exception as e:
        msg = f"Error writing output file: {e}"
        raise DataProcessingError(msg)
