from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel, QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QMessageBox

from Entity.User import User

#Check password handler (when try to delete someone)
class PasswordDialog(QDialog):
    loggedin = pyqtSignal(bool)

    def __init__(self, parent, username : str, user : User):
        super().__init__(parent)

        self.user = user
        self.username = username
        self.initUI()


    #Init all necessary graphics items
    def initUI(self):
        layout = QVBoxLayout()

        password_label = QLabel(f"Enter You're Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.setWindowTitle("Check password")

        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Cancel")

        ok_button.clicked.connect(self.ok_connect)
        cancel_button.clicked.connect(self.reject)

        layout.addWidget(password_label)
        layout.addWidget(self.password_input)

        button_layout = QHBoxLayout()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    
    #Check password from the server when try to delete someone
    def ok_connect(self):
        password = self.password_input.text()
        confirmPasswordRequest = f"TRY TO LOG IN login = {self.user.login}, password = {password}"
        confirmPasswordResponse = self.user.client.Get_response(confirmPasswordRequest)

        if confirmPasswordResponse.startswith("IDENDEFICATION OK"):
            self.show_success_message("Password OK")
            self.hide()
            self.loggedin.emit(True)
        
        else:
            style = "QLineEdit { background-color: #FF9999; }"
            self.password_input.setStyleSheet(style)
            self.show_error_message("Wrong Password")


    #Show specific error message
    def show_error_message(self, message):
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle("Error")
        error_dialog.setText(message)
        error_dialog.move(self.x(), self.y())
        error_dialog.exec_()


    #Show specific success message
    def show_success_message(self, message):
        success_dialog = QMessageBox()
        success_dialog.setIcon(QMessageBox.Information)
        success_dialog.setWindowTitle("Success")
        success_dialog.setText(message)
        success_dialog.move(self.x(), self.y())
        success_dialog.exec_()
        

