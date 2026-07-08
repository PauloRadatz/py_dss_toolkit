# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : CustomPlotStyle.py
# @Software: PyCharm

from dataclasses import dataclass
from typing import Any
from typing import Dict
from typing import Optional

import plotly.graph_objects as go


@dataclass
class InteractiveCustomPlotStyle:
    template: str = "plotly_white"
    title_font_size: int = 24
    axis_label_font_size: int = 18
    tick_font_size: int = 14
    legend_font_size: int = 16
    show_grid: bool = True
    grid_color: str = "lightgray"
    title_x: float = 0.5  # Center the title
    show_legend: bool = True
    legend_position: str = "outside top right"  # Options: 'top left', 'top right', 'bottom left', 'bottom right', 'outside top left', 'outside top right', 'outside bottom left', 'outside bottom right'

    # Custom legend properties (override legend_position when specified)
    legend_x: Optional[float] = None  # X position (0-1 for inside, <0 or >1 for outside)
    legend_y: Optional[float] = None  # Y position (0-1 for inside, <0 or >1 for outside)
    legend_xanchor: Optional[str] = None  # 'left', 'center', 'right'
    legend_yanchor: Optional[str] = None  # 'top', 'middle', 'bottom'
    legend_bgcolor: Optional[str] = None  # Background color (e.g., 'rgba(255,255,255,0.8)')
    legend_bordercolor: Optional[str] = None  # Border color
    legend_borderwidth: Optional[int] = None  # Border width in pixels
    legend_orientation: Optional[str] = None  # 'v' (vertical) or 'h' (horizontal)
    legend_font_family: Optional[str] = None  # Font family
    legend_font_color: Optional[str] = None  # Font color
    legend_itemwidth: Optional[int] = None  # Width of legend items

    def apply_style(self, fig: go.Figure):
        fig.update_layout(
            template=self.template,
            title_font=dict(size=self.title_font_size),
            xaxis=dict(
                title_font=dict(size=self.axis_label_font_size),
                tickfont=dict(size=self.tick_font_size),
                showgrid=self.show_grid,
                gridcolor=self.grid_color,
            ),
            yaxis=dict(
                title_font=dict(size=self.axis_label_font_size),
                tickfont=dict(size=self.tick_font_size),
                showgrid=self.show_grid,
                gridcolor=self.grid_color,
            ),
            legend=self._get_legend_config(),
            title_x=self.title_x,
            showlegend=self.show_legend,
        )

    def _get_legend_config(self) -> Dict[str, Any]:
        """
        Get legend configuration based on custom parameters or legend_position.

        Returns:
            Dict[str, Any]: Legend configuration dictionary for Plotly
        """
        # Check if any custom legend parameters are specified
        custom_params = [
            self.legend_x,
            self.legend_y,
            self.legend_xanchor,
            self.legend_yanchor,
            self.legend_bgcolor,
            self.legend_bordercolor,
            self.legend_borderwidth,
            self.legend_orientation,
            self.legend_font_family,
            self.legend_font_color,
            self.legend_itemwidth,
        ]

        # If any custom parameters are provided, use them
        if any(param is not None for param in custom_params):
            config = {}

            # Position parameters
            if self.legend_x is not None:
                config["x"] = self.legend_x
            if self.legend_y is not None:
                config["y"] = self.legend_y
            if self.legend_xanchor is not None:
                config["xanchor"] = self.legend_xanchor
            if self.legend_yanchor is not None:
                config["yanchor"] = self.legend_yanchor

            # Styling parameters
            if self.legend_bgcolor is not None:
                config["bgcolor"] = self.legend_bgcolor
            if self.legend_bordercolor is not None:
                config["bordercolor"] = self.legend_bordercolor
            if self.legend_borderwidth is not None:
                config["borderwidth"] = self.legend_borderwidth
            if self.legend_orientation is not None:
                config["orientation"] = self.legend_orientation
            if self.legend_itemwidth is not None:
                config["itemwidth"] = self.legend_itemwidth

            # Font configuration
            font_config = {"size": self.legend_font_size}
            if self.legend_font_family is not None:
                font_config["family"] = self.legend_font_family
            if self.legend_font_color is not None:
                font_config["color"] = self.legend_font_color
            config["font"] = font_config

            return config

        # Otherwise, use the predefined legend_position logic
        return dict(
            font=dict(size=self.legend_font_size),
            xanchor="left" if "left" in self.legend_position else "right",
            yanchor="bottom" if "bottom" in self.legend_position else "top",
            x=(
                -0.15
                if "outside" in self.legend_position and "left" in self.legend_position
                else 1.02
                if "outside" in self.legend_position and "right" in self.legend_position
                else 0
                if "left" in self.legend_position
                else 1
            ),
            y=0 if "bottom" in self.legend_position else 1,
            bgcolor="rgba(255,255,255,0.8)" if "outside" in self.legend_position else None,
            bordercolor="gray" if "outside" in self.legend_position else None,
            borderwidth=1 if "outside" in self.legend_position else 0,
        )
