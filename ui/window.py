from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from ui.board_widget import BoardWidget
from ai.random_ai import RandomAI
from core.engine import HexEngine
from core.board import Cell


class MainWindow(QMainWindow):
    def __init__(self, size: int = 11) -> None:
        super().__init__()
        self.setWindowTitle("HEX – PyQt6 GUI")
        self.engine = HexEngine(size)
        self.ai = RandomAI(Cell.BLACK)
        self.board_widget = BoardWidget(self.engine, self.ai)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.addWidget(self.board_widget)
        self.setCentralWidget(container)