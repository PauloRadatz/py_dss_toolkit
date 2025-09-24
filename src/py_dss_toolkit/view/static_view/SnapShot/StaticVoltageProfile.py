# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : VoltageProfile.py
# @Software: PyCharm

import matplotlib.pyplot as plt
from py_dss_toolkit.results.SnapShot.SnapShotPowerFlowResults import SnapShotPowerFlowResults
from py_dss_interface import DSS
from py_dss_toolkit.view.static_view.StaticCustomPlotStyle import StaticCustomPlotStyle
from typing import Optional, Union, Tuple, List
from py_dss_toolkit.view.static_view.SnapShot.StaticVoltageProfileBusMarker import StaticVoltageProfileBusMarker
from py_dss_toolkit.view.view_base.VoltageProfileBase import VoltageProfileBase


class StaticVoltageProfile(VoltageProfileBase):
    """
    A class for creating static voltage profile plots from power flow results.

    This class provides functionality to generate voltage profile plots showing
    voltage magnitude versus distance in km along electrical circuits. It supports
    plotting 3 nodes (phases) with different colors similar to OpenDSS plot profile and allows for
    custom bus markers to highlight specific locations.

    Attributes:
        _results (SnapShotPowerFlowResults): Power flow results containing voltage data
        _dss (DSS): OpenDSS interface object
        _plot_style (StaticCustomPlotStyle): Custom styling configuration for plots
    """

    def __init__(self, dss: DSS, results: SnapShotPowerFlowResults):
        """
        Initialize the StaticVoltageProfile object.

        Args:
            dss (DSS): OpenDSS interface object for accessing circuit data
            results (SnapShotPowerFlowResults): Power flow results containing
                voltage magnitude data for all buses and nodes
        """
        self._results = results
        self._dss = dss
        VoltageProfileBase.__init__(self, self._dss, self._results)

        self._plot_style = StaticCustomPlotStyle()

    @property
    def voltage_profile_plot_style(self):
        """
        Get the custom plot style configuration.

        Returns:
            StaticCustomPlotStyle: The plot style object containing styling
                configuration for voltage profile plots
        """
        return self._plot_style

    def voltage_profile_get_bus_mark(self, name: str, symbol: str = "x",
                                     size: float = 10,
                                     color: str = "black",
                                     marker_name: Optional[str] = None,
                                     show_legend: bool = False):
        """
        Create a bus marker object for highlighting specific buses in voltage profile plots.

        This method creates a StaticVoltageProfileBusMarker object that can be used
        to add custom markers to specific buses in the voltage profile plot.

        Args:
            name (str): The name of the bus to mark
            symbol (str, optional): The marker symbol to use (e.g., 'x', 'o', 's', '^').
                Defaults to "x".
            size (float, optional): The size of the marker. Defaults to 10.
            color (str, optional): The color of the marker. Defaults to "black".
            marker_name (Optional[str], optional): The name to display in the legend.
                If None, uses the bus name. Defaults to None.
            show_legend (bool, optional): Whether to show this marker in the legend.
                Defaults to False.

        Returns:
            StaticVoltageProfileBusMarker: A bus marker object that can be passed
                to the voltage_profile method's buses_marker parameter
        """
        if not marker_name:
            marker_name = name
        return StaticVoltageProfileBusMarker(name=name,
                                             symbol=symbol,
                                             size=size,
                                             color=color,
                                             marker_name=marker_name,
                                             show_legend=show_legend)

    def voltage_profile(self,
                        title: Optional[str] = "Voltage Profile",
                        xlabel: Optional[str] = "Distance (km)",
                        ylabel: Optional[str] = "Voltage (pu)",
                        xlim: Optional[Tuple[Union[int, float], Union[int, float]]] = None,
                        ylim: Optional[Tuple[Union[int, float], Union[int, float]]] = None,
                        line_marker_size: Optional[float] = 2,
                        buses_marker: Optional[List[StaticVoltageProfileBusMarker]] = None,
                        show_voltage_limits: Optional[bool] = True,
                        tight_layout: Optional[bool] = True,
                        legend: Optional[bool] = True,
                        dpi: Optional[int] = 200,
                        save_file_path: Optional[str] = None,
                        show: Optional[bool] = True,
                        **kwargs
                        ):
        """
        Generate a voltage profile plot showing voltage magnitude versus distance.

        This method creates a static voltage profile plot displaying voltage magnitudes
        for each node (phase) along the electrical circuit. The plot shows voltage
        versus distance with different colors for each node (Node 1: black, Node 2: red,
        Node 3: blue). Custom bus markers can be added to highlight specific locations.
        Optional voltage limit lines can be displayed showing the normal voltage maximum
        and minimum limits from OpenDSS.

        Args:
            title (Optional[str], optional): The title of the plot. Defaults to "Voltage Profile".
            xlabel (Optional[str], optional): Label for the x-axis. Defaults to "Distance (km)".
            ylabel (Optional[str], optional): Label for the y-axis. Defaults to "Voltage (pu)".
            xlim (Optional[Tuple[Union[int, float], Union[int, float]]], optional):
                Tuple of (min, max) values for x-axis limits. If None, auto-scales.
                Defaults to None.
            ylim (Optional[Tuple[Union[int, float], Union[int, float]]], optional):
                Tuple of (min, max) values for y-axis limits. If None, auto-scales.
                Defaults to None.
            line_marker_size (Optional[float], optional): Size of the circular markers
                on the voltage profile lines. Defaults to 2.
            buses_marker (Optional[List[StaticVoltageProfileBusMarker]], optional):
                List of custom bus markers to highlight specific buses. Use
                voltage_profile_get_bus_mark() to create marker objects. Defaults to None.
            show_voltage_limits (Optional[bool], optional): Whether to display horizontal
                red dashed lines showing the normal voltage maximum and minimum limits from OpenDSS.
                The limits are retrieved using "get normvmaxpu" and "get normvminpu" commands.
                Defaults to True.
            tight_layout (Optional[bool], optional): Whether to use tight layout for
                the plot to prevent overlapping elements. Defaults to True.
            legend (Optional[bool], optional): Whether to display the legend showing
                node colors and custom bus markers. Note: Voltage limit lines are not
                automatically added to the legend. Defaults to True.
            dpi (Optional[int], optional): Resolution of the plot in dots per inch.
                Defaults to 200.
            save_file_path (Optional[str], optional): File path to save the plot as PNG.
                If None, plot is not saved. Defaults to None.
            show (Optional[bool], optional): Whether to display the plot window.
                Defaults to True.
            **kwargs: Additional keyword arguments passed to the matplotlib figure object.

        Returns:
            Tuple[matplotlib.figure.Figure, matplotlib.axes.Axes]: A tuple containing:
                - fig: The matplotlib Figure object containing the plot
                - ax: The matplotlib Axes object for further customization

        Raises:
            Exception: If no energymeter is found in the circuit (checked by _check_energymeter).
            ValueError: If voltage limits cannot be retrieved from OpenDSS when show_voltage_limits=True.

        Note:
            The method automatically checks for the presence of an energymeter in the
            circuit before generating the plot. Voltage profiles require distance
            information which is typically provided by energymeter elements.

        """
        self._check_energymeter()

        self._plot_style.apply_style()
        fig, ax = plt.subplots()
        for key, value in kwargs.items():
            setattr(fig, key, value)

        buses, df, distances, sections = self._prepare_results()
        node_colors = {1: 'black', 2: 'red', 3: 'blue'}

        bus_annotated = list()
        legend_handles = [
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=node_colors[node], markersize=6)
            for node in range(1, 4)
        ]
        legend_labels = [f'Node {node}' for node in range(1, 4)]

        # Dictionary to track which bus markers have been added to the legend
        legend_added = {}

        for node in range(1, 4):
            for section in sections:
                bus1, bus2 = section
                distance1 = distances[buses.index(bus1)]
                distance2 = distances[buses.index(bus2)]
                ax.plot([distance1, distance2], [df.loc[bus1, f'node{node}'], df.loc[bus2, f'node{node}']], marker='o',
                        color=node_colors[node], markersize=line_marker_size)

                if buses_marker:
                    bus_marker = next((bus for bus in buses_marker if bus.name == bus1), None)
                    if bus_marker:
                        ax.plot(distance1, df.loc[bus1, f'node{node}'],
                                marker=bus_marker.symbol,
                                markersize=bus_marker.size,
                                color=bus_marker.color)

                        # Add the bus marker to the legend if show_legend is True and not already added
                        if bus_marker.show_legend and bus_marker.marker_name not in legend_added:
                            handle = plt.Line2D([0], [0],
                                                marker=bus_marker.symbol,
                                                color=bus_marker.color,
                                                linestyle='None',
                                                markersize=bus_marker.size,
                                                markerfacecolor=bus_marker.color,
                                                markeredgecolor=bus_marker.color)
                            legend_handles.append(handle)
                            legend_labels.append(bus_marker.marker_name)
                            legend_added[bus_marker.marker_name] = True  # Mark this marker as added

        # Add voltage limits if requested
        if show_voltage_limits:
            # Get voltage limits from OpenDSS
            normvmaxpu = float(self._dss.text("get normvmaxpu"))
            normvminpu = float(self._dss.text("get normvminpu"))

            # Get the x-axis limits to draw lines across the entire plot
            x_min, x_max = ax.get_xlim()

            # Plot horizontal lines for voltage limits
            ax.axhline(y=normvmaxpu, color='red', linestyle='--', linewidth=1.5, alpha=0.7, label=f'Max Limit ({normvmaxpu:.3f} pu)')
            ax.axhline(y=normvminpu, color='red', linestyle='--', linewidth=1.5, alpha=0.7, label=f'Min Limit ({normvminpu:.3f} pu)')

        # Create the legend
        if legend:
            ax.legend(legend_handles, legend_labels)

        fig.suptitle(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)

        if tight_layout:
            fig.tight_layout()

        fig.set_dpi(dpi)

        if save_file_path:
            fig.savefig(save_file_path, format="png", dpi=300, bbox_inches='tight')

        if show:
            plt.show()

        return fig, ax
