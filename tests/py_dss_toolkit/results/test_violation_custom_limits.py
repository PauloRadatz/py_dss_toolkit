class TestCustomVoltageLimits:
    def test_wider_limits_produce_fewer_violations(self, snapshot_study_13bus):
        snapshot_study_13bus.run()
        results = snapshot_study_13bus.results

        results.set_violation_voltage_ln_limits(v_min_pu=0.95, v_max_pu=1.05)
        under_default, over_default = results.violation_voltage_ln_nodes

        results.set_violation_voltage_ln_limits(v_min_pu=0.80, v_max_pu=1.20)
        under_wide, over_wide = results.violation_voltage_ln_nodes

        assert len(under_wide) <= len(under_default)
        assert len(over_wide) <= len(over_default)

    def test_tighter_limits_produce_more_violations(self, snapshot_study_13bus):
        snapshot_study_13bus.run()
        results = snapshot_study_13bus.results

        results.set_violation_voltage_ln_limits(v_min_pu=0.95, v_max_pu=1.05)
        under_default, over_default = results.violation_voltage_ln_nodes

        results.set_violation_voltage_ln_limits(v_min_pu=0.999, v_max_pu=1.001)
        under_tight, over_tight = results.violation_voltage_ln_nodes

        assert len(under_tight) >= len(under_default)
        assert len(over_tight) >= len(over_default)

    def test_limits_are_stored_correctly(self, snapshot_study_13bus):
        results = snapshot_study_13bus.results
        results.set_violation_voltage_ln_limits(v_min_pu=0.90, v_max_pu=1.10)
        assert results.v_min_pu == 0.90
        assert results.v_max_pu == 1.10


class TestCustomCurrentLoadingThreshold:
    def test_higher_threshold_produces_fewer_violations(self, snapshot_study_13bus):
        snapshot_study_13bus.run()
        results = snapshot_study_13bus.results

        results.set_currents_loading_threshold_percent(threshold_percent=100.0)
        violations_100 = results.violation_currents_elements

        results.set_currents_loading_threshold_percent(threshold_percent=1000.0)
        violations_1000 = results.violation_currents_elements

        assert len(violations_1000) <= len(violations_100)

    def test_zero_threshold_includes_all_elements(self, snapshot_study_13bus):
        snapshot_study_13bus.run()
        results = snapshot_study_13bus.results

        results.set_currents_loading_threshold_percent(threshold_percent=0.0)
        violations_zero = results.violation_currents_elements
        assert len(violations_zero) > 0

    def test_threshold_is_stored_correctly(self, snapshot_study_13bus):
        results = snapshot_study_13bus.results
        results.set_currents_loading_threshold_percent(threshold_percent=75.0)
        assert results.threshold_percent == 75.0
