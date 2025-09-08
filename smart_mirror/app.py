import sys
from PySide6 import QtCore, QtWidgets
from .main_window import MirrorWindow

if __name__ == "__main__":
    # Enable HiDPI before creating the app
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    app = QtWidgets.QApplication(sys.argv)
    win = MirrorWindow()
    sys.exit(app.exec())
