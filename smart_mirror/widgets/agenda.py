from PySide6 import QtWidgets

class AgendaWidget(QtWidgets.QWidget):
    def __init__(self, scale, parent=None):
        super().__init__(parent)
        self.scale = scale
        self.setProperty("class", "card")

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(scale.px(24), scale.px(20), scale.px(24), scale.px(20))
        layout.setSpacing(scale.px(10))

        title = QtWidgets.QLabel("Agenda Azi")
        title.setObjectName("title")
        title.setStyleSheet(f"font-size: {scale.sp(22)}pt; font-weight: 500;")

        self.list = QtWidgets.QVBoxLayout()
        self.list.setSpacing(scale.px(8))
        self.populate_dummy()

        layout.addWidget(title)
        layout.addLayout(self.list)

        # TODO: integrate Google Calendar / local ICS

    def add_item(self, time_str: str, text: str):
        h = QtWidgets.QHBoxLayout()
        lbl_time = QtWidgets.QLabel(time_str)
        lbl_time.setObjectName("accent")
        lbl_time.setStyleSheet(f"font-size: {self.scale.sp(16)}pt;")

        lbl_text = QtWidgets.QLabel(text)
        lbl_text.setObjectName("subtitle")
        lbl_text.setStyleSheet(f"font-size: {self.scale.sp(16)}pt;")

        h.addWidget(lbl_time)
        h.addSpacing(self.scale.px(12))
        h.addWidget(lbl_text)
        h.addStretch(1)
        self.list.addLayout(h)

    def populate_dummy(self):
        self.add_item("08:30", "Standup proiect")
        self.add_item("12:00", "Prânz cu Alex")
        self.add_item("16:30", "Gym · Pull day")
