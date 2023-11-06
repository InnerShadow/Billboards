import re

from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QMessageBox
from PyQt5.QtCore import pyqtSignal

from InteractiveObjects.MainWindowHelper.PasswordDialog import PasswordDialog

from Entity.User import User

#Handler of users deletion
class DeleteUserWidget(QWidget):
    deleted = pyqtSignal()

    def __init__(self, user : User):
        super().__init__()

        self.user = user

        self.initUI()


    #Init all necessary graphics items
    def initUI(self):
        layout = QVBoxLayout()

        self.setWindowTitle("Delete User")

        user_label = QLabel("Select User to Delete:")
        self.user_combobox = QComboBox()

        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Cancel")

        self.fillCombo()

        ok_button.clicked.connect(self.confirm_delete)
        cancel_button.clicked.connect(self.cancel_clicked)

        layout.addWidget(user_label)
        layout.addWidget(self.user_combobox)

        button_layout = QHBoxLayout()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)


    #Ask server about all usres and fill como box
    def fillCombo(self):
        getUsersRequest = f"GET ALL USERS"
        getUsersResponse = self.user.client.Get_response(getUsersRequest)

        users_pattern = r'User name = (\w+)'

        user_list: list[str] = []

        for match in re.finditer(users_pattern, getUsersResponse):
            name = match.group(1)
            if name != self.user.login:
                user_list.append(name)

        self.user_combobox.addItems(user_list)


    #Ask admin about password to delete some one
    def confirm_delete(self):
        self.selected_user = self.user_combobox.currentText()
        self.passwordDialog = PasswordDialog(self, self.selected_user, self.user)
        self.passwordDialog.move(self.x(), self.y())
        self.passwordDialog.show()

        self.passwordDialog.loggedin.connect(self.doDelite)

    
    #Perform deletion)
    def doDelite(self, loggedin : bool):
        if loggedin:
            deleteRequest = f"DELETE USER name = {self.selected_user}"
            _ = self.user.client.Get_response(deleteRequest)
            self.show_success_message(f"User {self.selected_user} has been deleted)")
            self.hide()
            self.deleted.emit()

    
    #Show specific success message
    def show_success_message(self, message):
        success_dialog = QMessageBox()
        success_dialog.setIcon(QMessageBox.Information)
        success_dialog.setWindowTitle("Success")
        success_dialog.setText(message)
        success_dialog.move(self.x(), self.y())
        success_dialog.exec_()
        

    #Handle close button clicked
    def cancel_clicked(self):
        self.close()

