import pytest
from py_dss_toolkit import CreateStudy
import py_dss_interface
from py_dss_toolkit import dss_tools
import os
import pathlib

script_path = os.path.dirname(os.path.abspath(__file__))
dss_file_13bus = pathlib.Path(script_path).joinpath("cases", "13Bus", "IEEE13Nodeckt.dss")

@pytest.fixture(scope="function")
def snapshot_study_13bus():
    study = CreateStudy.snapshot("My Study", dss_file=dss_file_13bus)

    return study

@pytest.fixture(scope="function")
def timeseries_study_13bus():

    study = CreateStudy.timeseries("My Study", dss_file=dss_file_13bus)

    return study

@pytest.fixture(scope="function")
def dss_tools_13bus():
    dss = py_dss_interface.DSS()
    dss_tools.update_dss(dss)
    dss_tools.configuration.compile_dss(dss_file_13bus)

    return dss
