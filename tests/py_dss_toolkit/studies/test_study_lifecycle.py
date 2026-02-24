from unittest.mock import patch


def test_snapshot_run_validates_settings_and_solves(snapshot_study_13bus):
    with patch.object(
        snapshot_study_13bus.settings,
        "validate_settings",
        wraps=snapshot_study_13bus.settings.validate_settings,
    ) as validate_spy, patch.object(
        snapshot_study_13bus.dss,
        "text",
        wraps=snapshot_study_13bus.dss.text,
    ) as text_spy:
        snapshot_study_13bus.run()

    validate_spy.assert_called_once()
    assert any(call.args[0] == "solve" for call in text_spy.call_args_list)


def test_timeseries_run_resets_meter_elements_when_enabled(timeseries_study_13bus):
    timeseries_study_13bus.reset_monitors_energymeters = True
    with patch.object(timeseries_study_13bus.dss.monitors, "reset_all") as monitor_reset, patch.object(
        timeseries_study_13bus.dss.meters, "reset_all"
    ) as meter_reset, patch.object(
        timeseries_study_13bus.dss,
        "text",
        wraps=timeseries_study_13bus.dss.text,
    ) as text_spy:
        timeseries_study_13bus.run()

    monitor_reset.assert_called_once()
    meter_reset.assert_called_once()
    assert any(call.args[0] == "solve" for call in text_spy.call_args_list)


def test_timeseries_run_does_not_reset_meter_elements_when_disabled(timeseries_study_13bus):
    timeseries_study_13bus.reset_monitors_energymeters = False
    with patch.object(timeseries_study_13bus.dss.monitors, "reset_all") as monitor_reset, patch.object(
        timeseries_study_13bus.dss.meters, "reset_all"
    ) as meter_reset, patch.object(
        timeseries_study_13bus.dss,
        "text",
        wraps=timeseries_study_13bus.dss.text,
    ) as text_spy:
        timeseries_study_13bus.run()

    monitor_reset.assert_not_called()
    meter_reset.assert_not_called()
    assert any(call.args[0] == "solve" for call in text_spy.call_args_list)


def test_timeseries_run_one_step_restores_original_time_and_number(timeseries_study_13bus):
    timeseries_study_13bus.settings.time = (3, 0)
    timeseries_study_13bus.settings.number = 7
    original_time = timeseries_study_13bus.settings.time
    original_number = timeseries_study_13bus.settings.number
    with patch.object(
        timeseries_study_13bus.dss,
        "text",
        wraps=timeseries_study_13bus.dss.text,
    ) as text_spy:
        timeseries_study_13bus.run_one_step((10, 15))

    assert timeseries_study_13bus.settings.time == original_time
    assert timeseries_study_13bus.settings.number == original_number
    assert any(call.args[0] == "solve" for call in text_spy.call_args_list)
