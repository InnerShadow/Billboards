from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import pyqtSignal

from ServerData.Client import Client
from InteractiveObjects.AuthenticationFailureDialog import AuthenticationFailureDialog
from InteractiveObjects.AuthenticationSuccessDialog import AuthenticationSuccessDialog

class AuthenticationWindow(QWidget):

    login_successful = pyqtSignal(str)

    def __init__(self, client : Client):
        super().__init__()
        self.client = client
        self.init_ui()


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

        idendefication_request = f"TRY TO LOG IN login = {username}, password = {password} "
        idendefication_repsnose = self.client.Get_response(idendefication_request)

        if idendefication_repsnose == "IDENDEFICATION OK":
            self.hide()

            self.success_dialog = AuthenticationSuccessDialog(username)
            self.success_dialog.show()
            self.login_successful.emit(f'Logged in successfully username = {username}')
        elif idendefication_repsnose == 'IDENTIFICATION NOT OK':
            print("AAAAAAAAAAAAa")
            self.failure_dialog = AuthenticationFailureDialog()
            self.failure_dialog.show()
            

    def continue_as_viewer(self):
        viewer_request = f"CONTINUE AS VIEWER"
        _ = self.client.Get_response(viewer_request)

        self.hide()

        self.success_dialog = AuthenticationSuccessDialog('viewer')
        self.success_dialog.show()
        self.login_successful.emit(f'Logged in successfully username = VIEWER')

