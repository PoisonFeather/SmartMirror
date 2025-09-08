from PySide6 import QtWidgets, QtCore
from ..theme import Theme
from .clock import GlowLabel
from ..services.weather_service import get_current_weather

CITY = "Alba Iulia"   # schimbă aici
COUNTRY = "RO"        # sau None

class _WeatherWorker(QtCore.QObject):
    finished = QtCore.Signal(dict)
    error = QtCore.Signal(str)

    @QtCore.Slot()
    def run(self):
        try:
            data = get_current_weather(CITY, COUNTRY)
            self.finished.emit(data)
        except Exception as e:
            self.error.emit(str(e))

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

        self.temp_label = GlowLabel("—°")
        self.temp_label.setStyleSheet(f"font-size: {self.scale.sp(56)}pt; font-weight: 300;")

        self.desc_label = QtWidgets.QLabel(f"Se încarcă… · {CITY}")
        self.desc_label.setObjectName("subtitle")
        self.desc_label.setStyleSheet(f"font-size: {self.scale.sp(16)}pt;")

        row.addWidget(self.temp_label, 0)
        row.addWidget(self.desc_label, 1)
        row.addStretch(1)

        self.extra_label = QtWidgets.QLabel("—")
        self.extra_label.setObjectName("subtitle")
        self.extra_label.setStyleSheet(f"font-size: {self.scale.sp(14)}pt;")

        layout.addWidget(title)
        layout.addLayout(row)
        layout.addWidget(self.extra_label)

        # --- state for threading ---
        self._thread: QtCore.QThread | None = None
        self._worker: _WeatherWorker | None = None
        self._running = False

        # înălțime minimă ca să nu rămână doar o linie
        self.setMinimumHeight(self.scale.px(120))

        # refresh periodic (10 min)
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.refresh_async)
        self._timer.start(10 * 60 * 1000)

        # first load imediat
        QtCore.QTimer.singleShot(0, self.refresh_async)

    @QtCore.Slot()
    def refresh_async(self):
        if self._running:
            return  # evită cereri simultane
        self._running = True

        self.desc_label.setText(f"Se încarcă… · {CITY}")
        self.extra_label.setText("—")

        self._thread = QtCore.QThread(self)
        self._worker = _WeatherWorker()
        self._worker.moveToThread(self._thread)

        self._thread.started.connect(self._worker.run)
        self._worker.finished.connect(self._on_result)
        self._worker.error.connect(self._on_error)

        # cleanup / reset flags
        self._worker.finished.connect(self._thread.quit)
        self._worker.error.connect(self._thread.quit)
        self._thread.finished.connect(self._thread.deleteLater)
        self._thread.finished.connect(self._on_thread_finished)

        # worker-ul e șters după ce thread-ul iese curat
        self._worker.finished.connect(self._worker.deleteLater)
        self._worker.error.connect(self._worker.deleteLater)

        self._thread.start()

    @QtCore.Slot()
    def _on_thread_finished(self):
        self._running = False
        self._thread = None
        self._worker = None

    @QtCore.Slot(dict)
    def _on_result(self, data: dict):
        # data: temp, desc, wind_kmh, humidity, location
        t = data.get("temp")
        d = data.get("desc") or "—"
        w = data.get("wind_kmh")
        h = data.get("humidity")
        loc = data.get("location") or CITY

        self.temp_label.setText(f"{t}°" if t is not None else "—°")
        self.desc_label.setText(f"{d} · {loc}")

        extras = []
        if w is not None: extras.append(f"Vânt {w} km/h")
        if h is not None: extras.append(f"Umiditate {h}%")
        self.extra_label.setText(" · ".join(extras) if extras else "—")

        # debug vizibil în consolă
       # print("weather data:", data)

    @QtCore.Slot(str)
    def _on_error(self, msg: str):
        self.desc_label.setText(f"Eroare meteo · {CITY}")
        self.extra_label.setText("Verifică conexiunea la internet")
        print("weather error:", msg)

    def cleanup(self):
        """Oprește timerul și așteaptă threadul să se oprească (cheamă din closeEvent)."""
        try:
            if self._timer:
                self._timer.stop()
            if self._thread and self._thread.isRunning():
                self._thread.quit()
                self._thread.wait(2000)
        finally:
            self._thread = None
            self._worker = None
            self._running = False
