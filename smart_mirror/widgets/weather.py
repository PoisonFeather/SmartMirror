from PySide6 import QtWidgets
from .clock import GlowLabel

class WeatherWidget(QtWidgets.QWidget):
    def __init__(self, scale, parent=None):
        super().__init__(parent)
        self.scale = scale
        self.setObjectName("weatherCard")
        self.setProperty("class", "card")
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(scale.px(24), scale.px(20), scale.px(24), scale.px(20))
        layout.setSpacing(scale.px(6))

        title = QtWidgets.QLabel("Vremea")
        title.setObjectName("title")
        title.setStyleSheet(f"font-size: {scale.sp(22)}pt; font-weight: 500;")

        self.temp_label = GlowLabel("23°")
        self.temp_label.setStyleSheet(f"font-size: {self.scale.sp(50)}pt; font-weight: 300;")

        self.desc_label = QtWidgets.QLabel("Parțial noros · Alba Iulia")
        self.desc_label.setObjectName("subtitle")
        self.desc_label.setStyleSheet(f"font-size: {self.scale.sp(16)}pt;")

        row = QtWidgets.QHBoxLayout()
        row.addWidget(self.temp_label)
        row.addSpacing(self.scale.px(12))
        row.addWidget(self.desc_label)
        row.addStretch(1)

        self.extra_label = QtWidgets.QLabel("Vânt 8 km/h · Umiditate 50%")
        self.extra_label.setObjectName("subtitle")
        self.extra_label.setStyleSheet(f"font-size: {self.scale.sp(14)}pt;")

        layout.addWidget(title)
        layout.addLayout(row)
        layout.addWidget(self.extra_label)

        # TODO: Hook a weather API here and refresh every 10–15 min
