from datetime import datetime
from PySide6 import QtCore, QtWidgets, QtGui
from ..theme import Theme

class GlowLabel(QtWidgets.QLabel):
    """Subtle glow for glass readability."""
    def __init__(self, *args, glow_color=Theme.GLOW, glow_radius=12, **kwargs):
        super().__init__(*args, **kwargs)
        effect = QtWidgets.QGraphicsDropShadowEffect()
        effect.setBlurRadius(glow_radius)
        effect.setColor(QtGui.QColor(glow_color))
        effect.setOffset(0, 0)
        self.setGraphicsEffect(effect)

class ClockWidget(QtWidgets.QWidget):
    """Minimal — fără card; timp mare, separator hairline, dată mică."""
    def __init__(self, scale, parent=None):
        super().__init__(parent)
        self.scale = scale

        col = QtWidgets.QVBoxLayout(self)
        col.setContentsMargins(0, 0, 0, 0)
        col.setSpacing(self.scale.px(8))

        self.time_label = GlowLabel()
        self.time_label.setObjectName("title")
        self.time_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        # hairline sub oră
        line = QtWidgets.QFrame()
        line.setObjectName("line")

        self.date_label = QtWidgets.QLabel()
        self.date_label.setObjectName("subtitle")
        self.date_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        col.addWidget(self.time_label)
        col.addWidget(line)
        col.addWidget(self.date_label)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()

    def update_time(self):
        now = datetime.now()
        self.time_label.setText(now.strftime("%H:%M"))
        self.date_label.setText(now.strftime("%A, %d %B %Y"))

        # tipografie mai mare și mai light
        self.time_label.setStyleSheet(
            f"font-size: {self.scale.sp(120)}pt; font-weight: 300; letter-spacing: 0.5px;"
        )
        self.date_label.setStyleSheet(
            f"font-size: {self.scale.sp(22)}pt;"
        )
