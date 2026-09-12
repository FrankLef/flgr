import polars as pl
from typing import Self
import plotly.graph_objects as go

from .base import Ply


class PlyWaterfall(Ply):
    def __init__(
        self,
        name: str,
        data: pl.DataFrame,
        x_period: str,
        x_label: str,
        measure: str,
        y: str,
        text: str,
        base: float,
    ) -> None:
        super().__init__(name=name)
        self.data = data
        self.x_period = x_period
        self.x_label = x_label
        self.measure = measure
        self.y = y
        self.text = text
        self.base = base

    def execute(self) -> Self:
        self.create_base()
        return self

    def create_base(self) -> Self:
        data = self.data
        x_period = self.x_period
        x_label = self.x_label
        measure = self.measure
        y = self.y
        text = self.text
        base = self.base

        fig = go.Figure(
            go.Waterfall(
                x=[data[x_period], data[x_label]],
                measure=data[measure],
                y=data[y],
                textposition="outside",
                text=data[text],
                base=base,
                decreasing={
                    "marker": {"color": "Maroon", "line": {"color": "red", "width": 2}}
                },
                increasing={"marker": {"color": "Teal"}},
                totals={
                    "marker": {
                        "color": "deep sky blue",
                        "line": {"color": "blue", "width": 3},
                    }
                },
            )
        )
        fig.update_layout(waterfallgap=0.3)
        self.fig = fig
        return self
