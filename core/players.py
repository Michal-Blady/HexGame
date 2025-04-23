from __future__ import annotations

import sys
from typing import Tuple

from core.board import Board, Cell

try:
    from colorama import Fore, Style
except ImportError:
    class _NoColor:
        def __getattr__(self, _):
            return ""

    Fore = Style = _NoColor()


class Player:
    def __init__(self, color: Cell, name: str | None = None) -> None:
        self.color = color
        self.name = name or ("White" if color is Cell.WHITE else "Black")

    def get_move(self, board: Board) -> Tuple[int, int]:
        raise NotImplementedError


class HumanPlayer(Player):

    def get_move(self, board: Board) -> Tuple[int, int]:
        tag = (
            Fore.WHITE + "W" + Style.RESET_ALL
            if self.color is Cell.WHITE
            else Fore.BLACK + "B" + Style.RESET_ALL
        )
        while True:
            try:
                raw = input(f"{self.name} ({tag}) – ruch [wiersz kolumna] » ")
                r, c = map(int, raw.split())
                if board.empty(r, c):
                    return r, c
                print("❗  Pole zajęte – spróbuj ponownie.")
            except (ValueError, IndexError):
                print("❗  Błędny format – spróbuj ponownie.")
