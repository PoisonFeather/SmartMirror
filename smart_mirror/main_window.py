from PySide6 import QtCore, QtWidgets
from .theme import Theme
from .scale import Scale
from .widgets.analog_clock import AnalogClockWidget   # <— nou
from .widgets.weather import WeatherWidget
from .widgets.agenda import AgendaWidget
from .widgets.clock import ClockWidget
class MirrorWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setCursor(QtCore.Qt.BlankCursor)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, False)

        screen = QtWidgets.QApplication.primaryScreen()
        self.scale = Scale(screen)

        central = QtWidgets.QWidget()
        grid = QtWidgets.QGridLayout(central)
        outer = self.scale.px(80)
        grid.setContentsMargins(outer, outer, outer, outer)
        grid.setHorizontalSpacing(self.scale.px(48))
        grid.setVerticalSpacing(self.scale.px(40))

        left_col = QtWidgets.QVBoxLayout()
        left_col.setSpacing(self.scale.px(32))

        # Ceas analog mare
        self.clockAnalog= AnalogClockWidget(self.scale, show_seconds=True)
        self.clock = ClockWidget(self.scale)
        left_col.addWidget(self.clockAnalog, 0)
        left_col.addWidget(self.clock, 1)

        # Meteo sub ceas
        self.weather = WeatherWidget(self.scale)
        left_col.addWidget(self.weather)
        left_col.addStretch(1)

        right_col = QtWidgets.QVBoxLayout()
        right_col.setSpacing(self.scale.px(32))
        self.agenda = AgendaWidget(self.scale)
        right_col.addWidget(self.agenda)
        right_col.addStretch(1)

        grid.addLayout(left_col, 0, 0)
        grid.addLayout(right_col, 0, 1)
        grid.setColumnStretch(0, 3)
        grid.setColumnStretch(1, 2)

        self.setCentralWidget(central)
        self.setStyleSheet(Theme.base_stylesheet())
        self.showFullScreen()

    def keyPressEvent(self, event) -> None:
        if event.key() in (QtCore.Qt.Key_Escape, QtCore.Qt.Key_Q):
            QtWidgets.QApplication.quit()
        return super().keyPressEvent(event)
