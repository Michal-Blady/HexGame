from PyQt6.QtWidgets import QApplication
import sys
from ui.window import MainWindow


def run():
    app = QApplication(sys.argv)
    window = MainWindow(size=11)
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    run()