import plotly.graph_objects as go

from py_dss_toolkit.view.interactive_view.InteractiveCustomPlotStyle import InteractiveCustomPlotStyle


def test_get_legend_config_uses_predefined_position_logic():
    style = InteractiveCustomPlotStyle(legend_position="outside top right", legend_font_size=12)

    config = style._get_legend_config()

    assert config["xanchor"] == "right"
    assert config["yanchor"] == "top"
    assert config["x"] == 1.02
    assert config["y"] == 1
    assert config["borderwidth"] == 1
    assert config["font"]["size"] == 12


def test_get_legend_config_uses_custom_legend_parameters_when_provided():
    style = InteractiveCustomPlotStyle(
        legend_position="outside top right",
        legend_x=0.33,
        legend_y=0.44,
        legend_xanchor="center",
        legend_yanchor="bottom",
        legend_orientation="h",
        legend_font_family="Arial",
        legend_font_color="black",
        legend_borderwidth=2,
        legend_itemwidth=80,
    )

    config = style._get_legend_config()

    assert config["x"] == 0.33
    assert config["y"] == 0.44
    assert config["xanchor"] == "center"
    assert config["yanchor"] == "bottom"
    assert config["orientation"] == "h"
    assert config["borderwidth"] == 2
    assert config["itemwidth"] == 80
    assert config["font"]["family"] == "Arial"
    assert config["font"]["color"] == "black"
    assert config["font"]["size"] == style.legend_font_size


def test_apply_style_updates_figure_layout_with_expected_fields():
    style = InteractiveCustomPlotStyle(show_legend=False, title_font_size=20)
    fig = go.Figure()

    style.apply_style(fig)

    assert fig.layout.showlegend is False
    assert fig.layout.title.font.size == 20
    assert fig.layout.legend.font.size == style.legend_font_size
