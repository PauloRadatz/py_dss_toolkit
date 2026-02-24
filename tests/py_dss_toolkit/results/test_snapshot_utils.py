import pytest
from py_dss_toolkit.results.SnapShot.snapshot_utils import (
    create_terminal_list,
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
        with pytest.raises(AssertionError, match="limit_type must be"):
            set_violation_current_limit_type("invalid_type")
