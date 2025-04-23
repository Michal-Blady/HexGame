from __future__ import annotations

from core.board import Board, Cell
from core.dsu import DSU


class HexEngine:
    def __init__(self, size: int = 11) -> None:
        self.board = Board(size)
        n = size * size
        self.top, self.bottom = n, n + 1
        self.left, self.right = n, n + 1
        self.uf_black = DSU(n + 2)
        self.uf_white = DSU(n + 2)
        self.turn = Cell.BLACK

    def play(self, r: int, c: int) -> None:
        self.board.place(r, c, self.turn)
        idx = self._idx(r, c)
        self._connect_neighbors(r, c, idx)
        self._connect_edges(r, c, idx)
        self.turn = self.turn.other()

    def winner(self) -> Cell | None:
        if self.uf_black.find(self.top) == self.uf_black.find(self.bottom):
            return Cell.BLACK
        if self.uf_white.find(self.left) == self.uf_white.find(self.right):
            return Cell.WHITE
        return None

    def _idx(self, r: int, c: int) -> int:
        return r * self.board.size + c

    def _connect_neighbors(self, r: int, c: int, idx: int) -> None:
        for nr, nc in self.board.neighbors(r, c):
            if self.board.grid[nr][nc] == self.board.grid[r][c]:
                nidx = self._idx(nr, nc)
                if self.board.grid[r][c] == Cell.BLACK:
                    self.uf_black.union(idx, nidx)
                else:
                    self.uf_white.union(idx, nidx)

    def _connect_edges(self, r: int, c: int, idx: int) -> None:
        size = self.board.size
        if self.board.grid[r][c] == Cell.BLACK:
            if r == 0:
                self.uf_black.union(idx, self.top)
            if r == size - 1:
                self.uf_black.union(idx, self.bottom)
        else:
            if c == 0:
                self.uf_white.union(idx, self.left)
            if c == size - 1:
                self.uf_white.union(idx, self.right)
