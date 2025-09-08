from PySide6 import QtGui

class Scale:
    def __init__(self, screen: QtGui.QScreen):
        size = screen.size()  # QSize in pixels
        dpi = screen.logicalDotsPerInch() or 96
        # baseline: 1920x1080 @ 96 DPI
        sx = size.width() / 1920.0
        sy = size.height() / 1080.0
        sdpi = dpi / 96.0
        self.f = max(sx, sy) * 0.95  # slightly smaller than max scale
        self.dpi = sdpi

    def px(self, n: int) -> int:
        return max(1, int(round(n * self.f)))

    def sp(self, n: int) -> int:
        # scale for font points
        return max(6, int(round(n * self.f * self.dpi)))
