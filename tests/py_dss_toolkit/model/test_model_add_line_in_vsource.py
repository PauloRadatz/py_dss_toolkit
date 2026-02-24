from py_dss_toolkit import dss_tools
import pytest

def test_dss_tools_add_line_in_vsource_creates_line(dss_tools_13bus):
    dss = dss_tools_13bus
    dss_tools.model.add_line_in_vsource()

    line_names = dss.lines.names
    assert "feeder_head" in [name.lower() for name in line_names], "Line.feeder_head was not created"

def test_dss_tools_add_line_in_vsource_creates_line_with_existing_energymeter(dss_tools_13bus):
    dss = dss_tools_13bus
    dss_tools.text("New energymeter.EM2 element=Line.670671")
    dss_tools.model.add_line_in_vsource()


    num_meter = dss_tools.model.meters_df.shape[0]
    assert num_meter == 1

@pytest.mark.parametrize(
    "study_fixture_name",
    [
        "snapshot_study_13bus",
        "timeseries_study_13bus",
    ]
)
def test_add_line_in_vsource_creates_line(request, study_fixture_name):
    study = request.getfixturevalue(study_fixture_name)
    study.model.add_line_in_vsource()

    line_names = study.dss.lines.names
    assert "feeder_head" in [name.lower() for name in line_names], "Line.feeder_head was not created"


def test_add_line_in_vsource_creates_meter(snapshot_study_13bus):
    snapshot_study_13bus.model.add_line_in_vsource(add_meter=True)

    meter_names = snapshot_study_13bus.dss.meters.names
    assert any("meter_feeder_head" in name.lower() for name in meter_names), \
        "meter_feeder_head was not created"


def test_add_line_in_vsource_creates_monitors(snapshot_study_13bus):
    snapshot_study_13bus.model.add_line_in_vsource(add_monitors=True)

    monitor_names = snapshot_study_13bus.dss.monitors.names
    expected_monitors = ["monitor_feeder_head_pq", "monitor_feeder_head_vi"]

    for name in expected_monitors:
        assert any(name in m.lower() for m in monitor_names), f"{name} was not created"

def test_add_line_in_vsource_preserves_bus_coordinates(snapshot_study_13bus):
    # Save original x/y
    snapshot_study_13bus.dss.vsources.name = "source"
    bus_name = snapshot_study_13bus.dss.cktelement.bus_names[0].split('.')[0].lower()
    snapshot_study_13bus.dss.circuit.set_active_bus(bus_name)
    x_original = snapshot_study_13bus.dss.bus.x
    y_original = snapshot_study_13bus.dss.bus.y

    snapshot_study_13bus.model.add_line_in_vsource()

    unreal_bus = f"{bus_name}_unrealbus"
    snapshot_study_13bus.dss.circuit.set_active_bus(unreal_bus)
    x_new = snapshot_study_13bus.dss.bus.x
    y_new = snapshot_study_13bus.dss.bus.y

    assert x_new == x_original and y_new == y_original, "Bus coordinates were not preserved"

def test_add_line_in_vsource_is_idempotent(snapshot_study_13bus):
    snapshot_study_13bus.model.add_line_in_vsource()
    initial_lines = set(snapshot_study_13bus.dss.lines.names)

    # Call again
    snapshot_study_13bus.model.add_line_in_vsource()
    lines_after = set(snapshot_study_13bus.dss.lines.names)

    assert initial_lines == lines_after, "Function should not recreate line if it already exists"
