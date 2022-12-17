import sys

from PySide6.QtWidgets import QApplication

from src import ui

app = QApplication(sys.argv)
main = ui.Main()
main.show()
sys.exit(app.exec())