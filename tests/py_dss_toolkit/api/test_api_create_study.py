import os
import pathlib

from py_dss_toolkit import CreateStudy
from py_dss_toolkit.results.SnapShot.SnapShotPowerFlowResults import SnapShotPowerFlowResults
from py_dss_toolkit.results.TimeSeries.TimeSeriesPowerFlowResults import TimeSeriesPowerFlowResults
from py_dss_toolkit.studies.SnapShotPowerFlow.StudySnapShotPowerFlow import StudySnapShotPowerFlow
from py_dss_toolkit.studies.TimeSeriesPowerFlow.StudyTimeSeriesPowerFlow import StudyTimeSeriesPowerFlow


SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
DSS_FILE_13BUS = pathlib.Path(SCRIPT_PATH).joinpath("../cases", "13bus", "IEEE13Nodeckt.dss")


def test_create_study_snapshot_returns_expected_type_and_wiring():
    study = CreateStudy.snapshot(name="snapshot study", dss_file=DSS_FILE_13BUS)

    assert isinstance(study, StudySnapShotPowerFlow)
    assert isinstance(study.results, SnapShotPowerFlowResults)
    assert study.settings is not None
    assert study.static_view is not None
    assert study.interactive_view is not None
    assert study.dss_view is not None


def test_create_study_timeseries_returns_expected_type_and_wiring():
    study = CreateStudy.timeseries(name="timeseries study", dss_file=DSS_FILE_13BUS)

    assert isinstance(study, StudyTimeSeriesPowerFlow)
    assert isinstance(study.results, TimeSeriesPowerFlowResults)
    assert study.settings is not None
    assert study.static_view is not None
    assert study.interactive_view is not None
    assert study.dss_view is not None


