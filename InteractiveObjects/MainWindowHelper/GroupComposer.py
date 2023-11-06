import re
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox
from Entity.User import User
from InteractiveObjects.MainWindowHelper.ScheduleComposer import ScheduleComposer

class GroupComposer(QWidget):
    accepted = pyqtSignal()

    def __init__(self, user: User):
        super().__init__()
        
        self.user = user
        self.schedules : list[str] = []

        self.init_ui()
    
    
    def init_ui(self):
        layout = QVBoxLayout()

        self.setWindowTitle("Create group")
        group_name_label = QLabel("Group Name:")
        self.group_name_input = QLineEdit()
        
        schedules_label = QLabel("Select Schedule:")
        self.schedule_combo = QComboBox()
        self.schedule_combo.addItem("Select a schedule")

        self.load_schedules()

        create_schedule_button = QPushButton("Create New Schedule")
        create_schedule_button.clicked.connect(self.create_new_schedule)

        create_group_button = QPushButton("Create Group")
        create_group_button.clicked.connect(self.create_group)

        layout.addWidget(group_name_label)
        layout.addWidget(self.group_name_input)
        layout.addWidget(schedules_label)
        layout.addWidget(self.schedule_combo)
        layout.addWidget(create_schedule_button)
        layout.addWidget(create_group_button)

        self.setLayout(layout)
    

    def load_schedules(self):
        schedules_request = "GET ALL SCHEDULES"
        schedules_response = self.user.client.Get_response(schedules_request)
        
        schedules_pattern = r'Schedule Name = (\w+(?: \w+)*)'
        
        for match in re.finditer(schedules_pattern, schedules_response):
            self.schedules.append(match.group(1))
            self.schedule_combo.addItem(match.group(1))


    def update_schedules(self):
        self.clear_schedules()
        self.load_schedules()


    def clear_schedules(self):
        self.schedules = []
        self.schedule_combo.clear()
    

    def create_new_schedule(self):
        self.schedule_composer = ScheduleComposer(self.user)
        self.schedule_composer.move(self.x(), self.y())
        self.schedule_composer.accepted.connect(self.update_schedules)
        self.schedule_composer.show()
    

    def create_group(self):
        group_name = self.group_name_input.text().strip()
        if not group_name:
            self.show_error_message("Please enter a group name.")
            return
        
        schedule_name = self.schedule_combo.currentText()
        if schedule_name == "Select a schedule":
            self.show_error_message("Please select or create a schedule.")
            return
        
        create_request = f"GET CREATE GROUP group_name = {group_name}, schedule_name = {schedule_name}"
        create_response = self.user.client.Get_response(create_request)

        if create_response == "Group created successfully":
            self.show_success_message("Group created successfully.")
            self.hide()
            self.accepted.emit()
        
        else:
            self.show_error_message(create_response)
    

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

