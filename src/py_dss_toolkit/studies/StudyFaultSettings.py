# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : StudyFaultSettings.py
# @Software: PyCharm

from dataclasses import dataclass
from dataclasses import field

from py_dss_toolkit.studies.settings_utils import VALID_FAULT_MODES
from py_dss_toolkit.studies.settings_utils import FaultModeType
from py_dss_toolkit.studies.settings_utils import check_mode
from py_dss_toolkit.studies.settings_utils import get_settings
from py_dss_toolkit.studies.settings_utils import set_mode
from py_dss_toolkit.studies.StudySettings import StudySettings


@dataclass(kw_only=True)
class StudyFaultSettings(StudySettings):
    _mode: str = field(init=False)

    def __post_init__(self):
        self._mode = check_mode(self._dss, VALID_FAULT_MODES)

    @property
    def mode(self) -> str:
        """Get the current fault study mode.

        Returns:
            Mode string: 'faultstudy', 'f', or 'fault'
        """
        return self._mode

    @mode.setter
    def mode(self, value: FaultModeType):
        """Set the fault study mode.

        Args:
            value: Mode string - 'faultstudy', 'f', or 'fault'
        """
        self._mode = set_mode(self._dss, VALID_FAULT_MODES, value)

    def get_settings(self):
        return get_settings(self.__dict__)
