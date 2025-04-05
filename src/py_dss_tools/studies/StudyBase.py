# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

from dataclasses import dataclass, field
from typing import Union, Optional

from py_dss_interface import DSS

from py_dss_tools.model.ModelBase import ModelBase
from py_dss_tools.utils import Utils


@dataclass(kw_only=True)
class StudyBase:
    """
    Represents a study configuration with OpenDSS interface integration.
    """
    _name: str = field(default=f"scenario_{Utils.generate_random_string()}", init=True, repr=True)
    _dss_file: str = field(init=True, repr=True)
    _base_frequency: Union[int, float] = field(default=60, init=True)
    _dss_dll: str = field(default=None, init=True)

    def __post_init__(self):
        """
        Post-initialization of the StudyBase class. Compiles the DSS file and initializes required elements.
        """
        self._dss = self._initialize_dss(self._dss_dll, self._dss_file)
        self._name = Utils.remove_blank_spaces(self._name)
        self._model = ModelBase(self._dss)

    @staticmethod
    def _initialize_dss(dll: Optional[str], dss_file: str) -> DSS:
        """
        Initializes and returns a DSS instance.

        Args:
            dll (Optional[str]): Path to the DSS DLL, if provided.
            dss_file (str): File path to the DSS input file.

        Returns:
            DSS: Initialized Direct DSS object.
        """
        dss_instance = DSS(dll) if dll else DSS()
        dss_instance.text(f"compile [{dss_file}]")
        return dss_instance

    @property
    def name(self) -> str:
        """
        Getter for the study name.

        Returns:
            str: The name of the study.
        """
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """
        Setter for the study name.

        Args:
            value (str): The desired new name for the study.
        """
        self._name = value

    @property
    def dss(self) -> DSS:
        """
        Getter for the DSS instance.

        Returns:
            DSS: The DSS instance.
        """
        return self._dss

    @property
    def model(self) -> ModelBase:
        """
        Getter for the model base.

        Returns:
            ModelBase: The model associated with the DSS instance.
        """
        return self._model
