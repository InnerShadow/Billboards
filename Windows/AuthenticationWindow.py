from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import pyqtSignal

class AuthenticationWindow(QWidget):

    login_successful = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.init_ui()

        self.show()


    def init_ui(self):
        self.setWindowTitle('Authentication')
        self.setGeometry(300, 300, 400, 200)

        layout = QVBoxLayout()

        self.username_label = QLabel('Username:')
        self.username_input = QLineEdit()

        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton('Log In')
        self.login_button.clicked.connect(self.log_in)

        self.continue_button = QPushButton('Continue as Viewer')
        self.continue_button.clicked.connect(self.continue_as_viewer)

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.continue_button)

        self.setLayout(layout)


    def log_in(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if username == 'your_username' and password == 'your_password':
            self.login_successful.emit('Logged in successfully')
            self.hide()
            


    def continue_as_viewer(self):
        print('Continue as viewer')
        self.hide()


