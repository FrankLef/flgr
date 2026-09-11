import itertools
from typing import Self
import polars as pl
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pypalettes import load_palette

from ..colors.convert import convert_hex_to_rgba
from .base import Ply


class PlyFacetsTims(Ply):
    def __init__(
        self,
        name: str,
        data: pl.DataFrame,
        period_var: str,
        ybase_var: str,
        yewm_var: str,
        group_var: str,
        label_base_var: str,
    ) -> None:
        super().__init__(name=name)
        self.data = data
        self.period_var = period_var
        self.ybase_var = ybase_var
        self.yewm_var = yewm_var
        self.group_var = group_var
        self.label_base_var = label_base_var
        self.set_palette()
        self.set_line()
        self.set_marker()
        self.set_textfont()

    def set_palette(self, name: str = "Classic_10") -> Self:
        self.palette = load_palette(name)
        return self

    def set_line(self, size: int = 3, shape: str = "solid") -> Self:
        self.geom_line = {"size": size, "shape": shape}
        return self

    def set_marker(self, size: int = 10, shape="circle") -> Self:
        # Options: 'circle', 'diamond', 'cross', 'x' ...
        self.geom_marker = {"size": size, "shape": shape}
        return self

    def set_textfont(self, size: int = 12, color="navy") -> Self:
        self.geom_textfont = {"size": size, "color": color}
        return self

    def execute(self) -> Self:
        self.create_base()
        return self

    def create_base(self) -> Self:
        data = self.data
        group_var = self.group_var
        period_var = self.period_var
        ybase_var = self.ybase_var
        yewm_var = self.yewm_var
        label_base_var = self.label_base_var

        groups = data[group_var].unique(maintain_order=True).to_list()
        ngroups = len(groups)

        fig = make_subplots(
            rows=ngroups,
            cols=1,
            subplot_titles=groups,
            shared_xaxes=True,
            vertical_spacing=0.10,
        )

        color_cycle = itertools.cycle(self.palette)
        for nrow, group in enumerate(groups, start=1):
            df = data.filter(pl.col(group_var).eq(group))
            a_color = convert_hex_to_rgba(next(color_cycle))
            fig.add_trace(
                go.Scatter(
                    x=df[period_var],
                    y=df[yewm_var],
                    mode="lines",
                    line=dict(
                        color=a_color,
                        width=self.geom_line["size"],
                        dash=self.geom_line["shape"],
                    ),
                ),
                row=nrow,
                col=1,
            )
            fig.add_trace(
                go.Scatter(
                    x=df[period_var],
                    y=df[ybase_var],
                    mode="markers+text",
                    text="<i>" + df[label_base_var] + "</i>",
                    textposition="top right",
                    textfont_size=self.geom_textfont["size"],
                    textfont=dict(color=self.geom_textfont["color"]),
                    marker=dict(
                        color=a_color,
                        size=self.geom_marker["size"],
                        symbol=self.geom_marker["shape"],
                    ),
                ),
                row=nrow,
                col=1,
            )
        fig.update_layout(template="none")
        self.fig = fig
        return self
