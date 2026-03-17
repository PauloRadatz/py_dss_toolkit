# -*- encoding: utf-8 -*-

import pathlib

from py_dss_toolkit.studies.SnapShotPowerFlow.StudySnapShotPowerFlow import StudySnapShotPowerFlow
from py_dss_toolkit.studies.TimeSeriesPowerFlow.StudyTimeSeriesPowerFlow import StudyTimeSeriesPowerFlow

from typing import Optional, Union


# TODO
# def check_scenario_exist(sc) -> bool:
#     return isinstance(sc, Scenario)

class CreateStudy:
    @staticmethod
    def snapshot(
        name: str,
        dss_file: Union[str, pathlib.Path],
        base_frequency: Union[int, float] = 60,
        dss_dll: Optional[str] = None) -> StudySnapShotPowerFlow:
        sc = StudySnapShotPowerFlow(_name=name, _dss_file=dss_file, _base_frequency=base_frequency, _dss_dll=dss_dll)
        return sc

    @staticmethod
    def timeseries(
        name: str,
        dss_file: Union[str, pathlib.Path],
        base_frequency: Union[int, float] = 60,
        dss_dll: Optional[str] = None) -> StudyTimeSeriesPowerFlow:
        sc = StudyTimeSeriesPowerFlow(_name=name, _dss_file=dss_file, _base_frequency=base_frequency, _dss_dll=dss_dll)
        return sc

    # @staticmethod
    # def fault_study(
    #     name: str,
    #     dss_file: Union[str, pathlib.Path],
    #     base_frequency: Union[int, float] = 60,
    #     dss_dll: Optional[str] = None) -> StudyFault:
    #     sc = StudyFault(_name=name, _dss_file=dss_file, _base_frequency=base_frequency, _dss_dll=dss_dll)
    #     return sc


