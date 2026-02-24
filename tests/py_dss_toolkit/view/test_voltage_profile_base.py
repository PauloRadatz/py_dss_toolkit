from types import SimpleNamespace

import pandas as pd
import pytest

from py_dss_toolkit.view.view_base.VoltageProfileBase import VoltageProfileBase


class FakeCktElement:
    def __init__(self):
        self._element_data = {}
        self._active_element = None
        self.bus_names = []

    @property
    def is_enabled(self):
        if self._active_element is None:
            return False
        return self._element_data[self._active_element]["enabled"]

    def update_from_element(self, element_name, element_data):
        self._active_element = element_name
        self._element_data[element_name] = element_data
        self.bus_names = element_data["bus_names"]


class FakeCircuit:
    def __init__(self, cktelement, element_data):
        self._cktelement = cktelement
        self._element_data = element_data
        self.buses_names = ["SOURCEBUS.1.2.3", "LOADBUS.1.2.3", "OTHERBUS.1.2.3"]
        self.buses_distances = [0.0, 1.2, 2.5]

    def set_active_element(self, element):
        self._cktelement.update_from_element(element, self._element_data[element])


def _build_voltage_profile_base(*, meter_count, meter_names, enabled_meter_elements, element_data):
    cktelement = FakeCktElement()
    circuit = FakeCircuit(cktelement, element_data)
    meters = SimpleNamespace(count=meter_count, names=meter_names)
    dss = SimpleNamespace(meters=meters, circuit=circuit, cktelement=cktelement)

    df = pd.DataFrame(
        {"node1": [1.0, 0.99], "node2": [1.01, 1.0], "node3": [0.98, 0.97]},
        index=["sourcebus", "loadbus"],
    )
    results = SimpleNamespace(voltage_ln_nodes=[df])

    voltage_profile = VoltageProfileBase(dss=dss, results=results)

    meter_element_data = {
        f"energymeter.{name}": {"enabled": enabled, "bus_names": ["sourcebus.1.2.3", "loadbus.1.2.3"]}
        for name, enabled in enabled_meter_elements.items()
    }
    voltage_profile._dss.circuit._element_data.update(meter_element_data)
    return voltage_profile


def test_check_energymeter_raises_when_no_meter_exists():
    voltage_profile = _build_voltage_profile_base(
        meter_count=0,
        meter_names=[],
        enabled_meter_elements={},
        element_data={},
    )

    with pytest.raises(ValueError, match="One enerymeter should exist"):
        voltage_profile._check_energymeter()


def test_check_energymeter_raises_when_none_enabled():
    voltage_profile = _build_voltage_profile_base(
        meter_count=2,
        meter_names=["m1", "m2"],
        enabled_meter_elements={"m1": False, "m2": False},
        element_data={},
    )

    with pytest.raises(ValueError, match="At least one enerymeter should be enabled"):
        voltage_profile._check_energymeter()


def test_check_energymeter_raises_when_more_than_one_enabled():
    voltage_profile = _build_voltage_profile_base(
        meter_count=2,
        meter_names=["m1", "m2"],
        enabled_meter_elements={"m1": True, "m2": True},
        element_data={},
    )

    with pytest.raises(ValueError, match="Only one enerymeter should be enabled"):
        voltage_profile._check_energymeter()


def test_check_energymeter_accepts_single_enabled_meter():
    voltage_profile = _build_voltage_profile_base(
        meter_count=2,
        meter_names=["m1", "m2"],
        enabled_meter_elements={"m1": True, "m2": False},
        element_data={},
    )

    voltage_profile._check_energymeter()


def test_prepare_results_normalizes_buses_and_filters_disabled_sections():
    voltage_profile = _build_voltage_profile_base(
        meter_count=1,
        meter_names=["m1"],
        enabled_meter_elements={"m1": True},
        element_data={
            "line.l1": {"enabled": True, "bus_names": ["SOURCEBUS.1.2.3", "LOADBUS.1.2.3"]},
            "reactor.r1": {"enabled": False, "bus_names": ["LOADBUS.1.2.3", "OTHERBUS.1.2.3"]},
            "load.ld1": {"enabled": True, "bus_names": ["LOADBUS.1.2.3", "OTHERBUS.1.2.3"]},
        },
    )
    voltage_profile._dss.circuit.elements_names = ["line.l1", "reactor.r1", "load.ld1"]

    buses, df, distances, sections = voltage_profile._prepare_results()

    assert buses == ["sourcebus", "loadbus", "otherbus"]
    assert list(df.index) == ["sourcebus", "loadbus"]
    assert distances == [0.0, 1.2, 2.5]
    assert sections == [("sourcebus", "loadbus")]
