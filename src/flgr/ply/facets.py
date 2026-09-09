import polars as pl
from typing import Final, Any
import plotly.graph_objects as go
from plotly.subplots import make_subplots


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

    def execute(self) -> None:
        self.fig = self.create_base()

    def create_base(self) -> go.Figure:
        TEXTFONT: Final[dict[str, Any]] = {"color": "navy", "size": 12}
        # MARKER_SIZE: Final[int] = 6

        data = self.data
        group_var = self.group_var
        period_var = self.period_var
        ybase_var = self.ybase_var
        ewm_var = self.yewm_var
        label_base_var = self.label_base_var

        groups = data[group_var].unique(maintain_order=True).to_list()
        ngroups = len(groups)

        fig = make_subplots(
            rows=ngroups,
            cols=1,
            # subplot_titles=concept_labels,
            shared_xaxes=True,
            vertical_spacing=0.10,
        )

        for nrow, group in enumerate(groups, start=1):
            df = data.filter(pl.col(group))
            fig.add_trace(
                go.Scatter(
                    x=df[period_var],
                    y=df[ewm_var],
                    mode="lines",
                    # line=dict(
                    #     color=concept_color,
                    #     width=int(geom_line["size"]),
                    #     dash=geom_line["shape"],
                    # ),
                ),
                row=nrow,
                col=1,
            )
            fig.add_trace(
                go.Scatter(
                    x=data[period_var],
                    y=data[ybase_var],
                    mode="markers+text",
                    text="<i>" + data[label_base_var] + "</i>",
                    textposition="top right",
                    textfont_size=TEXTFONT["size"],
                    textfont=dict(color=TEXTFONT["color"]),
                    # marker=dict(
                    #     color=concept_color,
                    #     size=MARKER_SIZE,
                    # ),
                ),
                row=nrow,
                col=1,
            )
        fig.update_layout(showlegend=False)
        return fig
