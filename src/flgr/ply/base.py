from typing import NamedTuple


class GeomSpecs(NamedTuple):
    color: str | None = None
    size: float | None = None
    shape: str | None = None


class Ply:
    def __init__(self, name: str) -> None:
        self.name = name
        self._title = ""
        self._subtitle = ""

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, text: str) -> None:
        self._title = text

    @property
    def subtitle(self) -> str:
        return self._subtitle

    @subtitle.setter
    def subtitle(self, text: str) -> None:
        self._subtitle = text
