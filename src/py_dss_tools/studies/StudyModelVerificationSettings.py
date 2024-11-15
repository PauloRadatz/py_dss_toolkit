# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

from typing import List, Tuple, Union
from dataclasses import dataclass, field, asdict
from py_dss_interface import DSS
from py_dss_tools.studies.StudySettings import StudySettings
import pandas as pd
from py_dss_tools.studies.settings_utils import *


@dataclass(kw_only=True)
class StudyModelVerificationSettings:
    isolated: bool = True
    loads_transformer_voltage: bool = True
    phases_connections: bool = True
    same_bus: bool = True
