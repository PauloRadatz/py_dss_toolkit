from unittest.mock import MagicMock

import pytest

from py_dss_toolkit.results.TimeSeries.Monitor import Monitor


class TestMonitorValueError:
    def test_invalid_name_raises_value_error(self):
        fake_dss = MagicMock()
        fake_dss.monitors.names = ["monitor_a", "monitor_b"]

        monitor = Monitor(fake_dss)
        with pytest.raises(ValueError, match="is not defined in the system"):
            monitor.monitor("nonexistent_monitor")

    def test_valid_name_does_not_raise(self, timeseries_study_13bus):
        timeseries_study_13bus.model.add_line_in_vsource(add_monitors=True)
        timeseries_study_13bus.run()
        df = timeseries_study_13bus.results.monitor("monitor_feeder_head_vi")
        assert not df.empty

    def test_invalid_name_message_contains_available_monitors(self):
        fake_dss = MagicMock()
        fake_dss.monitors.names = ["mon1", "mon2"]

        monitor = Monitor(fake_dss)
        with pytest.raises(ValueError, match="mon1") as exc_info:
            monitor.monitor("bad_name")
        assert "mon2" in str(exc_info.value)

    def test_case_insensitive_match(self):
        fake_dss = MagicMock()
        fake_dss.monitors.names = ["Monitor_A"]

        monitor = Monitor(fake_dss)
        with pytest.raises(ValueError, match="is not defined"):
            monitor.monitor("NONEXISTENT")
