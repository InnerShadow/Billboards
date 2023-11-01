import re

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QVBoxLayout, QHBoxLayout
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

        self.password_input.returnPressed.connect(self.log_in)

        form_layout = QVBoxLayout()
        form_layout.addWidget(self.username_label)
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(self.password_label)
        form_layout.addWidget(self.password_input)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.continue_button)

        layout.addLayout(form_layout)
        layout.addLayout(button_layout)

        self.setLayout(layout)
        # self.setWindowFlags(Qt.WindowStaysOnTopHint)
        # self.activateWindow()


    def log_in(self):    
        username = self.username_input.text()
        password = self.password_input.text()

        if username and password: 
            idendefication_request = f"TRY TO LOG IN login = {username}, password = {password}"
            idendefication_repsnose = self.client.Get_response(idendefication_request)

            autendeficated_pattern = r'IDENDEFICATION OK role = (\w+) '
            autendeficated_matches = re.search(autendeficated_pattern, idendefication_repsnose)

            if autendeficated_matches:
                self.hide()

                role = autendeficated_matches.group(1)

                self.success_dialog = AuthenticationSuccessDialog(username)
                self.success_dialog.move(self.x(), self.y())
                self.success_dialog.show()
                self.login_successful.emit(f'Logged in successfully username = {username}, role = {role}')

            elif idendefication_repsnose == 'IDENTIFICATION NOT OK':
                self.failure_dialog = AuthenticationFailureDialog()
                self.failure_dialog.move(self.x(), self.y())
                self.failure_dialog.show()
                self.highlight_fields()

        else:
            self.failure_dialog = AuthenticationFailureDialog()
            self.failure_dialog.move(self.x(), self.y())
            self.failure_dialog.show()
            self.highlight_fields()


    def continue_as_viewer(self):
        viewer_request = f"CONTINUE AS VIEWER"
        _ = self.client.Get_response(viewer_request)
        self.hide()
        self.success_dialog = AuthenticationSuccessDialog('viewer')
        self.success_dialog.move(self.x(), self.y())
        self.success_dialog.show()
        self.login_successful.emit(f'Logged in successfully username = VIEWER, role = viewer')


    def highlight_fields(self):
        style = "QLineEdit { background-color: #FF9999; }"
        self.username_input.setStyleSheet(style)
        self.password_input.setStyleSheet(style)

