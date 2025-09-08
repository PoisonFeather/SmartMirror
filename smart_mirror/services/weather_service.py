from PySide6 import QtWidgets
from ..theme import Theme
from .clock import GlowLabel

class WeatherWidget(QtWidgets.QWidget):
    def __init__(self, scale, parent=None):
        super().__init__(parent)
        self.scale = scale
        self.setObjectName("weatherCard")
        self.setProperty("class", "card")

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(scale.px(22), scale.px(18), scale.px(22), scale.px(18))
        layout.setSpacing(scale.px(10))

        title = QtWidgets.QLabel("Vremea")
        title.setObjectName("title")
        title.setStyleSheet(f"font-size: {scale.sp(18)}pt; font-weight: 500;")

        row = QtWidgets.QHBoxLayout()
        row.setSpacing(self.scale.px(14))

        # Temperatură mare + descriere
        self.temp_label = GlowLabel("23°")
        self.temp_label.setStyleSheet(f"font-size: {self.scale.sp(56)}pt; font-weight: 300;")

        self.desc_label = QtWidgets.QLabel("Parțial noros · Alba Iulia")
        self.desc_label.setObjectName("subtitle")
        self.desc_label.setStyleSheet(f"font-size: {self.scale.sp(16)}pt;")

        row.addWidget(self.temp_label, 0)
        row.addWidget(self.desc_label, 1)
        row.addStretch(1)

        self.extra_label = QtWidgets.QLabel("Vânt 8 km/h · Umiditate 50%")
        self.extra_label.setObjectName("subtitle")
        self.extra_label.setStyleSheet(f"font-size: {self.scale.sp(14)}pt;")

        layout.addWidget(title)
        layout.addLayout(row)
        layout.addWidget(self.extra_label)
