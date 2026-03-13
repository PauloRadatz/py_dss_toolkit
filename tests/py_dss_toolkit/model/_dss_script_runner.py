import py_dss_interface

from py_dss_toolkit import dss_tools


def run_dss_script(script: str):
    """Run DSS script string via dss.text() and return DSS instance."""
    dss = py_dss_interface.DSS()
    dss_tools.update_dss(dss)
    dss_tools.text(script.strip())
    return dss

