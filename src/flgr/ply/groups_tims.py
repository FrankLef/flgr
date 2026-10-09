import itertools
from typing import Self
import polars as pl
import plotly.graph_objects as go
from pypalettes import load_palette

from ..colors.convert import convert_hex_to_rgba
from .base import Ply


class PlyGroupsTims(Ply):
    def __init__(
        self,
        name: str,
        data: pl.DataFrame,
        period_var: str,
        group_var: str,
        marker_var: str | None,
        line_var: str | None,
        text_var: str | None,
        textpos_var: str | None,
    ) -> None:
        super().__init__(name=name)
        self.data = data
        self.period_var = period_var
        self.group_var = group_var
        self.marker_var = marker_var
        self.line_var = line_var
        self.text_var = text_var
        self.textpos_var = textpos_var
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

        groups = data[group_var].unique(maintain_order=True).to_list()

        fig = go.Figure()

        color_cycle = itertools.cycle(self.palette)
        for group in groups:
            df = data.filter(pl.col(group_var).eq(group))
            a_color = convert_hex_to_rgba(next(color_cycle))
            if self.marker_var:
                fig.add_trace(
                    go.Scatter(
                        x=df[period_var],
                        y=df[self.marker_var],
                        mode="markers",
                        marker=dict(
                            color=a_color,
                            size=self.geom_marker["size"],
                            symbol=self.geom_marker["shape"],
                        ),
                        name=group,
                    )
                )
            if self.line_var:
                fig.add_trace(
                    go.Scatter(
                        x=df[period_var],
                        y=df[self.line_var],
                        mode="lines",
                        line=dict(
                            color=a_color,
                            width=self.geom_line["size"],
                            dash=self.geom_line["shape"],
                        ),
                        name=group,
                    )
                )
            if self.text_var:
                if not self.textpos_var:
                    msg = f"`textpos_var` cannot be empty when `textvar` ('{self.text_var}') is given."
                    raise ValueError(msg)
                fig.add_trace(
                    go.Scatter(
                        x=df[period_var],
                        y=df[str(self.textpos_var)],
                        mode="text",
                        text="<i>" + df[self.text_var] + "</i>",
                        textposition="top right",
                        textfont_size=self.geom_textfont["size"],
                        textfont=dict(color=self.geom_textfont["color"]),
                        name=group,
                    )
                )
        fig.update_layout(template="none")
        self.fig = fig
        return self
