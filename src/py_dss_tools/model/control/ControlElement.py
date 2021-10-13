# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 25/09/2021 at 00:01:58
 Project: py_dss_tools [set, 2021]
"""
from abc import ABC
from dataclasses import dataclass

from py_dss_tools.utils.Utils import Utils


@dataclass
class ControlElement(ABC):
    """
    __basefreq: Base Frequency for ratings.

    __enabled: {Yes|No or True|False} Indicates whether this element is enabled.

    __like: Make like another object, e.g.: New Capacitor.C2 like=c1.
    """
    __basefreq: int = 60
    # TODO: create a enum in utils module
    __enabled: str = 'true'
    __like: str = ''
    __name: str = "my_capcpontrol_" + Utils.generate_random_string()

    @property
    def basefreq(self):
        return self.__basefreq

    @basefreq.setter
    def basefreq(self, value):
        self.__basefreq = value

    @property
    def enabled(self):
        return self.__enabled

    @enabled.setter
    def enabled(self, value):
        self.__enabled = value

    @property
    def like(self):
        return self.__like

    @like.setter
    def like(self, value):
        self.__like = value
