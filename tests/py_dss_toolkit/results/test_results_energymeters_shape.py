import pandas as pd
from pandas.testing import assert_frame_equal

from py_dss_toolkit.results.TimeSeries.Energymeters import Energymeters


class _FakeMeters:
    def __init__(self, entries, register_names):
        self._entries = entries
        self._register_names = register_names
        self._index = 0

    @property
    def count(self):
        return len(self._entries)

    def first(self):
        self._index = 0
        return 1 if self._entries else 0

    def next(self):
        if self._index < len(self._entries) - 1:
            self._index += 1
            return self._index + 1
        return 0

    @property
    def name(self):
        return self._entries[self._index]["name"]

    @property
    def register_names(self):
        return self._register_names

    @property
    def register_values(self):
        return self._entries[self._index]["register_values"]


class _FakeCktElement:
    def __init__(self, meters: _FakeMeters):
        self._meters = meters

    @property
    def is_enabled(self):
        return self._meters._entries[self._meters._index]["enabled"]


class _FakeDss:
    def __init__(self, entries, register_names):
        self.meters = _FakeMeters(entries=entries, register_names=register_names)
        self.cktelement = _FakeCktElement(self.meters)


def test_energymeters_skips_disabled_meters_without_column_misalignment():
    dss = _FakeDss(
        entries=[
            {"name": "MeterA", "enabled": True, "register_values": [1.0, 10.0]},
            {"name": "MeterB", "enabled": False, "register_values": [2.0, 20.0]},
            {"name": "MeterC", "enabled": True, "register_values": [3.0, 30.0]},
        ],
        register_names=["Reg1", "Reg2"],
    )

    result = Energymeters(dss).energymeters

    expected = pd.DataFrame(
        [
            {"name": "metera", "reg1": 1.0, "reg2": 10.0},
            {"name": "meterc", "reg1": 3.0, "reg2": 30.0},
        ]
    )
    assert_frame_equal(result, expected)
