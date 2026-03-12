from types import SimpleNamespace
from unittest.mock import ANY, patch

import pytest

from py_dss_toolkit.dss_tools.ConfigurationTools import ConfigurationTools
from py_dss_toolkit.dss_tools.SimulationTools import SimulationTools
from py_dss_toolkit.dss_tools.UtilitiesTools import UtilitiesTools
from py_dss_toolkit.dss_tools.dss_tools import DSSTools


class FakeDSS:
    def __init__(self):
        self.commands = []
        self.dssinterface = SimpleNamespace(datapath=None)

    def text(self, command: str):
        self.commands.append(command)
        return ""


def test_simulation_tools_solve_snapshot_emits_expected_command_sequence():
    dss = FakeDSS()
    tools = SimulationTools(dss)

    tools.solve_snapshot(control_mode="Static", max_iterations=20, max_control_iter=7)

    assert dss.commands == [
        "Set maxiterations=20",
        "Set maxcontroliter=7",
        "set ControlMode=Static",
        "Set Mode=SnapShot",
        "solve",
    ]


def test_simulation_tools_solve_daily_emits_expected_command_sequence():
    dss = FakeDSS()
    tools = SimulationTools(dss)

    tools.solve_daily(stepsize="30m", number=48, control_mode="time", max_iterations=8, max_control_iter=4)

    assert dss.commands == [
        "Set maxiterations=8",
        "Set maxcontroliter=4",
        "set ControlMode=time",
        "Set Mode=daily",
        "Set Stepsize=30m",
        "Set number=48",
        "solve",
    ]


def test_configuration_tools_compile_dss_emits_clearall_then_compile():
    dss = FakeDSS()
    tools = ConfigurationTools(dss)

    tools.compile_dss("my_case.dss")

    assert dss.commands == ["ClearAll", "Compile [my_case.dss]"]


def test_utilities_tools_save_circuit_emits_case_commands_and_sets_datapath():
    dss = FakeDSS()
    tools = UtilitiesTools(dss)

    tools.save_circuit(output_dir="C:/tmp/out", case_name="nightly_case")

    assert dss.dssinterface.datapath == "C:/tmp/out"
    assert dss.commands == [
        "set casename='nightly_case'",
        "save circuit Dir=nightly_case",
    ]


def test_dss_tools_update_dss_refreshes_dependent_objects():
    fake_dss = FakeDSS()
    with patch("py_dss_toolkit.results.Results.Results", autospec=True) as results_cls, patch(
        "py_dss_toolkit.model.ModelBase.ModelBase", autospec=True
    ) as model_cls, patch(
        "py_dss_toolkit.view.static_view.ViewResults.ViewResults", autospec=True
    ) as static_cls, patch(
        "py_dss_toolkit.view.interactive_view.ViewResults.ViewResults", autospec=True
    ) as interactive_cls, patch(
        "py_dss_toolkit.view.dss_view.ViewResults.ViewResults", autospec=True
    ) as dss_view_cls, patch(
        "py_dss_toolkit.dss_tools.dss_tools.SimulationTools", autospec=True
    ) as sim_cls, patch(
        "py_dss_toolkit.dss_tools.dss_tools.ConfigurationTools", autospec=True
    ) as cfg_cls, patch(
        "py_dss_toolkit.dss_tools.dss_tools.UtilitiesTools", autospec=True
    ) as util_cls:
        tools = DSSTools(None)
        tools.update_dss(fake_dss)

        results_cls.assert_called_once_with(fake_dss, ANY)
        model_cls.assert_called_once_with(fake_dss)
        static_cls.assert_called_once_with(fake_dss, results_cls.return_value)
        interactive_cls.assert_called_once_with(fake_dss, results_cls.return_value, model_cls.return_value)
        dss_view_cls.assert_called_once_with(fake_dss)
        sim_cls.assert_called_once_with(fake_dss)
        cfg_cls.assert_called_once_with(fake_dss)
        util_cls.assert_called_once_with(fake_dss)

        assert tools.dss is fake_dss
        assert tools.results is results_cls.return_value
        assert tools.model is model_cls.return_value
        assert tools.static_view is static_cls.return_value
        assert tools.interactive_view is interactive_cls.return_value
        assert tools.dss_view is dss_view_cls.return_value
        assert tools.simulation is sim_cls.return_value
        assert tools.configuration is cfg_cls.return_value
        assert tools.utilities is util_cls.return_value


@pytest.mark.parametrize(
    ("accessor", "args"),
    [
        ("dss", ()),
        ("results", ()),
        ("model", ()),
        ("dss_view", ()),
        ("static_view", ()),
        ("interactive_view", ()),
        ("simulation", ()),
        ("configuration", ()),
        ("utilities", ()),
        ("text", ("solve",)),
    ],
)
def test_dss_tools_requires_update_dss_before_property_access(accessor, args):
    tools = DSSTools(None)

    with pytest.raises(RuntimeError, match="update_dss"):
        value = getattr(tools, accessor)
        if callable(value):
            value(*args)
