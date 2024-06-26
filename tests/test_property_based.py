from hypothesis import given
from hypothesis import strategies as st

from model import Scenario


@given(st.builds(Scenario))
def test_scenario_model(scenario: Scenario) -> None:
    assert isinstance(scenario, Scenario)  # noqa: S101
    assert scenario.scenario_id is not None  # noqa: S101
    assert scenario.scenario_name is not None  # noqa: S101
    assert scenario.full_name is not None  # noqa: S101
    assert scenario.header is not None  # noqa: S101
    assert isinstance(scenario.steps, list)  # noqa: S101
    assert isinstance(scenario.resolutions, list)  # noqa: S101
