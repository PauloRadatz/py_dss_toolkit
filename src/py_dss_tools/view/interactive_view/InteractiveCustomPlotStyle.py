# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : CustomPlotStyle.py
# @Software: PyCharm

from dataclasses import dataclass
import plotly.graph_objects as go


@dataclass
class InteractiveCustomPlotStyle:
    template: str = 'plotly_white'
    title_font_size: int = 24
    axis_label_font_size: int = 18
    tick_font_size: int = 14
    legend_font_size: int = 16
    show_grid: bool = True
    grid_color: str = 'lightgray'
    title_x: float = 0.5  # Center the title
    show_legend: bool = True
    legend_position: str = 'top right'

    def apply_style(self, fig: go.Figure):
        fig.update_layout(
            template=self.template,
            title_font=dict(size=self.title_font_size),
            xaxis=dict(
                title_font=dict(size=self.axis_label_font_size),
                tickfont=dict(size=self.tick_font_size),
                showgrid=self.show_grid,
                gridcolor=self.grid_color
            ),
            yaxis=dict(
                title_font=dict(size=self.axis_label_font_size),
                tickfont=dict(size=self.tick_font_size),
                showgrid=self.show_grid,
                gridcolor=self.grid_color
            ),
            legend=dict(
                font=dict(size=self.legend_font_size),
                xanchor='right',
                yanchor='top',
                x=1 if self.legend_position == 'top right' else 0,
                y=1
            ),
            title_x=self.title_x,
            showlegend=self.show_legend
        )
