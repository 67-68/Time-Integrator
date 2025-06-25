from QtUI.views.MainWindow import MainWindow
from PyQt6.QtWidgets import QApplication
import sys

DEBUG_UI = True

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
