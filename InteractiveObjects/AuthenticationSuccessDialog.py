from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout

class AuthenticationSuccessDialog(QDialog):
    def __init__(self, username):
        super().__init__()
        self.init_ui(username)
        self.show()


    def init_ui(self, username):
        self.setWindowTitle('Authentication Success')
        self.setGeometry(819, 471, 400, 100)

        layout = QVBoxLayout()

        message_label = QLabel(f'Logged in successfully as {username}')
        ok_button = QPushButton('OK')
        ok_button.clicked.connect(self.accept)

        layout.addWidget(message_label)
        layout.addWidget(ok_button)

        self.setLayout(layout)

