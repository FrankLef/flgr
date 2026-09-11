import itertools
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
        ybase_var: str,
        group_var: str,
        label_base_var: str,
    ) -> None:
        super().__init__(name=name)
        self.data = data
        self.period_var = period_var
        self.ybase_var = ybase_var
        self.group_var = group_var
        self.label_base_var = label_base_var
        self.set_palette()
        self.set_line()
        self.set_textfont()

    def set_palette(self, name: str = "Classic_10") -> None:
        self.palette = load_palette(name)

    def set_line(self, size: int = 2, shape: str = "solid") -> None:
        self.geom_line = {"size": size, "shape": shape}

    def set_textfont(self, size: int = 12, color="navy") -> None:
        self.geom_textfont = {"size": size, "color": color}

    def execute(self) -> None:
        self.create_base()

    def create_base(self) -> None:
        data = self.data
        group_var = self.group_var
        period_var = self.period_var
        ybase_var = self.ybase_var
        label_base_var = self.label_base_var

        groups = data[group_var].unique(maintain_order=True).to_list()

        fig = go.Figure()

        color_cycle = itertools.cycle(self.palette)
        for group in groups:
            df = data.filter(pl.col(group_var).eq(group))
            a_color = convert_hex_to_rgba(next(color_cycle))
            fig.add_trace(
                go.Scatter(
                    x=df[period_var],
                    y=df[ybase_var],
                    mode="lines+text",
                    text="<i>" + df[label_base_var] + "</i>",
                    textposition="top right",
                    textfont_size=self.geom_textfont["size"],
                    textfont=dict(color=self.geom_textfont["color"]),
                    line=dict(
                        color=a_color,
                        width=self.geom_line["size"],
                        dash=self.geom_line["shape"],
                    ),
                    name=group,
                )
            )
        fig.update_layout(template="none")
        self.fig = fig
