import re

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox, QPushButton

from Entity.User import User

from InteractiveObjects.LogViewerWidget import LogViewerWidget

class LogExportWidget(QWidget):
    def __init__(self, user : User):
        super().__init__()
        self.user = user
        self.initUI()

        self.show()


    def initUI(self):
        layout = QVBoxLayout()

        self.setWindowTitle("Export logs")

        self.user_combo = QComboBox(self)

        export_button = QPushButton("Export Logs", self)

        export_button.clicked.connect(self.doExpotr)

        self.fillCombo()

        layout.addWidget(self.user_combo)
        layout.addWidget(export_button)

        self.setLayout(layout)

        self.resize(200, 75)


    def fillCombo(self):
        users_request = f"GET ALL USERS"
        users_response = self.user.client.Get_response(users_request)

        users_pattern = r'User name = (\w+)'

        user_list: list[str] = []

        for match in re.finditer(users_pattern, users_response):
            user_list.append(match.group(1))

        self.user_combo.addItems(user_list)


    def doExpotr(self):
        logs_request = f"GET LOGS FOR user = {self.user_combo.currentText()}"
        logs_response = self.user.client.Get_response(logs_request)

        self.logViewerWidget = LogViewerWidget(logs_response)
        self.logViewerWidget.move(self.x() // 2, self.y() // 2)
        self.logViewerWidget.show()

        