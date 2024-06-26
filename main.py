import json
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Annotated, Any

import click
from jsonschema import ValidationError as JSONSchemaValidationError
from jsonschema import validate
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


# Models
class MarkDownModel(BaseModel, ABC):
    model_config = ConfigDict(populate_by_name=True)

    @classmethod
    def markdown_fields(cls) -> list[str]:
        return []

    @abstractmethod
    def to_markdown(self) -> str:
        pass


class Narration(MarkDownModel):
    narration_id: Annotated[str, Field(alias="id")]
    name: str | None = None
    lang: list[str] | None = None

    def to_markdown(self) -> str:
        if not self.narration_id:
            msg = "Narration ID is missing."
            raise DataProcessingError(msg)
        return f"{self.narration_id}\n{H2_HEADER}\n"


class Step(MarkDownModel):
    step_id: Annotated[str, Field(alias="id")]
    narration: Narration | None = None
    text: str | None = None
    type: str | None = None

    @classmethod
    def markdown_fields(cls) -> list[str]:
        return ["narration", "text"]

    def to_markdown(self) -> str:
        output = []
        if self.narration:
            output.append(self.narration.to_markdown())
        if self.text:
            output.append(f"{self.text}\n{H1_HEADER}")
        return "".join(output)


class Resolution(MarkDownModel):
    resolution_id: Annotated[str, Field(alias="id")]
    narration: Narration
    text: str

    @classmethod
    def markdown_fields(cls) -> list[str]:
        return ["narration", "text"]

    def to_markdown(self) -> str:
        return f"{self.narration.to_markdown()}{self.text}\n{H1_HEADER}"


class Scenario(MarkDownModel):
    scenario_id: Annotated[str, Field(alias="id")]
    scenario_name: str
    full_name: str
    header: str
    steps: list[Step]
    resolutions: list[Resolution]

    @classmethod
    def markdown_fields(cls) -> list[str]:
        return ["steps", "resolutions"]

    def to_markdown(self) -> str:
        output = [f"{self.scenario_name}\n{H1_HEADER}"]
        story_steps = [step for step in self.steps if step.narration]
        for item in story_steps + self.resolutions:
            output.append(item.to_markdown())
        return "\n".join(output)

    @classmethod
    def from_json(cls, file_path: Path) -> "Scenario":
        """Read and parse the JSON file using Pydantic and validate against schema."""
        try:
            data = json.loads(file_path.read_text(encoding="utf-8"))
            validate(instance=data, schema=SIMPLIFIED_SCHEMA)
            return cls.model_validate(data)
        except (json.JSONDecodeError, JSONSchemaValidationError, ValidationError) as e:
            logging.error("Error processing JSON data", exc_info=True)
            msg = "Invalid JSON data"
            raise DataProcessingError(msg) from e


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
