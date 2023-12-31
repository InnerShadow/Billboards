import re

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QComboBox, QMessageBox

from Entity.User import User
from Entity.Billboard import BillBoard
from InteractiveObjects.MainWindowHelper.GroupComposer import GroupComposer

#Wiget of billboard movment to other group
class BillboardGroupManager(QWidget):
    def __init__(self, user : User, billboard : BillBoard):
        super().__init__()

        self.user = user
        self.billboard = billboard
        self.groups : list[str]= []

        self.init_ui()


    #Init all graphics items
    def init_ui(self):
        layout = QVBoxLayout()

        self.setWindowTitle("Move a billboard")

        self.group_combo = QComboBox()
        self.move_button = QPushButton("Move Billboard")
        self.create_group_button = QPushButton("Create New Group")

        layout.addWidget(self.group_combo)
        layout.addWidget(self.create_group_button)
        layout.addWidget(self.move_button)

        self.group_combo.addItem("Select a group")
        self.group_combo.setCurrentText("Select a group")

        self.move_button.clicked.connect(self.move_billboard)
        self.create_group_button.clicked.connect(self.create_new_group)
        self.fill_groups()

        self.setLayout(layout)

        self.resize(225, 30)


    #perform movment
    def move_billboard(self):
        move_to = self.group_combo.currentText()

        if move_to == "Select a group":
            self.show_error_message("Please select a group.")
            return
        
        move_request = f"MOVE BILLBOARDS x = {self.billboard.x_pos}, y = {self.billboard.y_pos} TO GROUP name = {move_to}"
        move_response = self.user.client.Get_response(move_request)

        if move_response == "Billboard moved successfully":
            self.show_success_message(move_response)
            self.hide()

        else:
            self.show_error_message(move_response)


    #If user want to greate new group show specific wiget
    def create_new_group(self):
        self.schedule_composer = GroupComposer(self.user)
        self.schedule_composer.move(self.x(), self.y())
        self.schedule_composer.accepted.connect(self.update_groops)
        self.schedule_composer.show()


    #Update info if new group was created
    def update_groops(self):
        self.clearGroops()
        self.fill_groups()


    #Clwar all groups befor update them
    def clearGroops(self):
        self.groups = []
        self.group_combo.clear()


    #Ask server to get all groups fot this user and groups for Noone
    def fill_groups(self):
        groops_request = f"GET ALL GROOPS for user = {self.user.login}"
        groups_response = self.user.client.Get_response(groops_request)

        groups_pattern = r'Group Name = (\w+(?: \w+)*)'

        for match in re.finditer(groups_pattern, groups_response):
            self.groups.append(match.group(1))

        self.group_combo.addItems(self.groups)


    #Show specific error window
    def show_error_message(self, message):
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle("Error")
        error_dialog.setText(message)
        error_dialog.move(self.x(), self.y())
        error_dialog.exec_()


    #Show specific success mwssage
    def show_success_message(self, message):
        success_dialog = QMessageBox()
        success_dialog.setIcon(QMessageBox.Information)
        success_dialog.setWindowTitle("Success")
        success_dialog.setText(message)
        success_dialog.move(self.x(), self.y())
        success_dialog.exec_()

