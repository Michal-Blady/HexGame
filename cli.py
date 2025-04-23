#!/usr/bin/env python
"""Wejście z linii komend – gra konsolowa."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import List

from hex.board import Cell
from hex.engine import HexEngine
from hex.players import HumanPlayer, RandomAI

SAVE_FILE = Path("hex_state.json")


def build_players(cfg: List[str]) -> List:
    mapping = {"human": HumanPlayer, "ai": RandomAI}
    players = []
    for idx, spec in enumerate(cfg):
        try:
            cls = mapping[spec]
        except KeyError:
            sys.exit(f"Nieznany typ gracza: {spec!r}")
        color = Cell.BLUE if idx == 0 else Cell.RED
        players.append(cls(color))
    return players


def save_state(engine: HexEngine) -> None:
    data = {
        "size": engine.board.size,
        "grid": [[cell.value for cell in row] for row in engine.board.grid],
        "turn": engine.turn.value,
    }
    SAVE_FILE.write_text(json.dumps(data))


def load_state() -> HexEngine | None:
    if not SAVE_FILE.exists():
        return None
    data = json.loads(SAVE_FILE.read_text())
    engine = HexEngine(data["size"])
    engine.board.grid = [[Cell(v) for v in row] for row in data["grid"]]
    engine.turn = Cell(data["turn"])
    # DSU trzeba odbudować:
    for r in range(engine.board.size):
        for c in range(engine.board.size):
            if engine.board.grid[r][c] != Cell.EMPTY:
                engine.play(r, c)
    return engine


def main() -> None:  # noqa: D401
    parser = argparse.ArgumentParser(description="HEX – gra konsolowa")
    parser.add_argument("--size", type=int, default=11, help="rozmiar planszy (domyślnie 11)")
    parser.add_argument("--players", nargs=2, default=["human", "ai"],
                        help="typy graczy [human|ai] np. --players human human")
    parser.add_argument("--resume", action="store_true", help="wznawia ostatnią zapisaną grę")
    args = parser.parse_args()

    engine = load_state() if args.resume else HexEngine(args.size)
    p1, p2 = build_players(args.players)

    print(engine.board)
    while not engine.winner():
        current = p1 if engine.turn is Cell.BLUE else p2
        r, c = current.get_move(engine.board)
        engine.play(r, c)
        print("\n" * 3, engine.board, sep="")
        save_state(engine)  # auto‑save po każdym ruchu

    winner = engine.winner()
    print(f"\n🎉  ZWYCIĘŻA {winner.name}!  🎉")
    SAVE_FILE.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
