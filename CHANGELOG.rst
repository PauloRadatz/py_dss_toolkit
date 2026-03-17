Changelog
=========

0.13.0 (unreleased)
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
