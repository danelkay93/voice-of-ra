from hypothesis import given
from hypothesis import strategies as st

from model import Scenario


@given(st.builds(Scenario))
def test_scenario_model(scenario: Scenario) -> None:
    pytest.assume(isinstance(scenario, Scenario))
    pytest.assume(scenario.scenario_id is not None)
    pytest.assume(scenario.scenario_name is not None)
    pytest.assume(scenario.full_name is not None)
    pytest.assume(scenario.header is not None)
    pytest.assume(isinstance(scenario.steps, list))
    pytest.assume(isinstance(scenario.resolutions, list))
