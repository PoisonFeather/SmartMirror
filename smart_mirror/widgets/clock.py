from datetime import datetime
from PySide6 import QtCore, QtWidgets, QtGui
from smart_mirror.theme import Theme

class GlowLabel(QtWidgets.QLabel):
    """QLabel that draws a subtle outer glow to increase readability on glass."""
    def __init__(self, *args, glow_color=Theme.GLOW, glow_radius=8, **kwargs):
        super().__init__(*args, **kwargs)
        self._drop_shadow = QtWidgets.QGraphicsDropShadowEffect()
        self._drop_shadow.setBlurRadius(glow_radius)
        self._drop_shadow.setColor(QtGui.QColor(glow_color))
        self._drop_shadow.setOffset(0, 0)
        self.setGraphicsEffect(self._drop_shadow)

class ClockWidget(QtWidgets.QWidget):
    def __init__(self, scale, parent=None):
        super().__init__(parent)
        self.scale = scale
        self.setObjectName("clockCard")

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(scale.px(24), scale.px(20), scale.px(24), scale.px(20))
        layout.setSpacing(scale.px(4))

        self.time_label = GlowLabel()
        self.time_label.setObjectName("title")
        self.time_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        self.date_label = QtWidgets.QLabel()
        self.date_label.setObjectName("subtitle")
        self.date_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        layout.addWidget(self.time_label)
        layout.addWidget(self.date_label)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()

        self.setProperty("class", "card")

    def update_time(self):
        now = datetime.now()
        self.time_label.setText(now.strftime("%H:%M"))
        self.date_label.setText(now.strftime("%A, %d %B %Y"))
        self.time_label.setStyleSheet(f"font-size: {self.scale.sp(90)}pt; font-weight: 300;")
        self.date_label.setStyleSheet(f"font-size: {self.scale.sp(20)}pt;")
