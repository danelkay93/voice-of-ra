import json

import pytest


@pytest.fixture(scope="session")
def example_json_path(tmp_path_factory: pytest.TempPathFactory) -> Path:
    json_content = {
        "id": "example_scenario",
        "scenario_name": "Example Scenario",
        "full_name": "Scenario I: Example Scenario",
        "header": "Scenario I",
        "steps": [],
        "resolutions": []
    }
    file_path = tmp_path_factory.mktemp("data") / "example_scenario.json"
    file_path.write_text(json.dumps(json_content), encoding="utf-8")
    return file_path
