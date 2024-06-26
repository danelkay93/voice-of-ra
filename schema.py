import json

# Custom exception
class DataProcessingError(Exception):
    """Custom exception for data processing errors"""

# Simplified JSON schema
SIMPLIFIED_SCHEMA = json.loads("""
{
  "$schema": "http://json-schema.org/schema#",
  "type": "object",
  "properties": {
    "id": { "type": "string" },
    "scenario_name": { "type": "string" },
    "full_name": { "type": "string" },
    "header": { "type": "string" },
    "steps": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": { "type": "string" },
          "narration": {
            "type": "object",
            "properties": {
              "id": { "type": "string" },
              "name": { "type": "string" },
              "lang": { "type": "array", "items": { "type": "string" } }
            },
            "required": ["id"]
          },
          "text": { "type": "string" },
          "type": { "type": "string" }
        },
        "required": ["id"]
      }
    },
    "resolutions": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": { "type": "string" },
          "narration": {
            "type": "object",
            "properties": {
              "id": { "type": "string" },
              "name": { "type": "string" },
              "lang": { "type": "array", "items": { "type": "string" } }
            },
            "required": ["id"]
          },
          "text": { "type": "string" }
        },
        "required": ["id"]
      }
    }
  },
  "required": ["id", "scenario_name", "full_name", "header", "steps", "resolutions"]
}
""")
