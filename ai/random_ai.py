from __future__ import annotations
import random
from typing import Tuple

from core.board import Board, Cell

class RandomAI:

    def __init__(self, color: Cell, connect_chance: float = 0.5) -> None:

        self.color = color
        self.name = "AI-SmartRandom"
        self.connect_chance = connect_chance

    def get_move(self, board: Board) -> Tuple[int, int]:
        empties = [(r, c)
                   for r in range(board.size)
                   for c in range(board.size)
                   if board.empty(r, c)]

        if random.random() < self.connect_chance:
            connecting = []
            for (r, c) in empties:
                for nr, nc in board.neighbors(r, c):
                    if board.grid[nr][nc] == self.color:
                        connecting.append((r, c))
                        break
            if connecting:
                return random.choice(connecting)

        return random.choice(empties)
