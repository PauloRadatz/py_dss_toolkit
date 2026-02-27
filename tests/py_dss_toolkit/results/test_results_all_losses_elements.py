import py_dss_interface
import pytest

from py_dss_toolkit import dss_tools

# Skip when cktelement.all_losses is not yet in py_dss_interface
_has_all_losses = hasattr(py_dss_interface.DSS().cktelement, "all_losses")
pytestmark = pytest.mark.skipif(
    not _has_all_losses,
    reason="cktelement.all_losses not yet in py_dss_interface",
)

EXPECTED_COLUMNS = [
    "P total (kW)",
    "Q total (kvar)",
    "P load (kW)",
    "Q load (kvar)",
    "P no-load (kW)",
    "Q no-load (kvar)",
]


def assert_all_losses_elements_13bus(df):
    assert df.shape == (19, 6)
    assert list(df.columns) == EXPECTED_COLUMNS


def test_dss_tools_13bus_results_all_losses_elements(dss_tools_13bus):
    dss_tools.simulation.solve_snapshot()
    df = dss_tools.results.all_losses_elements
    assert_all_losses_elements_13bus(df)


def test_snapshot_13bus_results_all_losses_elements(snapshot_study_13bus):
    snapshot_study_13bus.run()
    df = snapshot_study_13bus.results.all_losses_elements
    assert_all_losses_elements_13bus(df)


@pytest.mark.parametrize(
    "study_fixture_name",
    [
        "snapshot_study_13bus",
        "timeseries_study_13bus",
    ],
)
def test_results_all_losses_elements_all_studies(request, study_fixture_name):
    study = request.getfixturevalue(study_fixture_name)
    study.run()
    df_shape = study.results.all_losses_elements.shape
    assert df_shape == (19, 6)
