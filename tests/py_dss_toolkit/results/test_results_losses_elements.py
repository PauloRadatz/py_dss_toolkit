import pytest

from py_dss_toolkit import dss_tools


def assert_losses_elements_13bus(dfs):
    p_df, q_df = dfs
    assert p_df.shape == (19, 1)
    assert q_df.shape == (19, 1)
    assert "P losses (kW)" in p_df.columns
    assert "Q losses (kvar)" in q_df.columns
    assert p_df.index.equals(q_df.index)


def test_dss_tools_13bus_results_losses_elements(dss_tools_13bus):
    dss_tools.simulation.solve_snapshot()
    dfs = dss_tools.results.losses_elements
    assert_losses_elements_13bus(dfs)


def test_snapshot_13bus_results_losses_elements(snapshot_study_13bus):
    snapshot_study_13bus.run()
    dfs = snapshot_study_13bus.results.losses_elements
    assert_losses_elements_13bus(dfs)


@pytest.mark.parametrize(
    "study_fixture_name",
    [
        "snapshot_study_13bus",
        "timeseries_study_13bus",
    ],
)
def test_results_losses_elements_all_studies(request, study_fixture_name):
    study = request.getfixturevalue(study_fixture_name)
    study.run()
    df_p_shape = study.results.losses_elements[0].shape
    df_q_shape = study.results.losses_elements[1].shape
    assert df_p_shape == (19, 1)
    assert df_q_shape == (19, 1)
