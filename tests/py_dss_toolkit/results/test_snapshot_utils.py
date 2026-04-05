import numpy as np
import pandas as pd
import pytest
from py_dss_toolkit.results.SnapShot.snapshot_utils import (
    create_terminal_list,
    dataframe_to_column_records,
    set_violation_current_limit_type,
    get_violation_current_limit_type,
)


class TestCreateTerminalList:
    def test_single_terminal(self):
        nodes = [1, 2, 3]
        result = create_terminal_list(nodes, num_terminals=1)
        assert result == ["Terminal1.1", "Terminal1.2", "Terminal1.3"]

    def test_two_terminals(self):
        nodes = [1, 2, 3, 1, 2, 3]
        result = create_terminal_list(nodes, num_terminals=2)
        assert result == [
            "Terminal1.1", "Terminal1.2", "Terminal1.3",
            "Terminal2.1", "Terminal2.2", "Terminal2.3",
        ]

    def test_three_terminals(self):
        nodes = [1, 2, 1, 2, 1, 2]
        result = create_terminal_list(nodes, num_terminals=3)
        assert result == [
            "Terminal1.1", "Terminal1.2",
            "Terminal2.1", "Terminal2.2",
            "Terminal3.1", "Terminal3.2",
        ]

    def test_empty_nodes(self):
        assert create_terminal_list([], num_terminals=1) == []


class TestViolationCurrentLimitType:
    def setup_method(self):
        set_violation_current_limit_type("norm_amps")

    def test_default_is_norm_amps(self):
        assert get_violation_current_limit_type() == "norm_amps"

    def test_set_emerg_amps(self):
        set_violation_current_limit_type("emerg_amps")
        assert get_violation_current_limit_type() == "emerg_amps"

    def test_set_norm_amps_explicitly(self):
        set_violation_current_limit_type("emerg_amps")
        set_violation_current_limit_type("norm_amps")
        assert get_violation_current_limit_type() == "norm_amps"

    def test_invalid_limit_type_raises(self):
        with pytest.raises(ValueError, match="limit_type must be"):
            set_violation_current_limit_type("invalid_type")


class TestDataframeToColumnRecords:
    def test_empty_dataframe(self):
        assert dataframe_to_column_records(pd.DataFrame()) == {}

    def test_named_index_and_numeric_columns(self):
        df = pd.DataFrame({"a": [1.0, 2.0], "b": [3, 4]}, index=pd.Index(["x", "y"], name="bus"))
        rec = dataframe_to_column_records(df)
        assert rec["bus"] == ["x", "y"]
        assert rec["a"] == [1.0, 2.0]
        assert rec["b"] == [3, 4]

    def test_numpy_scalar_becomes_python(self):
        df = pd.DataFrame({"v": [np.float64(1.25)]}, index=["n1"])
        rec = dataframe_to_column_records(df)
        assert isinstance(rec["v"][0], float)
        assert rec["v"][0] == 1.25

    def test_nan_becomes_none(self):
        df = pd.DataFrame({"v": [float("nan")]})
        rec = dataframe_to_column_records(df)
        assert rec["v"][0] is None
