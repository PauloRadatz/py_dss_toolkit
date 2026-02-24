from types import SimpleNamespace

import pytest

from py_dss_toolkit.view.view_base.MonitorBase import MonitorBase


def _build_monitor_base(*, names=None, mode=0, vipolar="Yes", ppolar="No", terminal=1):
    names = names or ["monitor_test"]
    monitors = SimpleNamespace(
        names=names,
        mode=mode,
        name=None,
        element="line.my_line",
        terminal=terminal,
    )
    bus = SimpleNamespace(kv_base=12.47)
    cktelement = SimpleNamespace(
        num_phases=3,
        num_conductors=3,
        node_order=[1, 2, 3, 1, 2, 3],
        bus_names=["SourceBus.1.2.3", "LoadBus.1.2.3"],
    )

    class _Circuit:
        def __init__(self):
            self.active_element = None
            self.active_bus = None

        def set_active_element(self, element):
            self.active_element = element

        def set_active_bus(self, bus_name):
            self.active_bus = bus_name

    circuit = _Circuit()

    def text(query):
        if "vipolar" in query:
            return vipolar
        if "ppolar" in query:
            return ppolar
        raise AssertionError(f"Unexpected query: {query}")

    dss = SimpleNamespace(
        monitors=monitors,
        circuit=circuit,
        cktelement=cktelement,
        bus=bus,
        text=text,
    )
    return MonitorBase(dss=dss, results=None)


@pytest.mark.parametrize("vipolar_value", ["Yes", "YES", "TrUe"])
def test_check_v_monitor_accepts_case_insensitive_true_like_values(vipolar_value):
    monitor_base = _build_monitor_base(vipolar=vipolar_value, mode=0)
    monitor_base._check_v_monitor("Monitor_Test")


@pytest.mark.parametrize("vipolar_value", ["No", "FALSE", "nO"])
def test_check_v_monitor_rejects_false_like_values(vipolar_value):
    monitor_base = _build_monitor_base(vipolar=vipolar_value, mode=0)

    with pytest.raises(ValueError, match="Invalid monitor vipolar"):
        monitor_base._check_v_monitor("monitor_test")


def test_check_v_monitor_rejects_invalid_mode():
    monitor_base = _build_monitor_base(vipolar="Yes", mode=1)

    with pytest.raises(ValueError, match="Invalid monitor mode"):
        monitor_base._check_v_monitor("monitor_test")


def test_check_v_monitor_rejects_unknown_monitor():
    monitor_base = _build_monitor_base(names=["another_monitor"])

    with pytest.raises(ValueError, match="is not a monitor"):
        monitor_base._check_v_monitor("monitor_test")


def test_check_p_monitor_rejects_invalid_mode():
    monitor_base = _build_monitor_base(ppolar="No", mode=0)

    with pytest.raises(ValueError, match="Invalid monitor mode"):
        monitor_base._check_p_monitor("monitor_test")


@pytest.mark.parametrize("ppolar_value", ["True", "YES", "yEs"])
def test_check_p_monitor_rejects_true_like_values(ppolar_value):
    monitor_base = _build_monitor_base(ppolar=ppolar_value, mode=1)

    with pytest.raises(ValueError, match="Invalid monitor ppolar"):
        monitor_base._check_p_monitor("monitor_test")


def test_organize_v_results_for_terminal_1_returns_nodes_and_base():
    monitor_base = _build_monitor_base(terminal=1)

    elem_nodes, v_base = monitor_base._organize_v_results("monitor_test")

    assert elem_nodes == [1, 2, 3]
    assert v_base == pytest.approx(12470.0)


def test_organize_v_results_for_terminal_2_returns_nodes_and_base():
    monitor_base = _build_monitor_base(terminal=2)

    elem_nodes, v_base = monitor_base._organize_v_results("monitor_test")

    assert elem_nodes == [1, 2, 3]
    assert v_base == pytest.approx(12470.0)


def test_organize_v_results_invalid_terminal_raises():
    monitor_base = _build_monitor_base(terminal=3)

    with pytest.raises(ValueError, match="terminal=3 not implemented"):
        monitor_base._organize_v_results("monitor_test")


def test_organize_p_results_for_terminal_1_returns_nodes():
    monitor_base = _build_monitor_base(terminal=1)
    elem_nodes = monitor_base._organize_p_results("monitor_test")
    assert elem_nodes == [1, 2, 3]


def test_organize_p_results_for_terminal_2_returns_nodes():
    monitor_base = _build_monitor_base(terminal=2)
    elem_nodes = monitor_base._organize_p_results("monitor_test")
    assert elem_nodes == [1, 2, 3]


def test_organize_p_results_invalid_terminal_raises():
    monitor_base = _build_monitor_base(terminal=3)

    with pytest.raises(ValueError, match="terminal=3 not implemented"):
        monitor_base._organize_p_results("monitor_test")
