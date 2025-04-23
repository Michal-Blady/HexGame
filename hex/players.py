from __future__ import annotations

import random
import sys
from typing import Tuple

from colorama import Fore, Style

from .board import Board, Cell


class Player:
    def __init__(self, color: Cell, name: str | None = None) -> None:
        self.color = color
        self.name = name or ("Blue" if color is Cell.BLUE else "Red")

    def get_move(self, board: Board) -> Tuple[int, int]:
        raise NotImplementedError


class HumanPlayer(Player):
    def get_move(self, board: Board) -> Tuple[int, int]:  # noqa: D401
        while True:
            print(f"{self.name} ({self._color_tag}): podaj ruch [np. 3 4] » ", end="")
            try:
                r, c = map(int, sys.stdin.readline().split())
                if board.empty(r, c):
                    return r, c
                print("Pole zajęte – spróbuj ponownie.")
            except (ValueError, IndexError):
                print("Błędny format – spróbuj ponownie.")

    @property
    def _color_tag(self) -> str:
        return Fore.BLUE + "B" + Style.RESET_ALL if self.color is Cell.BLUE else Fore.RED + "R" + Style.RESET_ALL


class RandomAI(Player):
    def get_move(self, board: Board) -> Tuple[int, int]:
        empties = [
            (r, c)
            for r in range(board.size)
            for c in range(board.size)
            if board.empty(r, c)
        ]
        return random.choice(empties)
