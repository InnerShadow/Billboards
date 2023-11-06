from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QComboBox, QMessageBox

from Entity.User import User

class CreateUserWidget(QWidget):
    created = pyqtSignal()

    def __init__(self, user : User):
        super().__init__()

        self.user = user

        self.initUI()


    def initUI(self):
        layout = QVBoxLayout()

        name_label = QLabel("Name:")
        self.name_input = QLineEdit()

        password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.setWindowTitle("Crete user")

        role_label = QLabel("Role:")
        self.role_combobox = QComboBox()
        self.role_combobox.addItems(["viewer", "owner", "admin"])

        create_button = QPushButton("Create User")

        create_button.clicked.connect(self.create_user_clicked)

        form_layout = QVBoxLayout()
        form_layout.addWidget(name_label)
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(role_label)
        form_layout.addWidget(self.role_combobox)

        layout.addLayout(form_layout)
        layout.addWidget(create_button)

        self.setLayout(layout)


    def create_user_clicked(self):
        name = self.name_input.text()
        password = self.password_input.text()
        role = self.role_combobox.currentText()

        createUserRequest = f"RESIGTER USER login = {name}, password = {password}, role = {role}"
        createUserResponse = self.user.client.Get_response(createUserRequest)

        self.show_success_message(createUserResponse)


    def show_success_message(self, message):
        success_dialog = QMessageBox()
        success_dialog.setIcon(QMessageBox.Information)
        success_dialog.setWindowTitle("Success")
        success_dialog.setText(message)
        success_dialog.exec_()
        self.hide()
        self.created.emit()
        
