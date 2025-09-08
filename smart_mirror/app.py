import sys
from PySide6 import QtWidgets
from .main_window import MirrorWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = MirrorWindow()
    sys.exit(app.exec())
