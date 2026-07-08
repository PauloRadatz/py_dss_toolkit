# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

"""Global ``dss_tools`` facade: model, results, simulation, and views for OpenDSS.

The exported singleton ``dss_tools`` is a :class:`DSSTools` instance with no DSS
until you call ``dss_tools.update_dss(dss)`` with ``py_dss_interface.DSS()``.
"""

from typing import TYPE_CHECKING
from typing import Optional

from py_dss_interface import DSS

from py_dss_toolkit.dss_tools.ConfigurationTools import ConfigurationTools
from py_dss_toolkit.dss_tools.SimulationTools import SimulationTools
from py_dss_toolkit.dss_tools.UtilitiesTools import UtilitiesTools

if TYPE_CHECKING:
    from py_dss_toolkit.model.ModelBase import ModelBase
    from py_dss_toolkit.model_verification.ModelVerification import ModelVerification
    from py_dss_toolkit.results.Results import Results
    from py_dss_toolkit.view.dss_view.ViewResults import ViewResults as DSSView
    from py_dss_toolkit.view.interactive_view.ViewResults import ViewResults as InteractiveView
    from py_dss_toolkit.view.static_view.ViewResults import ViewResults as StaticView


class DSSTools:
    """Single entry point to py-dss-toolkit for one OpenDSS engine instance.

    Use :meth:`update_dss` to attach ``py_dss_interface.DSS``. Then access:

    * **model** — element and bus data as DataFrames, plus the circuit graph.
    * **results** — snapshot, time-series, and fault outputs after solves.
    * **simulation** — run power flow and related commands.
    * **static_view** / **interactive_view** — Matplotlib and Plotly plots.
    * **dss_view** — DSSView.exe-based plots (requires ``dss.backend == "Windows-Delphi"``).
    * **model_verification** — topology checks (e.g. islands, loops).
    * **configuration** / **utilities** — helpers for settings and misc tasks.

    The module attribute ``dss_tools`` is created with ``dss=None``. Until
    :meth:`update_dss` is called, :attr:`dss`, :meth:`text`, and all other
    public accessors raise ``RuntimeError``.

    Example::

        from py_dss_interface import DSS
        from py_dss_toolkit import dss_tools

        dss = DSS()
        dss_tools.update_dss(dss)
        dss_tools.text("compile [path/to/master.dss]")
        dss_tools.simulation.solve_snapshot()
        vmags, vangs = dss_tools.results.voltage_ln_nodes
    """

    def __init__(self, dss: Optional[DSS]):
        """Create a facade; pass ``None`` for the global ``dss_tools`` singleton.

        Args:
            dss: Live ``DSS`` instance, or ``None`` until :meth:`update_dss` runs.
        """
        self._dss = dss
        self._results = None
        self._model = None
        self._model_verification = None
        self._dss_view = None
        self._static_view = None
        self._interactive_view = None
        self._simulation = None
        self._configuration = None
        self._utilities = None

        if dss:
            self.__load_objects()

    def __load_objects(self):
        """Construct model, results, views, and tool wrappers for ``self._dss``."""
        from py_dss_toolkit.model.ModelBase import ModelBase
        from py_dss_toolkit.model_verification.ModelVerification import ModelVerification
        from py_dss_toolkit.results.Results import Results
        from py_dss_toolkit.view.dss_view.ViewResults import ViewResults as DSSView
        from py_dss_toolkit.view.interactive_view.ViewResults import ViewResults as InteractiveView
        from py_dss_toolkit.view.static_view.ViewResults import ViewResults as StaticView

        self._model = ModelBase(self._dss)
        self._results = Results(self._dss, lambda: self._model.bus_connection_type_map)
        self._model_verification = ModelVerification(self._dss, self._model)
        self._static_view = StaticView(self._dss, self._results)
        self._interactive_view = InteractiveView(self._dss, self._results, self._model)
        self._dss_view = DSSView(self._dss)
        self._simulation = SimulationTools(self._dss)
        self._configuration = ConfigurationTools(self._dss)
        self._utilities = UtilitiesTools(self._dss)

    def update_dss(self, dss: DSS):
        """Attach a DSS instance and rebuild model, results, and views.

        Use when creating a new engine or switching instances. Cached objects from
        a previous ``dss`` are replaced.

        Args:
            dss: Connected ``py_dss_interface.DSS`` instance.
        """
        self._dss = dss
        self.__load_objects()

    def __raise_if_dss_not_connected(self):
        if self._dss is None:
            raise RuntimeError(
                "DSS is not connected. Use dss_tools.update_dss(dss) before accessing this property. Where dss is an instance of py_dss_interface.DSS()"
            )

    def __raise_if_dssview_backend_unsupported(self):
        """DSSView.exe (used by dss_view) only works with the Windows Delphi OpenDSS DLL."""
        backend = getattr(self._dss, "backend", None)
        if backend != "Windows-Delphi":
            raise RuntimeError(
                "dss_view requires the OpenDSS Windows-Delphi backend because it invokes "
                "DSSView.exe, which is only compatible with that engine build. "
                f"Current backend is {backend!r}."
            )

    @property
    def dss(self) -> DSS:
        """Low-level OpenDSS API handle for this session.

        Returns:
            DSS: The ``py_dss_interface.DSS`` instance passed to :meth:`update_dss`.

        Raises:
            RuntimeError: If no DSS has been set yet.
        """
        self.__raise_if_dss_not_connected()
        return self._dss

    @property
    def results(self) -> "Results":
        """Voltages, currents, powers, losses, monitors, and related outputs.

        Data match the latest solution in :attr:`dss`—solve first via
        :attr:`simulation` (or equivalent) before reading quantities. Combines
        steady-state, time-series, and short-circuit accessors on one object.

        Returns:
            Results: Snapshot, time-series, and fault result namespaces for this circuit.

        Raises:
            RuntimeError: If no DSS has been set yet.
        """
        self.__raise_if_dss_not_connected()
        return self._results

    @property
    def model(self) -> "ModelBase":
        """Compiled circuit as DataFrames (buses, segments, elements) and topology graph.

        Returns:
            ModelBase: Tabular model data plus ``graph`` / ``graph_df`` for NetworkX queries.

        Raises:
            RuntimeError: If no DSS has been set yet.
        """
        self.__raise_if_dss_not_connected()
        return self._model

    @property
    def model_verification(self) -> "ModelVerification":
        """Reports for data-quality and topology issues (e.g. isolated buses, loops).

        Returns:
            ModelVerification: Verification helpers for the active model.

        Raises:
            RuntimeError: If no DSS has been set yet.
        """
        self.__raise_if_dss_not_connected()
        return self._model_verification

    @property
    def dss_view(self) -> "DSSView":
        """Plots via DSSView.exe (Delphi OpenDSS workflow).

        Returns:
            DSSView: Helpers that drive DSSView for plotting.

        Raises:
            RuntimeError: If no DSS is connected, or if ``dss.backend`` is not
                ``Windows-Delphi`` (DSSView.exe only works with the Delphi OpenDSS DLL).
        """
        self.__raise_if_dss_not_connected()
        self.__raise_if_dssview_backend_unsupported()
        return self._dss_view

    @property
    def static_view(self) -> "StaticView":
        """Matplotlib figures for snapshots and studies.

        Returns:
            StaticView: Static plotting API.

        Raises:
            RuntimeError: If no DSS has been set yet.
        """
        self.__raise_if_dss_not_connected()
        return self._static_view

    @property
    def interactive_view(self) -> "InteractiveView":
        """Plotly-based interactive figures and circuit-oriented UI helpers.

        Returns:
            InteractiveView: Interactive visualization API.

        Raises:
            RuntimeError: If no DSS has been set yet.
        """
        self.__raise_if_dss_not_connected()
        return self._interactive_view

    @property
    def simulation(self) -> SimulationTools:
        """Drivers for power flow, time-series, and related solution commands.

        Returns:
            SimulationTools: Methods to solve and advance the simulation.

        Raises:
            RuntimeError: If no DSS has been set yet.
        """
        self.__raise_if_dss_not_connected()
        return self._simulation

    @property
    def configuration(self) -> ConfigurationTools:
        """Helpers for circuit and study configuration (e.g. voltage bases, options).

        Returns:
            ConfigurationTools: Configuration utilities bound to :attr:`dss`.

        Raises:
            RuntimeError: If no DSS has been set yet.
        """
        self.__raise_if_dss_not_connected()
        return self._configuration

    @property
    def utilities(self) -> UtilitiesTools:
        """Small convenience helpers that do not fit the other categories.

        Returns:
            UtilitiesTools: Miscellaneous utilities.

        Raises:
            RuntimeError: If no DSS has been set yet.
        """
        self.__raise_if_dss_not_connected()
        return self._utilities

    def text(self, command: str) -> str:
        """Execute a DSS script line or command string (same as ``dss.text``).

        Args:
            command: Text passed to the OpenDSS text interface (e.g. ``compile``, ``solve``).

        Returns:
            str: Engine output or status text.

        Raises:
            RuntimeError: If no DSS has been set yet.
        """
        self.__raise_if_dss_not_connected()
        return self._dss.text(command)


dss_tools = DSSTools(None)
