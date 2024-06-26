import json
from abc import ABC, abstractmethod
from typing import Annotated
from pathlib import Path
from pydantic import BaseModel, ConfigDict, Field
from utils import read_json_file, validate_json_schema

from main import DataProcessingError

# Constants
H1_HEADER = "=" * 6
H2_HEADER = "-" * 6

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
        data = read_json_file(file_path)
        validate_json_schema(data)
        return cls.model_validate(data)
