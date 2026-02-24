import matplotlib.pyplot as plt
import plotly.graph_objects as go


def test_static_voltage_profile_smoke(snapshot_study_13bus):
    snapshot_study_13bus.model.add_line_in_vsource(add_meter=True)
    snapshot_study_13bus.run()

    fig, ax = snapshot_study_13bus.static_view.voltage_profile(
        show=False,
        show_voltage_limits=False,
    )

    assert fig is not None
    assert ax is not None
    plt.close(fig)


def test_interactive_circuit_plot_smoke(snapshot_study_13bus):
    snapshot_study_13bus.model.add_line_in_vsource(add_meter=True)
    snapshot_study_13bus.run()

    fig = snapshot_study_13bus.interactive_view.circuit_plot(
        parameter="phases",
        show=False,
        mark_buses=False,
        show_colorbar=False,
    )

    assert isinstance(fig, go.Figure)
    assert len(fig.data) > 0
