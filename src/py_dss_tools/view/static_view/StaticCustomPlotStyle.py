# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : CustomPlotStyle.py
# @Software: PyCharm


from dataclasses import dataclass
import matplotlib.pyplot as plt

@dataclass
class StaticCustomPlotStyle:
    figure_figsize: tuple = (6, 5)
    figure_facecolor: str = 'white'
    axes_labelcolor: str = '.15'
    xtick_direction: str = 'out'
    ytick_direction: str = 'out'
    xtick_color: str = '.15'
    ytick_color: str = '.15'
    axes_axisbelow: bool = True
    grid_linestyle: str = '--'
    text_color: str = '.15'
    font_family: list = None
    font_sans_serif: list = None
    lines_solid_capstyle: str = 'round'
    patch_edgecolor: str = 'w'
    patch_force_edgecolor: bool = True
    xtick_top: bool = False
    ytick_right: bool = False
    axes_grid: bool = True
    axes_facecolor: str = 'white'
    axes_edgecolor: str = '.8'
    grid_color: str = '.8'
    axes_spines_left: bool = True
    axes_spines_bottom: bool = True
    axes_spines_right: bool = True
    axes_spines_top: bool = True
    xtick_bottom: bool = False
    ytick_left: bool = False
    axes_titlesize: str = 'x-large'
    axes_labelsize: str = 'large'
    figure_titlesize: str = 'x-large'
    xtick_labelsize: str = 'medium'
    ytick_labelsize: str = 'medium'
    legend_fontsize: str = 'medium'
    legend_loc: str = 'upper right'
    legend_shadow: bool = False
    legend_title_fontsize: str = 'large'

    def __post_init__(self):
        if self.font_family is None:
            self.font_family = ['sans-serif']

        if self.font_sans_serif is None:
            self.font_sans_serif = ['Arial', 'DejaVu Sans', 'Liberation Sans', 'Bitstream Vera Sans', 'sans-serif']

    def apply_style(self):
        style_mapping = {
            'figure_figsize': 'figure.figsize',
            'figure_facecolor': 'figure.facecolor',
            'axes_labelcolor': 'axes.labelcolor',
            'xtick_direction': 'xtick.direction',
            'ytick_direction': 'ytick.direction',
            'xtick_color': 'xtick.color',
            'ytick_color': 'ytick.color',
            'axes_axisbelow': 'axes.axisbelow',
            'grid_linestyle': 'grid.linestyle',
            'text_color': 'text.color',
            'font_family': 'font.family',
            'font_sans_serif': 'font.sans-serif',
            'lines_solid_capstyle': 'lines.solid_capstyle',
            'patch_edgecolor': 'patch.edgecolor',
            'patch_force_edgecolor': 'patch.force_edgecolor',
            'xtick_top': 'xtick.top',
            'ytick_right': 'ytick.right',
            'axes_grid': 'axes.grid',
            'axes_facecolor': 'axes.facecolor',
            'axes_edgecolor': 'axes.edgecolor',
            'grid_color': 'grid.color',
            'axes_spines_left': 'axes.spines.left',
            'axes_spines_bottom': 'axes.spines.bottom',
            'axes_spines_right': 'axes.spines.right',
            'axes_spines_top': 'axes.spines.top',
            'xtick_bottom': 'xtick.bottom',
            'ytick_left': 'ytick.left',
            'axes_titlesize': 'axes.titlesize',
            'axes_labelsize': 'axes.labelsize',
            'figure_titlesize': 'figure.titlesize',
            'xtick_labelsize': 'xtick.labelsize',
            'ytick_labelsize': 'ytick.labelsize',
            'legend_fontsize': 'legend.fontsize',
            'legend_loc': 'legend.loc',
            'legend_shadow': 'legend.shadow',
            'legend_title_fontsize': 'legend.title_fontsize'
        }

        style_config = {style_mapping[key]: value for key, value in self.__dict__.items() if not key.startswith("__")}
        plt.rcParams.update(style_config)
