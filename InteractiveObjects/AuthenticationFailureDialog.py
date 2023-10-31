from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout

class AuthenticationFailureDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.show()


    def init_ui(self):
        self.setWindowTitle('Authentication Failure')
        self.setGeometry(819, 471, 400, 100)

        layout = QVBoxLayout()

        message_label = QLabel('Authentication failed. Please check your credentials.')
        ok_button = QPushButton('OK')
        ok_button.clicked.connect(self.accept)

        layout.addWidget(message_label)
        layout.addWidget(ok_button)

        self.setLayout(layout)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.activateWindow()

