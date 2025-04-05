# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : comparing_2_models.py
# @Software: PyCharm

import os
import pathlib
import py_dss_tools

script_path = os.path.dirname(os.path.abspath(__file__))

dss_file = pathlib.Path(script_path).joinpath("../feeders", "13Bus", "IEEE13Nodeckt.dss")
dss_file = r"C:\PauloRadatz\AzureDevOps\model_reduction\p1rhs1_sub\dss_models\impedance\P1R--p1rhs1_1247--p1rdt2397\4-low_voltage\Master.dss"
study = py_dss_tools.CreateStudy.generic(name="Test", dss_file=str(dss_file))

df = study.model.loads_df

df_s = study.model.summary_df


dss_file = r"C:\PauloRadatz\AzureDevOps\model_reduction\p1rhs1_sub\dss_models\impedance\P1R--p1rhs1_1247--p1rdt2397\2-Base_Case_clean\Master.dss"
study = py_dss_tools.CreateStudy.generic(name="Test", dss_file=str(dss_file))
# study.utils.dss_command("New EnergyMeter.M element=Transformer.Sub terminal=1")

df_1 = study.model.loads_df

df_s_1 = study.model.summary_df

print("here")
