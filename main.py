import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import click

from model import Scenario
from schema import DataProcessingError
from utils import write_output as utils_write_output

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


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


def process_scenario(file_path: Path, output_strategy: OutputStrategy) -> None:
    try:
        scenario = LoadJSONCommand().execute({"file_path": file_path})
        output = output_strategy.generate(scenario)
        output_path = file_path.parent / (file_path.stem + "_output.txt")
        utils_write_output(output_path, output)
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
