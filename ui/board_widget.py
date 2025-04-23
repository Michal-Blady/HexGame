from __future__ import annotations
from PyQt6.QtWidgets import QWidget, QPushButton, QGridLayout, QMessageBox
from PyQt6.QtCore import Qt
from core.engine import HexEngine
from core.board import Cell
from ai.random_ai import RandomAI


class BoardWidget(QWidget):
    def __init__(self, engine: HexEngine, ai: RandomAI) -> None:
        super().__init__()
        self.engine = engine
        self.ai = ai
        size = engine.board.size
        self.buttons: list[list[QPushButton]] = []

        grid = QGridLayout(self)
        grid.setSpacing(4)
        for r in range(size):
            row_btns: list[QPushButton] = []
            for c in range(size):
                btn = QPushButton()
                btn.setFixedSize(36, 36)
                btn.clicked.connect(lambda _, x=r, y=c: self.on_click(x, y))
                grid.addWidget(btn, r, c + r)  # offset for hex layout
                row_btns.append(btn)
            self.buttons.append(row_btns)
        self.update_ui_all()

    def on_click(self, r: int, c: int) -> None:
        if not self.engine.board.empty(r, c):
            return
        self.play_move(r, c)
        if self.engine.winner():
            return
        # AI move
        ar, ac = self.ai.get_move(self.engine.board)
        self.play_move(ar, ac)

    def play_move(self, r: int, c: int) -> None:
        self.engine.play(r, c)
        self.update_ui(r, c)
        winner = self.engine.winner()
        if winner:
            self.show_winner(winner)

    def update_ui(self, r: int, c: int) -> None:
        cell = self.engine.board.grid[r][c]
        btn = self.buttons[r][c]
        if cell is Cell.WHITE:
            btn.setStyleSheet('background: white;')
        else:
            btn.setStyleSheet('background: black;')
        btn.setEnabled(False)

    def update_ui_all(self) -> None:
        size = self.engine.board.size
        for r in range(size):
            for c in range(size):
                btn = self.buttons[r][c]
                btn.setText('')
                btn.setEnabled(self.engine.board.empty(r, c))
                btn.setStyleSheet('')

    def show_winner(self, winner: Cell) -> None:
        msg = "Wygrał biały!" if winner is Cell.WHITE else "Wygrał czarny!"
        QMessageBox.information(self, "Koniec gry", msg)
        # Disable all buttons
        for row in self.buttons:
            for btn in row:
                btn.setEnabled(False)