import matplotlib.pyplot as plt
import plotly.graph_objects as go


def _prepare_timeseries_monitor_data(timeseries_study_13bus):
    timeseries_study_13bus.model.add_line_in_vsource(add_monitors=True)
    timeseries_study_13bus.run()


def test_interactive_monitor_vmag_vs_time_smoke(timeseries_study_13bus):
    _prepare_timeseries_monitor_data(timeseries_study_13bus)

    fig = timeseries_study_13bus.interactive_view.vmag_vs_time(
        "monitor_feeder_head_vi",
        show=False,
    )

    assert isinstance(fig, go.Figure)
    assert len(fig.data) > 0


def test_interactive_monitor_p_vs_time_smoke(timeseries_study_13bus):
    _prepare_timeseries_monitor_data(timeseries_study_13bus)

    fig = timeseries_study_13bus.interactive_view.p_vs_time(
        "monitor_feeder_head_pq",
        show=False,
    )

    assert isinstance(fig, go.Figure)
    assert len(fig.data) > 0


def test_static_monitor_vmag_vs_time_smoke(timeseries_study_13bus):
    _prepare_timeseries_monitor_data(timeseries_study_13bus)

    fig, ax = timeseries_study_13bus.static_view.vmag_vs_time(
        "monitor_feeder_head_vi",
        show=False,
    )

    assert fig is not None
    assert ax is not None
    plt.close(fig)
