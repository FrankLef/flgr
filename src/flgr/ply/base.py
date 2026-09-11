from typing import Self
import plotly.graph_objects as go


# class GeomSpecs(NamedTuple):
#     color: str | None = None
#     size: float | None = None
#     shape: str | None = None


class Ply:
    def __init__(self, name: str) -> None:
        self.name = name
        self.fig = go.Figure()

    def titles(self, title: str, subtitle: str | None = None) -> Self:
        self.fig.update_layout(
            title=dict(text=title, subtitle=dict(text=subtitle)),
        )
        return self

    def template(self, templ: go.layout.Template) -> Self:
        self.fig.update_layout(template=templ)
        return self
