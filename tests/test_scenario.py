from pathlib import Path

from model import Scenario
from utils import read_json_file, validate_json_schema


def test_scenario_from_json(example_json_path: Path) -> None:
    scenario = Scenario.from_json(example_json_path)
    pytest.assume(scenario.scenario_id == "example_scenario")
    pytest.assume(scenario.scenario_name == "Example Scenario")
    pytest.assume(scenario.full_name == "Scenario I: Example Scenario")
    pytest.assume(scenario.header == "Scenario I")
    pytest.assume(scenario.steps == [])
    pytest.assume(scenario.resolutions == [])


def test_read_json_file(example_json_path: Path) -> None:
    data = read_json_file(example_json_path)
    pytest.assume(data["id"] == "example_scenario")


def test_validate_json_schema(example_json_path: Path) -> None:
    data = read_json_file(example_json_path)
    validate_json_schema(data)
