import re
from functools import partial

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QCompleter, QDialog, QPushButton, QMessageBox
from PyQt5.QtCore import pyqtSignal

from Entity.User import User

class TransferOwnershipWiget(QWidget):
    transer_signal = pyqtSignal(str, str)

    def __init__(self, user: User, billboards_group : str):
        super().__init__()

        self.user = user
        self.billboards_group = billboards_group
        self.user_list: list[str] = []

        self.init_ui()


    def init_ui(self):
        layout = QVBoxLayout()

        self.setWindowTitle('Transfer Ownership')
        self.user_label = QLabel('Select User:')
        self.user_lineedit = QLineEdit()

        owners_request = "GET OWNERS"
        owners_response = self.user.client.Get_response(owners_request) + " "
        owners_pattern = r'Owner name = (\w+)'

        for match in re.finditer(owners_pattern, owners_response):
            name = match.group(1)
            if name != self.user.login:
                self.user_list.append(name)

        completer = QCompleter(self.user_list)
        self.user_lineedit.setCompleter(completer)
        #self.user_lineedit.returnPressed.connect(partial(self.confirm_transfer_ownership, '', ''))

        self.ok_button = QPushButton('OK')
        self.ok_button.clicked.connect(self.show_confirmation_dialog)

        layout.addWidget(self.user_label)
        layout.addWidget(self.user_lineedit)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.activateWindow()


    def show_error_message(self, message):
        error_dialog = QMessageBox(self)
        error_dialog.setWindowTitle('Error')
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setText(message)
        error_dialog.addButton(QMessageBox.Ok)
        error_dialog.exec_()


    def show_success_message(self, message):
        success_dialog = QMessageBox(self)
        success_dialog.setWindowTitle('Success')
        success_dialog.setIcon(QMessageBox.Information)
        success_dialog.setText(message)
        success_dialog.addButton(QMessageBox.Ok)
        success_dialog.exec_()
        

    def show_confirmation_dialog(self):
        selected_user = self.user_lineedit.text()

        dialog = QDialog(self)
        dialog.setWindowTitle('Transfer Ownership Confirmation')

        label = QLabel(f'Are you sure you want to transfer ownership to {selected_user}?')
        dialog.layout = QVBoxLayout()
        dialog.layout.addWidget(label)

        confirm_button = QPushButton('Confirm')
        cancel_button = QPushButton('Cancel')

        confirm_button.clicked.connect(lambda: self.confirm_transfer_ownership(selected_user, dialog))
        cancel_button.clicked.connect(dialog.reject)

        dialog.layout.addWidget(confirm_button)
        dialog.layout.addWidget(cancel_button)
        dialog.setLayout(dialog.layout)

        dialog.exec_()


    def confirm_transfer_ownership(self, selected_user : str, dialog):
        if selected_user in self.user_list:
            transfer_request = f"TRANSFER OWNERSHIP OF {self.billboards_group} TO {selected_user}"
            _ = self.user.client.Get_response(transfer_request)
            self.show_success_message('Ownership transferred successfully.')
            dialog.accept()
            self.transer_signal.emit(selected_user, self.billboards_group)
            self.hide()

        else:
            self.show_error_message('Selected user not found.')

