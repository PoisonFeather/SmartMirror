from PySide6 import QtCore, QtWidgets
from .theme import Theme
from .scale import Scale
from .widgets.clock import ClockWidget
from .widgets.weather import WeatherWidget
from .widgets.agenda import AgendaWidget

class MirrorWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setCursor(QtCore.Qt.BlankCursor)  # hide cursor (kiosk)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, False)

        screen = QtWidgets.QApplication.primaryScreen()
        self.scale = Scale(screen)

        central = QtWidgets.QWidget()
        grid = QtWidgets.QGridLayout(central)
        grid.setContentsMargins(self.scale.px(50), self.scale.px(50), self.scale.px(50), self.scale.px(50))
        grid.setHorizontalSpacing(self.scale.px(30))
        grid.setVerticalSpacing(self.scale.px(30))

        # LEFT COLUMN (Clock + Weather)
        left_col = QtWidgets.QVBoxLayout()
        left_col.setSpacing(self.scale.px(30))
        self.clock = ClockWidget(self.scale)
        self.weather = WeatherWidget(self.scale)
        left_col.addWidget(self.clock)
        left_col.addWidget(self.weather)
        left_col.addStretch(1)

        # RIGHT COLUMN (Agenda)
        right_col = QtWidgets.QVBoxLayout()
        right_col.setSpacing(self.scale.px(30))
        self.agenda = AgendaWidget(self.scale)
        right_col.addWidget(self.agenda)
        right_col.addStretch(1)

        grid.addLayout(left_col, 0, 0)
        grid.addLayout(right_col, 0, 1)
        self.setCentralWidget(central)

        # Apply theme
        self.setStyleSheet(Theme.base_stylesheet())

        # Fullscreen on the target display
        self.showFullScreen()

    # Optional: escape to quit (since frameless)
    def keyPressEvent(self, event) -> None:
        if event.key() in (QtCore.Qt.Key_Escape, QtCore.Qt.Key_Q):
            QtWidgets.QApplication.quit()
        return super().keyPressEvent(event)
