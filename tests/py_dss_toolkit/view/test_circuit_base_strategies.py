from types import SimpleNamespace

import numpy as np
import pandas as pd
import pytest

from py_dss_toolkit.view.interactive_view.SnapShot.Circuit.CircuitBase import CircuitBase


def _empty_vmags():
    return pd.DataFrame(columns=["node1", "node2", "node3"])


def _build_circuit_base():
    dss = SimpleNamespace()
    results = SimpleNamespace(
        powers_elements=[pd.DataFrame(), pd.DataFrame()],
        voltages_elements=[pd.DataFrame(), pd.DataFrame()],
        voltage_ln_nodes=[_empty_vmags(), _empty_vmags()],
        voltage_ll_nodes=[_empty_vmags(), _empty_vmags()],
        voltage_nodes=[_empty_vmags(), _empty_vmags()],
        violation_voltage_ln_nodes=[pd.DataFrame(), pd.DataFrame()],
        violation_voltage_ll_nodes=[pd.DataFrame(), pd.DataFrame()],
        violation_voltage_nodes=[pd.DataFrame(), pd.DataFrame()],
        violation_currents_elements=pd.DataFrame(),
    )
    model = SimpleNamespace(
        lines_df=pd.DataFrame(columns=["name", "bus1", "bus2", "phases", "linetype"]),
        buses_df=pd.DataFrame(columns=["name", "distance"]),
    )
    return CircuitBase(dss=dss, results=results, model=model)


def _sample_vmags_bus_ab():
    return pd.DataFrame(
        {
            "node1": [1.0, 0.98],
            "node2": [1.01, 0.99],
            "node3": [1.0, 0.97],
        },
        index=["a", "b"],
    )


def test_voltage_strategy_uses_nodal_ln_and_bus2_mean():
    circuit = _build_circuit_base()
    circuit._results.voltage_ln_nodes = (_sample_vmags_bus_ab(), _empty_vmags())
    lines_df = pd.DataFrame(
        {
            "name": ["line.l1"],
            "bus1": ["a"],
            "bus2": ["b"],
            "phases": [3],
            "linetype": ["oh"],
        }
    )
    _, results, _, _ = circuit._get_plot_settings("voltage", lines_df=lines_df)
    assert results["line.l1"] == pytest.approx((0.98 + 0.99 + 0.97) / 3.0)


def test_voltage_strategy_ln_ll_switch():
    circuit = _build_circuit_base()
    ln_df = _sample_vmags_bus_ab()
    ll_df = pd.DataFrame(
        {"node1": [2.0, 2.1], "node2": [2.0, 2.0], "node3": [2.0, 2.2]},
        index=["a", "b"],
    )
    circuit._results.voltage_ln_nodes = (ln_df, _empty_vmags())
    circuit._results.voltage_ll_nodes = (ll_df, _empty_vmags())
    lines_df = pd.DataFrame(
        {
            "name": ["line.l1"],
            "bus1": ["a"],
            "bus2": ["b"],
            "phases": [3],
            "linetype": ["oh"],
        }
    )
    circuit.voltage_settings.voltage_type = "ll"
    _, results, _, _ = circuit._get_plot_settings("voltage", lines_df=lines_df)
    assert results["line.l1"] == pytest.approx((2.1 + 2.0 + 2.2) / 3.0)


def test_voltage_violations_strategy_follows_voltage_type():
    circuit = _build_circuit_base()
    lines_df = pd.DataFrame(
        {
            "name": ["line.l1", "line.l2", "line.l3"],
            "bus1": ["x", "y", "z"],
            "bus2": ["a", "b", "c"],
            "phases": [3, 3, 3],
            "linetype": ["oh", "oh", "oh"],
        }
    )
    circuit._results.violation_voltage_ln_nodes = (pd.DataFrame(index=["x"]), pd.DataFrame())
    circuit._results.violation_voltage_ll_nodes = (pd.DataFrame(index=["y"]), pd.DataFrame())
    circuit._results.violation_voltage_nodes = (pd.DataFrame(index=["z"]), pd.DataFrame())

    circuit.voltage_settings.voltage_type = "ln"
    _, res_ln, _, _ = circuit._get_plot_settings("voltage violations", lines_df=lines_df.copy())
    assert res_ln["line.l1"] == "1"
    assert res_ln["line.l2"] == "0"
    assert res_ln["line.l3"] == "0"

    circuit.voltage_settings.voltage_type = "ll"
    _, res_ll, _, _ = circuit._get_plot_settings("voltage violations", lines_df=lines_df.copy())
    assert res_ll["line.l1"] == "0"
    assert res_ll["line.l2"] == "1"
    assert res_ll["line.l3"] == "0"

    circuit.voltage_settings.voltage_type = "ln-ll"
    _, res_sm, _, _ = circuit._get_plot_settings("voltage violations", lines_df=lines_df.copy())
    assert res_sm["line.l1"] == "0"
    assert res_sm["line.l2"] == "0"
    assert res_sm["line.l3"] == "1"


