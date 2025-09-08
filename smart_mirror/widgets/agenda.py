from PySide6 import QtWidgets

class AgendaWidget(QtWidgets.QWidget):
    def __init__(self, scale, parent=None):
        super().__init__(parent)
        self.scale = scale
        self.setProperty("class", "card")

        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(scale.px(22), scale.px(18), scale.px(22), scale.px(18))
        root.setSpacing(scale.px(10))

        title = QtWidgets.QLabel("Agenda Azi")
        title.setObjectName("title")
        title.setStyleSheet(f"font-size: {scale.sp(18)}pt; font-weight: 500;")

        self.list = QtWidgets.QVBoxLayout()
        self.list.setSpacing(scale.px(8))

        root.addWidget(title)
        root.addLayout(self.list)

        self.populate_dummy()

    def add_item(self, time_str: str, text: str):
        h = QtWidgets.QHBoxLayout()
        h.setSpacing(self.scale.px(10))

        time = QtWidgets.QLabel(time_str)
        time.setObjectName("accent")
        time.setStyleSheet(f"font-size: {self.scale.sp(16)}pt; font-weight: 500;")

        txt = QtWidgets.QLabel(text)
        txt.setObjectName("subtitle")
        txt.setStyleSheet(f"font-size: {self.scale.sp(16)}pt;")

        h.addWidget(time, 0)
        h.addWidget(txt, 1)
        self.list.addLayout(h)

    def populate_dummy(self):
        self.add_item("08:30", "Standup proiect")
        self.add_item("12:00", "Prânz cu Alex")
        self.add_item("16:30", "Gym · Pull day")
