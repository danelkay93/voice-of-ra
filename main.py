import json
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Annotated, Any

import click
from model import Narration, Step, Resolution, Scenario
from utils import read_json_file, validate_json_schema, write_output
from pydantic import BaseModel, ConfigDict, Field, ValidationError

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Constants
H1_HEADER = "=" * 6
H2_HEADER = "-" * 6


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




# Command pattern
class Command(ABC):
    @abstractmethod
    def execute(self, data: dict[str, Any]) -> Any:
        pass


class LoadJSONCommand(Command):
    def execute(self, data: dict[str, Any]) -> Scenario:
        file_path = data["file_path"]
        return Scenario.from_json(file_path)


# Strategy pattern
class OutputStrategy(ABC):
    @abstractmethod
    def generate(self, scenario: Scenario) -> str:
        pass


class MarkdownOutputStrategy(OutputStrategy):
    def generate(self, scenario: Scenario) -> str:
        return scenario.to_markdown()


class HTMLOutputStrategy(OutputStrategy):
    def generate(self, scenario: Scenario) -> str:
        # Placeholder for HTML generation
        return f"<html><body><h1>{scenario.scenario_name}</h1></body></html>"


class TTSOutputStrategy(OutputStrategy):
    def generate(self, scenario: Scenario) -> str:
        # Stub for future TTS implementation
        msg = "TTS output is not yet implemented"
        raise NotImplementedError(msg)


def write_output(file_path: Path, content: str) -> None:
    try:
        file_path.write_text(content, encoding="utf-8")
        logging.info(f"Output written successfully: {file_path}")
    except Exception as e:
        logging.error("Failed to write output file", exc_info=True)
        msg = f"Error writing output file: {e}"
        raise DataProcessingError(msg)


def process_scenario(file_path: Path, output_strategy: OutputStrategy) -> None:
    try:
        scenario = LoadJSONCommand().execute({"file_path": file_path})
        output = output_strategy.generate(scenario)
        output_path = file_path.with_stem(file_path.stem + "_output").with_suffix(".txt")
        write_output(output_path, output)
    except DataProcessingError as e:
        logging.exception(f"Error processing scenario: {e}")
        raise


@click.command()
@click.argument("input_file_path", type=click.Path(exists=True, path_type=Path), required=True)
@click.option("--output-format", type=click.Choice(["markdown", "html", "tts"]), default="markdown")
def main(input_file_path: Path, output_format: str) -> None:
    strategy_map = {
        "markdown": MarkdownOutputStrategy(),
        "html": HTMLOutputStrategy(),
        "tts": TTSOutputStrategy(),
    }

    try:
        strategy = strategy_map[output_format]
        process_scenario(input_file_path, strategy)
    except NotImplementedError:
        logging.exception("The selected output strategy is not yet implemented.")
        msg = "Selected output strategy is not available."
        raise click.ClickException(msg)
    except DataProcessingError as e:
        logging.exception(f"Data processing failed: {e}")
        raise click.ClickException(str(e))


if __name__ == "__main__":
    main()
