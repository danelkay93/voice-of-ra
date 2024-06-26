from hypothesis import given
from hypothesis import strategies as st

from model import Scenario


@given(st.builds(Scenario))
def test_scenario_model(scenario) -> None:
    assert isinstance(scenario, Scenario)
    assert scenario.scenario_id is not None
    assert scenario.scenario_name is not None
    assert scenario.full_name is not None
    assert scenario.header is not None
    assert isinstance(scenario.steps, list)
    assert isinstance(scenario.resolutions, list)
