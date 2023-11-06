import re

from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtCore import pyqtSignal

from ServerData.Client import Client

class AuthenticationWindow(QWidget):
    #Main Window will catch thi signal
    login_successful = pyqtSignal(str)

    def __init__(self, client : Client):
        super().__init__()
        self.client = client
        self.init_ui()


    #Set buttons & lines to enter data
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


    #Try to log in
    def log_in(self):
        #Get texts from line editors    
        username = self.username_input.text()
        password = self.password_input.text()

        #If fill all fields
        if username and password:
            #Ask server to check data 
            idendefication_request = f"TRY TO LOG IN login = {username}, password = {password}"
            idendefication_repsnose = self.client.Get_response(idendefication_request)

            #Deparse it
            autendeficated_pattern = r'IDENDEFICATION OK role = (\w+) '
            autendeficated_matches = re.search(autendeficated_pattern, idendefication_repsnose)

            #If idendefication ok
            if autendeficated_matches:
                self.hide()

                role = autendeficated_matches.group(1)

                self.show_success_message(f"Logged in successfully as {username}")
                self.login_successful.emit(f'Logged in successfully username = {username}, role = {role}')

            #Else say it & highlight fields
            else:
                self.highlight_fields()
                self.show_error_message("Logged in failed")

        #Ask to fill all fields
        else:
            self.highlight_fields()
            self.show_error_message("Logged in failed")


    #Continue as viewer option
    def continue_as_viewer(self):
        #Tell server about continue as viewer option
        viewer_request = f"CONTINUE AS VIEWER"
        _ = self.client.Get_response(viewer_request)
        self.hide()
        self.show_success_message("Logged in successfully as viewer")
        self.login_successful.emit(f'Logged in successfully username = VIEWER, role = viewer')


    #Simply highlight input fields
    def highlight_fields(self):
        style = "QLineEdit { background-color: #FF9999; }"
        self.username_input.setStyleSheet(style)
        self.password_input.setStyleSheet(style)


    #Messege box about faild idendefication
    def show_error_message(self, message):
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle("Error")
        error_dialog.setText(message)
        error_dialog.exec_()


    #Messege box about success idendefication
    def show_success_message(self, message):
        success_dialog = QMessageBox()
        success_dialog.setIcon(QMessageBox.Information)
        success_dialog.setWindowTitle("Success")
        success_dialog.setText(message)
        success_dialog.exec_()


