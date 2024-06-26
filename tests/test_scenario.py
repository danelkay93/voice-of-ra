from pathlib import Path

from model import Scenario
from utils import read_json_file, validate_json_schema


def test_scenario_from_json(example_json_path: Path) -> None:
    scenario = Scenario.from_json(example_json_path)
    assert scenario.scenario_id == "example_scenario"
    assert scenario.scenario_name == "Example Scenario"
    assert scenario.full_name == "Scenario I: Example Scenario"
    assert scenario.header == "Scenario I"
    assert scenario.steps == []
    assert scenario.resolutions == []


def test_read_json_file(example_json_path: Path) -> None:
    data = read_json_file(example_json_path)
    assert data["id"] == "example_scenario"


def test_validate_json_schema(example_json_path: Path) -> None:
    data = read_json_file(example_json_path)
    validate_json_schema(data)
