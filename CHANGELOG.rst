Changelog
=========

0.20.0 (2026-07-29)
-------------------
* ``CreateStudy``: Added ``bdgd2opendss_yearly_model`` static factory method for initializing ``BDGD2OpenDSSYearlyModel`` study instances.

0.19.0 (2026-07-14)
-------------------
* Studies: Replaced annual energy calibration with a highly accurate month-by-month ``execute_monthly_energy_case`` iteration, optimized OpenDSS loadshape compilation by utilizing binary ``.sng`` arrays directly, and enhanced stability with embedded solver configuration and DSS engine cleanups.

0.18.0 (2026-07-13)
-------------------
* Studies: Refactored ``BDGD2OpenDSSYearlyModel`` to use a dataclass and an active ``DSS`` instance, removed the ``include_generators`` flag, and updated the master writer to gracefully exclude commented-out GD redirects.

0.17.0 (2026-04-06)
-------------------
* Model: ``ModelQueries.load_to_transformer_df`` and ``_load_to_transformer_records`` list every enabled load with its feeding transformer from the graph node attribute (same values as ``feeding_transformer``; all loads, unlike ``model_verification.loads_transformer_voltage_df`` which is kV-mismatch-only).

0.16.0 (2026-04-05)
-------------------
* ``ConfigurationTools.circuit_readiness()`` reports whether the active circuit has elements (``ready``, ``code``, ``message``); empty circuits return ``code="no_elements"``.
* ``SimulationTools.snapshot_solve_status()`` returns snapshot solve flags: ``converged``, ``control_iterations``, ``max_control_iterations``, and ``control_iteration_limit_hit``.
* SnapShot: ``snapshot_utils.dataframe_to_column_records()`` converts a DataFrame (including a named index) to column-oriented dicts suitable for JSON (``NaN`` → ``None``, NumPy scalars normalized to Python values).
* SnapShot results expose private ``_*_records`` helpers built on that helper: ``CurrentsLoading._current_loading_percent_records``, ``CurrentsViolations._violation_currents_elements_records``, ``VoltagesNodalSmart._voltage_mag_smart_nodes_records`` / ``_voltage_ang_smart_nodes_records``, and ``VoltagesNodalViolations._violation_voltage_ln_nodes_records``, ``_violation_voltage_ll_nodes_records``, ``_violation_voltage_nodes_records`` (each violation group returns ``undervoltage`` / ``overvoltage`` column records).

0.15.0 (2026-03-25)
-------------------
* Interactive circuit plots (``circuit_plot`` / ``circuit_geoplot``): ``VoltageSettings.voltage_type`` (``"ln"``, ``"ll"``, or ``"ln-ll"``) selects nodal magnitudes like the voltage profile; per-line values use mean/min/max over ``node1``–``node3`` at the chosen ``bus1``/``bus2``. Voltage violation coloring uses the matching ``violation_voltage_*`` results based on the same setting.

0.14.0 (2026-03-25)
-------------------
* Nodal voltage violations: ``violation_voltage_ll_nodes`` applies the same per-unit limits as ``violation_voltage_ln_nodes`` to line-to-line nodal magnitudes (from ``create_nodal_ll_voltage_dataframes``).
* Nodal voltage violations: ``violation_voltage_nodes`` uses the same per-bus LN/LL selection as ``VoltagesNodalSmart.voltage_nodes`` (via ``create_nodal_smart_voltage_dataframes``); violation checks use numeric columns only so the ``voltage_type`` column is not compared to limits.
* ``VoltagesNodalViolations`` accepts an optional ``connection_type_map`` (dict or callable), aligned with ``VoltagesNodalSmart``; ``Results``, ``SnapShotPowerFlowResults``, and ``TimeSeriesPowerFlowResults`` pass it through so ``dss_tools.results`` stays consistent with ``bus_connection_type_map``.
* ``dss_tools.dss_view`` raises ``RuntimeError`` when ``dss.backend`` is not ``Windows-Delphi`` (DSSView.exe requires the Delphi OpenDSS build).

0.13.0 (2026-03-18)
-------------------
* ``dss_tools`` now raises a descriptive error telling the user to call ``dss_tools.update_dss(dss)`` before accessing lazy properties or calling ``text()`` without a connected DSS instance.
* Model verification tests reorganized by feature: ``test_isolated``, ``test_nodes_connections``, ``test_loop_edges``, ``test_loads_transformer_voltage``, ``test_reversed_segments``, ``test_same_buses_segments``, ``test_disabled_segments``.
* ``meshed_edges_df`` renamed to ``loop_edges_df`` (aligns with OpenDSS "Show Loops" terminology).
* ``voltage_nodes`` now includes a ``voltage_type`` column ('ln' or 'll') indicating the voltage reference used per bus.
* Added ``PCElementsDF`` and ``PDElementsDF`` for PC/PD element DataFrames.
* Graph capabilities: ``CircuitGraph``, ``GraphBuilder`` for topology analysis.
* Loading currents fixed for terminal 2 and 3 of transformers.
* Fixed 13bus example and updated expected test outputs.
* Voltage profile plots: added ``voltage_type`` parameter (``"ln"``, ``"ll"``, ``"ln-ll"``) to ``StaticVoltageProfile.voltage_profile()`` and ``InteractiveVoltageProfile.voltage_profile()``. ``"ln"`` uses line-to-neutral, ``"ll"`` uses line-to-line, ``"ln-ll"`` uses smart per-bus selection via ``VoltagesNodalSmart``.

0.12.0 (2026-02-27)
-------------------
* ``user_numerical_defined_settings.results`` and ``user_categorical_defined_settings.results`` now require a pandas Series (not DataFrame); raises descriptive error if DataFrame is passed.

0.11.0 (2026-02-27)
-------------------
* Added Losses results: ``losses_elements`` returns total active and reactive losses per PD element (kW, kvar).
* Added AllLosses results: ``all_losses_elements`` returns total, load, and no-load losses per PD element using ``cktelement.all_losses``.
* Added unit tests for losses_elements and all_losses_elements.

0.10.0 (2026-02-26)
-------------------
* Relaxed dependency constraints to improve compatibility in Google Colab environments.

0.9.0 (2026-02-26)
------------------
* Performance improvements across model, results, and view modules

0.8.0 (2026-02-24)
------------------
* Fixed bug in monitor plotting.
* Added more unit tests and test reorganization (model, results, studies, view)
* Allow user to access dss via dss_tools.dss.
* Interactive view / plot style updates

0.7.0 (2026-02-23)
------------------
Updating to work with py-dss-interface 2.3.0

0.6.0 (2025-10-16)
------------------
* segments_df includes nodes and enabled.

* monitor can plot voltage in pu when connected to element's terminal 2

0.5.0 (2025-09-24)
------------------
* Returns fig and ax objects in the static_view plots.

* Raise an error when there is no Monitor for the results.monitor

0.4.0 (2025-08-20)
------------------
* Added Voltage LL Nodes results. Code provided by Wes

0.0.0 (2021-05-18)
------------------

* First release on PyPI.
