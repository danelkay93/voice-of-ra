import json
from pathlib import Path
from jsonschema import validate
from jsonschema import ValidationError as JSONSchemaValidationError
from pydantic import ValidationError

from schema import SIMPLIFIED_SCHEMA, DataProcessingError

def read_json_file(file_path: Path) -> dict:
    try:
        return json.loads(file_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise DataProcessingError(f"Error reading JSON file: {e}")

def validate_json_schema(data: dict) -> None:
    try:
        validate(instance=data, schema=SIMPLIFIED_SCHEMA)
    except JSONSchemaValidationError as e:
        raise DataProcessingError(f"JSON schema validation error: {e}")

def write_output(file_path: Path, content: str) -> None:
    try:
        file_path.write_text(content, encoding="utf-8")
    except Exception as e:
        raise DataProcessingError(f"Error writing output file: {e}")
