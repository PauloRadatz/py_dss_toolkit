# -*- encoding: utf-8 -*-

import pathlib
from typing import Optional
from typing import Union

from py_dss_toolkit.studies.SnapShotPowerFlow.StudySnapShotPowerFlow import StudySnapShotPowerFlow
from py_dss_toolkit.studies.TimeSeriesPowerFlow.StudyTimeSeriesPowerFlow import StudyTimeSeriesPowerFlow
from py_dss_toolkit.studies.BDGD2OpenDSSYearlyModel import BDGD2OpenDSSYearlyModel


class CreateStudy:
    """Factory for structured OpenDSS studies (compile DSS, run, visualize).

    Use :meth:`snapshot` or :meth:`timeseries` to obtain a study object with a
    compiled circuit and attached ``py_dss_interface.DSS`` instance.
    """

    @staticmethod
    def snapshot(
        name: str,
        dss_file: Union[str, pathlib.Path],
        base_frequency: Union[int, float] = 60,
        dss_dll: Optional[str] = None,
    ) -> StudySnapShotPowerFlow:
        """Build a snapshot (steady-state) power-flow study.

        Args:
            name: Study label.
            dss_file: Path to the main DSS file to compile.
            base_frequency: System base frequency in Hz (default 60).
            dss_dll: Optional path to the OpenDSS library; if omitted, defaults apply.

        Returns:
            StudySnapShotPowerFlow: Configured study; call its ``run()`` (or equivalent)
            after setup to execute the simulation workflow.
        """
        sc = StudySnapShotPowerFlow(_name=name, _dss_file=dss_file, _base_frequency=base_frequency, _dss_dll=dss_dll)
        return sc

    @staticmethod
    def timeseries(
        name: str,
        dss_file: Union[str, pathlib.Path],
        base_frequency: Union[int, float] = 60,
        dss_dll: Optional[str] = None,
    ) -> StudyTimeSeriesPowerFlow:
        """Build a time-series (e.g. QSTS) power-flow study.

        Args:
            name: Study label.
            dss_file: Path to the main DSS file to compile.
            base_frequency: System base frequency in Hz (default 60).
            dss_dll: Optional path to the OpenDSS library; if omitted, defaults apply.

        Returns:
            StudyTimeSeriesPowerFlow: Configured study for time-series simulation.
        """
        sc = StudyTimeSeriesPowerFlow(_name=name, _dss_file=dss_file, _base_frequency=base_frequency, _dss_dll=dss_dll)
        return sc

    @staticmethod
    def bdgd2opendss_yearly_model(
        name: str,
        dss_model_folder: Union[str, pathlib.Path],
        base_frequency: Union[int, float] = 60,
        dss_dll: Optional[str] = None,
    ) -> BDGD2OpenDSSYearlyModel:
        """Build a BDGD to OpenDSS 8760 yearly model study converter.

        Args:
            name: Study label.
            dss_model_folder: Path to the BDGD model folder.
            base_frequency: System base frequency in Hz (default 60).
            dss_dll: Optional path to the OpenDSS library; if omitted, defaults apply.

        Returns:
            BDGD2OpenDSSYearlyModel: Configured study for BDGD 8760 conversion.
        """
        return BDGD2OpenDSSYearlyModel(
            _name=name,
            dss_model_folder=dss_model_folder,
            _base_frequency=base_frequency,
            _dss_dll=dss_dll,
        )

    # @staticmethod
    # def fault_study(
    #     name: str,
    #     dss_file: Union[str, pathlib.Path],
    #     base_frequency: Union[int, float] = 60,
    #     dss_dll: Optional[str] = None) -> StudyFault:
    #     sc = StudyFault(_name=name, _dss_file=dss_file, _base_frequency=base_frequency, _dss_dll=dss_dll)
    #     return sc
