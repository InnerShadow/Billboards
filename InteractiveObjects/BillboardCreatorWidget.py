import re

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox, QPushButton, QLabel, QMessageBox

from InteractiveObjects.GroupComposer import GroupComposer

from Entity.User import User

class BillboardCreatorWidget(QWidget):
    created = pyqtSignal()

    def __init__(self, user: User, x_pos: float, y_pos: float):
        super().__init__()

        self.user = user
        self.x_pos = x_pos
        self.y_pos = y_pos

        self.init_ui()


    def init_ui(self):
        layout = QVBoxLayout()

        self.setWindowTitle("Create Billboard")

        user_label = QLabel("Select User:")
        group_label = QLabel("Select Group:")

        self.user_combo = QComboBox()
        self.group_combo = QComboBox()

        create_group_button = QPushButton("Create Group") 

        create_button = QPushButton("Create Billboard")

        self.user_combo.currentIndexChanged.connect(self.update_group_combo)
        create_button.clicked.connect(self.create_billboard)
        create_group_button.clicked.connect(self.createGroup)

        layout.addWidget(user_label)
        layout.addWidget(self.user_combo)
        layout.addWidget(group_label)
        layout.addWidget(self.group_combo)

        layout.addWidget(create_group_button)
        layout.addWidget(create_button)

        self.fill_user_combo()

        self.setLayout(layout)

        self.resize(300, 150) 


    def fill_user_combo(self):
        user_list = self.get_user_list()
        self.user_combo.addItems(user_list)


    def update_group_combo(self):
        selected_user = self.user_combo.currentText()
        group_list = self.get_group_list(selected_user)

        self.group_combo.clear()
        self.group_combo.addItems(group_list)


    def create_billboard(self):
        selected_user = self.user_combo.currentText()
        selected_group = self.group_combo.currentText()

        create_request = f"CREATE NEW BILLBOARD FOR user = {selected_user} IN group = {selected_group} x_pos = {self.x_pos}, y_pos = {self.y_pos}"
        create_response = self.user.client.Get_response(create_request)

        if create_response == "Billboard created successfully" or create_response == "Ownership relationship already exists":
            self.show_success_message("Billboard created successfully")
            self.hide()
            self.created.emit()

        else:
            self.show_error_message(create_response)


    def get_user_list(self):
        owners_request = "GET OWNERS"
        owners_response = self.user.client.Get_response(owners_request) + " "
        owners_pattern = r'Owner name = (\w+)'

        users_list = []

        for match in re.finditer(owners_pattern, owners_response):
            users_list.append(match.group(1))

        return users_list


    def get_group_list(self, selected_user):
        groops_request = f"GET ALL GROOPS for user = {selected_user}"
        groups_response = self.user.client.Get_response(groops_request)

        groups_pattern = r'Group Name = (\w+(?: \w+)*)'

        groops_list = []

        for match in re.finditer(groups_pattern, groups_response):
            groops_list.append(match.group(1))

        return groops_list


    def createGroup(self):
        self.groupComposer = GroupComposer(self.user)
        self.groupComposer.move(self.x(), self.y())
        self.groupComposer.show()
        self.groupComposer.accepted.connect(self.update_group_combo)


    def show_error_message(self, message):
        error_dialog = QMessageBox(self)
        error_dialog.setWindowTitle('Error')
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setText(message)
        error_dialog.addButton(QMessageBox.Ok)
        error_dialog.move(self.x(), self.y())
        error_dialog.exec_()


    def show_success_message(self, message):
        success_dialog = QMessageBox(self)
        success_dialog.setWindowTitle('Success')
        success_dialog.setIcon(QMessageBox.Information)
        success_dialog.setText(message)
        success_dialog.addButton(QMessageBox.Ok)
        success_dialog.move(self.x(), self.y())
        success_dialog.exec_()

