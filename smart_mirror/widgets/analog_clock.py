from math import sin, cos, pi
from datetime import datetime
from PySide6 import QtCore, QtGui, QtWidgets
from ..theme import Theme

class AnalogClockWidget(QtWidgets.QWidget):
    """
    Ceas analog minimalist:
    - Marcaje: ore (12) + minute (60) discrete
    - Limbi: oră/minut (pline), secundar opțional (sweep smooth)
    - Auto-scale după dimensiunea widgetului (folosește cât spațiu are)
    - Glow subtil pe limbi pentru lizibilitate pe sticlă
    """
    def __init__(self, scale, show_seconds=True, parent=None):
        super().__init__(parent)
        self.scale = scale
        self.show_seconds = show_seconds
        self.setMinimumSize(scale.px(260), scale.px(260))  # măcar 260px
        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent, True)
        self.setAutoFillBackground(False)

        # Timer: 60 FPS pentru sweep lin; dacă nu vrei sweep, pune 1000ms
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(16 if self.show_seconds else 1000)

        # Antialiasing hint
        self.setRenderHint = True

    def sizeHint(self):
        return QtCore.QSize(self.scale.px(420), self.scale.px(420))

    def _draw_glow_line(self, painter, p1, p2, width):
        """Strat subțire translucid sub limbă ca 'glow' discret."""
        glow = QtGui.QPen(QtGui.QColor(135, 206, 250, 70))  # #87CEFA cu alpha
        glow.setCapStyle(QtCore.Qt.RoundCap)
        glow.setWidthF(width * 1.8)
        painter.setPen(glow)
        painter.drawLine(p1, p2)

    def paintEvent(self, event):
        now = datetime.now()
        sec = now.second + now.microsecond / 1_000_000.0
        minute = now.minute + sec / 60.0
        hour = (now.hour % 12) + minute / 60.0

        # Setup painter
        p = QtGui.QPainter(self)
        if self.setRenderHint:
            p.setRenderHint(QtGui.QPainter.Antialiasing, True)

        # Fundal (ușor mai deschis decât bg ca să „iasă” cercul subtil)
        p.fillRect(self.rect(), QtGui.QColor(11, 11, 13))  # Theme.BG

        # Normalizează la un pătrat și translatează în centru
        side = min(self.width(), self.height())
        cx = self.width() / 2
        cy = self.height() / 2
        radius = side * 0.45  # padding natural

        p.translate(cx, cy)

        # Cadran minimalist: cerc subțire
        pen_face = QtGui.QPen(QtGui.QColor(255, 255, 255, 22))
        pen_face.setWidthF(side * 0.006)
        p.setPen(pen_face)
        p.setBrush(QtCore.Qt.NoBrush)
        p.drawEllipse(QtCore.QPointF(0, 0), radius, radius)

        # Marcaje minute (60) foarte discrete
        minor_pen = QtGui.QPen(QtGui.QColor(255, 255, 255, 28))
        minor_pen.setWidthF(max(1.0, side * 0.003))
        p.setPen(minor_pen)
        for i in range(60):
            angle = i * (2 * pi / 60.0)
            r1 = radius * 0.92
            r2 = radius * 0.96
            # La 5 minute, nu desenăm aici (marcajele de oră vor fi mai tari)
            if i % 5 != 0:
                x1, y1 = r1 * sin(angle), -r1 * cos(angle)
                x2, y2 = r2 * sin(angle), -r2 * cos(angle)
                p.drawLine(QtCore.QPointF(x1, y1), QtCore.QPointF(x2, y2))

        # Marcaje ore (12) mai vizibile
        hour_pen = QtGui.QPen(QtGui.QColor(245, 245, 247, 120))
        hour_pen.setCapStyle(QtCore.Qt.RoundCap)
        hour_pen.setWidthF(max(1.5, side * 0.006))
        p.setPen(hour_pen)
        for i in range(12):
            angle = i * (2 * pi / 12.0)
            r1 = radius * 0.88
            r2 = radius * 0.97
            x1, y1 = r1 * sin(angle), -r1 * cos(angle)
            x2, y2 = r2 * sin(angle), -r2 * cos(angle)
            p.drawLine(QtCore.QPointF(x1, y1), QtCore.QPointF(x2, y2))

        # Limba orei
        hour_angle = (hour / 12.0) * 2 * pi
        hour_len = radius * 0.55
        hour_w = max(3.0, side * 0.012)
        p1 = QtCore.QPointF(0, 0)
        p2 = QtCore.QPointF(hour_len * sin(hour_angle), -hour_len * cos(hour_angle))
        self._draw_glow_line(p, p1, p2, hour_w)
        pen_hour = QtGui.QPen(QtGui.QColor(245, 245, 247))  # alb cald
        pen_hour.setWidthF(hour_w)
        pen_hour.setCapStyle(QtCore.Qt.RoundCap)
        p.setPen(pen_hour)
        p.drawLine(p1, p2)

        # Limba minutului
        minute_angle = (minute / 60.0) * 2 * pi
        min_len = radius * 0.78
        min_w = max(2.0, side * 0.0085)
        p2 = QtCore.QPointF(min_len * sin(minute_angle), -min_len * cos(minute_angle))
        self._draw_glow_line(p, p1, p2, min_w)
        pen_min = QtGui.QPen(QtGui.QColor(245, 245, 247))
        pen_min.setWidthF(min_w)
        pen_min.setCapStyle(QtCore.Qt.RoundCap)
        p.setPen(pen_min)
        p.drawLine(p1, p2)

        # Limba secundarului (opțional), accent soft
        if self.show_seconds:
            sec_angle = (sec / 60.0) * 2 * pi
            sec_len = radius * 0.86
            s_w = max(1.2, side * 0.004)
            sec_color = QtGui.QColor(124, 212, 253)  # Theme.ACCENT
            # linie dublă (fină) pentru un look high-end
            p2 = QtCore.QPointF(sec_len * sin(sec_angle), -sec_len * cos(sec_angle))
            pen_glide = QtGui.QPen(QtGui.QColor(sec_color.red(), sec_color.green(), sec_color.blue(), 140))
            pen_glide.setWidthF(s_w)
            pen_glide.setCapStyle(QtCore.Qt.RoundCap)
            p.setPen(pen_glide)
            p.drawLine(p1, p2)

            # contragreutate scurtă în spate
            back_len = radius * 0.18
            p3 = QtCore.QPointF(-back_len * sin(sec_angle), back_len * cos(sec_angle))
            p.drawLine(p1, p3)

        # buton central
        center_brush = QtGui.QBrush(QtGui.QColor(245, 245, 247))
        p.setPen(QtCore.Qt.NoPen)
        p.setBrush(center_brush)
        p.drawEllipse(QtCore.QPointF(0, 0), max(2.5, side * 0.007), max(2.5, side * 0.007))
