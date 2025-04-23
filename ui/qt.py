from __future__ import annotations

import sys
from functools import partial

from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QGridLayout, QMessageBox
)
from ai.random_ai import RandomAI
from core.engine import HexEngine
from core.engine import Cell


class HexWindow(QWidget):
    def __init__(self, size: int = 11) -> None:
        super().__init__()
        self.engine = HexEngine(size)
        self.ai = RandomAI(Cell.RED)
        self.buttons: list[list[QPushButton]] = []

        grid = QGridLayout(self)
        for r in range(size):
            row_btns = []
            for c in range(size):
                btn = QPushButton(" ")
                btn.setFixedSize(36, 36)
                btn.clicked.connect(partial(self.move_human, r, c))
                grid.addWidget(btn, r, c + r)
                row_btns.append(btn)
            self.buttons.append(row_btns)

        self.setWindowTitle("HEX – PyQt6")
        self.show()

    def move_human(self, r: int, c: int) -> None:
        if not self.engine.board.empty(r, c):
            return
        self.make_move(r, c)                # Blue
        if self.engine.winner():
            return
        ar, ac = self.ai.get_move(self.engine.board)
        self.make_move(ar, ac)
        self.engine.turn = Cell.BLUE

    def make_move(self, r: int, c: int) -> None:
        self.engine.play(r, c)
        self.update_ui(r, c)
        winner = self.engine.winner()
        if winner:
            QMessageBox.information(self, "Koniec gry",
                                     f"Zwycięża {winner.name}!")
            self.close()

    def update_ui(self, r: int, c: int) -> None:
        cell = self.engine.board.grid[r][c]
        char = "●" if cell is Cell.BLUE else "○"
        self.buttons[r][c].setText(char)
        self.buttons[r][c].setEnabled(False)


def main() -> None:  # noqa: D401
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("HEX – PyQt6")
    engine = HexEngine(11)
    ai = RandomAI(Cell.RED)

    grid = QGridLayout(window)

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