def test_get_plot_settings_raises_for_unknown_parameter():
    circuit = _build_circuit_base()

    with pytest.raises(ValueError, match="Unknown parameter"):
        circuit._get_plot_settings("not supported")


def test_user_numerical_defined_strategy_raises_when_results_not_set():
    circuit = _build_circuit_base()
    circuit.user_numerical_defined_settings.results = None

    with pytest.raises(ValueError, match="No results found for 'user numerical defined' parameter"):
        circuit._get_plot_settings("user numerical defined")


def test_user_categorical_defined_strategy_raises_when_results_not_set():
    circuit = _build_circuit_base()
    circuit.user_categorical_defined_settings.results = None

    with pytest.raises(ValueError, match="No results found for 'user categorical defined' parameter"):
        circuit._get_plot_settings("user categorical defined")


def test_get_phase_width_covers_all_phase_branches():
    circuit = _build_circuit_base()
    num_phases = pd.Series({"line.3ph": 3, "line.2ph": 2, "line.1ph": 1})

    assert circuit._get_phase_width("line.3ph", num_phases, 1, 2, 3) == 3
    assert circuit._get_phase_width("line.2ph", num_phases, 1, 2, 3) == 2
    assert circuit._get_phase_width("line.1ph", num_phases, 1, 2, 3) == 1


def test_get_dash_prefers_phase_styles_then_line_type_then_default():
    circuit = _build_circuit_base()
    num_phases = pd.Series({"line.a": 3, "line.b": 2, "line.c": 1, "line.d": 1, "line.e": 1})
    line_type = pd.Series({"line.a": "ug", "line.b": "oh", "line.c": "oh", "line.d": "ug", "line.e": "x"})

    assert circuit._get_dash("line.a", num_phases, None, None, "dot", line_type, "dash", "longdash") == "dot"
    assert circuit._get_dash("line.b", num_phases, None, "dashdot", None, line_type, "dash", "longdash") == "dashdot"
    assert circuit._get_dash("line.c", num_phases, None, None, None, line_type, "dash", "longdash") == "dash"
    assert circuit._get_dash("line.d", num_phases, None, None, None, line_type, "dash", "longdash") == "longdash"
    assert circuit._get_dash("line.e", num_phases, None, None, None, line_type, None, None) == "solid"


def test_calculate_colorbar_range_uses_data_or_explicit_limits():
    circuit = _build_circuit_base()
    result_values = np.array([0.5, 1.2, 3.4])

    auto_settings = SimpleNamespace(colorbar_cmin=None, colorbar_cmax=None)
    cmin, cmax = circuit._calculate_colorbar_range(auto_settings, result_values)
    assert cmin == pytest.approx(0.5)
    assert cmax == pytest.approx(3.4)

    fixed_settings = SimpleNamespace(colorbar_cmin=0.0, colorbar_cmax=5.0)
    cmin, cmax = circuit._calculate_colorbar_range(fixed_settings, result_values)
    assert cmin == 0.0
    assert cmax == 5.0


def test_calculate_colorbar_ticks_from_count_and_decimal_points():
    circuit = _build_circuit_base()
    result_values = np.array([0.0, 0.5, 1.0])
    settings = SimpleNamespace(
        colorbar_tickvals=3,
        colorbar_ticktext_decimal_points=2,
        colorbar_tickvals_list=None,
    )

    tickvals, ticktext = circuit._calculate_colorbar_ticks(settings, result_values)

    assert np.allclose(tickvals, np.array([0.0, 0.5, 1.0]))
    assert ticktext == ["0.00", "0.50", "1.00"]


def test_calculate_colorbar_ticks_list_overrides_generated_ticks():
    circuit = _build_circuit_base()
    result_values = np.array([0.0, 1.0])
    settings = SimpleNamespace(
        colorbar_tickvals=4,
        colorbar_ticktext_decimal_points=1,
        colorbar_tickvals_list=[0.2, 0.8],
    )

    tickvals, ticktext = circuit._calculate_colorbar_ticks(settings, result_values)

    assert tickvals == [0.2, 0.8]
    assert ticktext == [0.2, 0.8]
