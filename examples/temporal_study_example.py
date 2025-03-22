# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : temporal_study_example.py
# @Software: PyCharm

import os
import pathlib
import py_dss_tools

script_path = os.path.dirname(os.path.abspath(__file__))

dss_file = pathlib.Path(script_path).joinpath("feeders", "13Bus", "IEEE13Nodeckt.dss")

study = py_dss_tools.CreateStudy.timeseries(name="Test", dss_file=str(dss_file))

study.dss.text("New EnergyMeter.M element=Transformer.Sub terminal=1")
study.dss.text("New monitor.M1 element=Line.692675 terminal=1")
study.dss.text("New monitor.M1_p element=Line.692675 terminal=1 mode=1 ppolar=no")
study.dss.text("batchedit load..* daily=default")

study.settings.mode = "daily"
study.run()

study.results.monitor("m1")
study.dss_view.vmag_vs_time("m1")
study.dss_view.p_vs_time("m1_p")

print(study.results.energymeters)


