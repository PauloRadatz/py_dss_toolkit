# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 24/09/2021 at 22:29:34
 Project: py_dss_tools [set, 2021]
"""
from abc import ABC, abstractmethod

import attr

from py_dss_tools.utils import Utils


@attr.s(kw_only=True)
class PDElement(ABC):
    """
    _basefreq: Base Frequency for ratings.

    _emergamps: Maximum or emerg current.

    _enabled: {Yes|No or True|False} Indicates whether this element is enabled.

    _faultrate: Failure rate PER UNIT LENGTH per year. Length must be same units as LENGTH property. Default is 0.1
    fault per unit length per year.

    _like: Make like another object, e.g.: New Capacitor.C2 like=c1

    _normamps: Normal rated current.

    _pctperm: Percent of failures that become permanent. Default is 20.

    _phases: Number of phases, this line.

    _repair: Hours to repair. Default is 3 hr.
    """

    _basefreq = attr.ib(validator=attr.validators.instance_of((int, float)), default=60)
    _emergamps = attr.ib(validator=attr.validators.instance_of((int, float)), default=600)
    _enabled = attr.ib(validator=attr.validators.instance_of(str), default='true')
    _faultrate = attr.ib(validator=attr.validators.instance_of((int, float)), default=0.1)
    _like = attr.ib(validator=attr.validators.instance_of(str), default='')
    _name = attr.ib(validator=attr.validators.instance_of(str), default='pdelement_' + Utils.generate_random_string(),
                    converter=Utils.remove_blank_spaces)
    _normamps = attr.ib(validator=attr.validators.instance_of((int, float)), default=400)
    _pctperm = attr.ib(validator=attr.validators.instance_of((int, float)), default=20)
    _phases = attr.ib(validator=attr.validators.instance_of((int, float)), default=3)
    _repair = attr.ib(validator=attr.validators.instance_of((int, float)), default=3)

    def __attrs_post_init__(self):
        if self._name != '':
            return
        else:
            self._name = 'my_pdelement_' + Utils.generate_random_string()

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
