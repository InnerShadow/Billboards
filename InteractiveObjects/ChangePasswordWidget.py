from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from Entity.User import User

class ChangePasswordWidget(QWidget):
    def __init__(self, user: User):
        super().__init__()
        self.user = user

        self.init_ui()


    def init_ui(self):
        layout = QVBoxLayout()

        self.setWindowTitle("Change Password")

        self.username_label = QLabel(f"<b><font size='6'>{self.user.login}</font></b>")

        self.old_password_input = QLineEdit()
        self.old_password_input.setPlaceholderText("Old Password")
        self.old_password_input.setEchoMode(QLineEdit.Password)

        self.new_password_input = QLineEdit()
        self.new_password_input.setPlaceholderText("New Password")
        self.new_password_input.setEchoMode(QLineEdit.Password)

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirm New Password")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)

        self.change_password_button = QPushButton("Change Password")
        self.change_password_button.clicked.connect(self.change_password)

        layout.addWidget(self.username_label)
        layout.addWidget(self.old_password_input)
        layout.addWidget(self.new_password_input)
        layout.addWidget(self.confirm_password_input)
        layout.addWidget(self.change_password_button)

        self.setLayout(layout)

        self.resize(225, 30)


    def change_password(self):

        fields_to_check = [
            self.old_password_input,
            self.new_password_input,
            self.confirm_password_input,
        ]

        red_style = "QLineEdit { background-color: #FF9999; }"
        white_style = "QLineEdit { background-color: white; }"
        all_fields_valid = True

        for field in fields_to_check:
            if not field.text():
                field.setStyleSheet(red_style)
                all_fields_valid = False
            else:
                field.setStyleSheet(white_style)

        if not all_fields_valid:
            self.show_error_message("Please fill in all fields.")
            return

        old_password = self.old_password_input.text()
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()

        if new_password != confirm_password:
            self.new_password_input.setStyleSheet(red_style)
            self.confirm_password_input.setStyleSheet(red_style)
            self.old_password_input.setStyleSheet(white_style)
            self.show_error_message("New passwords do not match. Please confirm the new password.")
            return

        change_password_request = f"USER name = {self.user.login} CHANGE PASSWORD FROM old = {old_password}, TO new = {new_password}"
        change_password_response = self.user.client.Get_response(change_password_request)

        if change_password_response == "Password updated successfully":
            self.show_success_message("Password changed successfully")
            self.hide()
        
        else :
            self.old_password_input.setStyleSheet(red_style)
            self.new_password_input.setStyleSheet(white_style)
            self.confirm_password_input.setStyleSheet(white_style)
            self.show_error_message(change_password_response)


    def show_error_message(self, message):
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle("Error")
        error_dialog.setText(message)
        error_dialog.move(self.x(), self.y())
        error_dialog.exec_()


    def show_success_message(self, message):
        success_dialog = QMessageBox()
        success_dialog.setIcon(QMessageBox.Information)
        success_dialog.setWindowTitle("Success")
        success_dialog.setText(message)
        success_dialog.move(self.x(), self.y())
        success_dialog.exec_()

