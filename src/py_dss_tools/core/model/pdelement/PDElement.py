# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 24/09/2021 at 22:29:34
 Project: py_dss_tools [set, 2021]
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from py_dss_tools.core.model.pdelement.PDElementError import PDElementError
from py_dss_tools.utils.Utils import Utils


@dataclass
class PDElement(ABC):
    """
    __basefreq: Base Frequency for ratings.

    __emergamps: Maximum or emerg current.

    __enabled: {Yes|No or True|False} Indicates whether this element is enabled.

    __faultrate: Failure rate PER UNIT LENGTH per year. Length must be same units as LENGTH property. Default is 0.1
    fault per unit length per year.

    __like: Make like another object, e.g.: New Capacitor.C2 like=c1

    __normamps: Normal rated current.

    __pctperm: Percent of failures that become permanent. Default is 20.

    __phases: Number of phases, this line.

    __repair: Hours to repair. Default is 3 hr.
    """
    _basefreq: float = 60
    _emergamps: float = 600
    _enabled: str = 'true'
    _faultrate: float = 0.1
    _like: str = ''
    _name: str = 'my_pdelement_' + Utils.generate_random_string()
    _normamps: float = 400
    _pctperm: float = 20
    _phases: int = 3
    _repair: float = 3

    @property
    @abstractmethod
    def emergamps(self):
        pass

    @emergamps.setter
    @abstractmethod
    def emergamps(self, value):
        pass

    @property
    @abstractmethod
    def enabled(self):
        pass

    @enabled.setter
    @abstractmethod
    def enabled(self, value: str):
        pass

    @property
    @abstractmethod
    def faultrate(self):
        pass

    @faultrate.setter
    @abstractmethod
    def faultrate(self, value: float):
        pass

    @property
    @abstractmethod
    def like(self):
        pass

    @like.setter
    @abstractmethod
    def like(self, value: str):
        pass

    @property
    @abstractmethod
    def name(self):
        pass

    @name.setter
    @abstractmethod
    def name(self, value: str):
        pass

    @property
    @abstractmethod
    def normamps(self):
        pass

    @normamps.setter
    @abstractmethod
    def normamps(self, value: float):
        pass

    @property
    @abstractmethod
    def pctperm(self):
        pass

    @pctperm.setter
    @abstractmethod
    def pctperm(self, value: float):
        pass

    @property
    @abstractmethod
    def phases(self):
        pass

    @phases.setter
    @abstractmethod
    def phases(self, value: int):
        pass

    @property
    @abstractmethod
    def repair(self):
        pass

    @repair.setter
    @abstractmethod
    def repair(self, value: float):
        pass

    def check_instance(self, value: [str, float, int], property_name: str, type_: List[str]):
        if type(value).__name__ not in type_:
            raise PDElementError(self._name,
                                 f"Type Error, check the type of the variable {property_name}. Expected: {type_}, but "
                                 f"found {type(value)}")
        else:
            return
