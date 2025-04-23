from __future__ import annotations

import enum
from typing import Iterator, List, Tuple


class Cell(enum.IntEnum):
    EMPTY = 0
    WHITE = 1
    BLACK = 2

    def other(self) -> "Cell":  # noqa: D401
        return Cell.WHITE if self is Cell.BLACK else Cell.BLACK


class Board:
    """Hex‑board + ASCII‑wizualizacja."""

    # sąsiedztwo heksagonalne (w układzie axial)
    DIRS: Tuple[Tuple[int, int], ...] = (
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
    )

    def __init__(self, size: int = 11) -> None:
        self.size = size
        self.grid: List[List[Cell]] = [
            [Cell.EMPTY for _ in range(size)] for _ in range(size)
        ]


    def inside(self, r: int, c: int) -> bool:
        return 0 <= r < self.size and 0 <= c < self.size

    def empty(self, r: int, c: int) -> bool:
        return self.grid[r][c] is Cell.EMPTY

    def place(self, r: int, c: int, who: Cell) -> None:
        if not self.inside(r, c):
            raise ValueError("Ruch poza planszą")
        if not self.empty(r, c):
            raise ValueError("Pole zajęte")
        self.grid[r][c] = who

    def neighbors(self, r: int, c: int) -> Iterator[Tuple[int, int]]:
        for dr, dc in Board.DIRS:
            nr, nc = r + dr, c + dc
            if self.inside(nr, nc):
                yield nr, nc


    def __str__(self) -> str:
        lines: List[str] = []
        pad = ""
        for r in range(self.size):
            line = pad + " ".join(self._cell_char(r, c) for c in range(self.size))
            lines.append(line)
            pad += "  "
        return "\n".join(lines)

    def _cell_char(self, r: int, c: int) -> str:  # noqa: D401
        mapping = {Cell.EMPTY: ".", Cell.WHITE: "●", Cell.BLACK: "○"}
        return mapping[self.grid[r][c]]

def as_int_grid(self) -> list[list[int]]:
    return [[cell.value for cell in row] for row in self.grid]
