from pathlib import Path
from model import Scenario
from utils import read_json_file, validate_json_schema


def test_scenario_from_json(example_json_path: Path) -> None:
    scenario = Scenario.from_json(example_json_path)
    assert scenario.scenario_id == "example_scenario"  # noqa: S101
    assert scenario.scenario_name == "Example Scenario"  # noqa: S101
    assert scenario.full_name == "Scenario I: Example Scenario"  # noqa: S101
    assert scenario.header == "Scenario I"  # noqa: S101
    assert scenario.steps == []  # noqa: S101
    assert scenario.resolutions == []  # noqa: S101


def test_read_json_file(example_json_path: Path) -> None:
    data = read_json_file(example_json_path)
    assert data["id"] == "example_scenario"  # noqa: S101


def test_validate_json_schema(example_json_path: Path) -> None:
    data = read_json_file(example_json_path)
    validate_json_schema(data)
