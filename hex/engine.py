from __future__ import annotations

from typing import Tuple

from .board import Board, Cell
from .unionfind import DSU


class HexEngine:
    def __init__(self, size: int = 11) -> None:
        self.board = Board(size)
        n = size * size
        self.top, self.bottom = n, n + 1
        self.left, self.right = n, n + 1
        self.uf_blue = DSU(n + 2)
        self.uf_red = DSU(n + 2)
        self.turn = Cell.BLUE

    def play(self, r: int, c: int) -> None:
        self.board.place(r, c, self.turn)
        index = self._idx(r, c)
        self._connect_neighbors(r, c, index)
        self._connect_edges(r, c, index)
        self.turn = self.turn.other()

    def winner(self) -> Cell | None:  # noqa: D401
        if self.uf_blue.find(self.top) == self.uf_blue.find(self.bottom):
            return Cell.BLUE
        if self.uf_red.find(self.left) == self.uf_red.find(self.right):
            return Cell.RED
        return None

    def _idx(self, r: int, c: int) -> int:
        return r * self.board.size + c

    def _connect_neighbors(self, r: int, c: int, index: int) -> None:
        for nr, nc in self.board.neighbors(r, c):
            if self.board.grid[nr][nc] == self.board.grid[r][c]:
                neigh_idx = self._idx(nr, nc)
                if self.board.grid[r][c] == Cell.BLUE:
                    self.uf_blue.union(index, neigh_idx)
                else:
                    self.uf_red.union(index, neigh_idx)

    def _connect_edges(self, r: int, c: int, index: int) -> None:
        size = self.board.size
        if self.board.grid[r][c] == Cell.BLUE:
            if r == 0:
                self.uf_blue.union(index, self.top)
            if r == size - 1:
                self.uf_blue.union(index, self.bottom)
        else:
            if c == 0:
                self.uf_red.union(index, self.left)
            if c == size - 1:
                self.uf_red.union(index, self.right)
