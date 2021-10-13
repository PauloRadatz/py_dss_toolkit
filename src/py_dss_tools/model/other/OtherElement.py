# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 24/09/2021 at 23:29:42
 Project: py_dss_tools [set, 2021]
"""
from abc import abstractmethod, ABC
from dataclasses import dataclass


@dataclass
class OtherElement(ABC):
    """
    _basefreq: Base Frequency for ratings.

    _enabled: {Yes|No or True|False} Indicates whether this element is enabled.

    _like: Make like another object, e.g.:
        New Capacitor.C2 like=c1  ...

    _phases: Number of Phases. Default is 1.

    """
    _basefreq: float = 60
    _enabled: str = 'true'
    _like: str = ''
    _phases: int = 1

    @property
    @abstractmethod
    def basefreq(self):
        pass

    @basefreq.setter
    @abstractmethod
    def basefreq(self, value):
        pass

    @property
    @abstractmethod
    def enabled(self):
        pass

    @enabled.setter
    @abstractmethod
    def enabled(self, value):
        pass

    @property
    @abstractmethod
    def like(self):
        pass

    @like.setter
    @abstractmethod
    def like(self, value):
        pass

    @property
    @abstractmethod
    def phases(self):
        pass

    @phases.setter
    @abstractmethod
    def phases(self, value):
        pass
