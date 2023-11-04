import re

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox, QPushButton, QMessageBox
from PyQt5.QtCore import pyqtSignal

from InteractiveObjects.ScheduleComposer import ScheduleComposer

from Entity.User import User

class SetScheduleWidget(QWidget):
    set_signal = pyqtSignal(str)

    def __init__(self, user: User, billboard_group : str):
        super().__init__()

        self.user = user
        self.billboard_group = billboard_group
        self.schedules : list[str] = []

        self.init_ui()


    def init_ui(self):
        layout = QVBoxLayout()

        self.setWindowTitle("Set Schedule for Group")

        self.schedule_combo = QComboBox()
        self.create_schedule_button = QPushButton("Create Schedule")
        self.set_schedule_button = QPushButton("Set Schedule")
        self.set_schedule_button.clicked.connect(self.set_schedule)
        self.create_schedule_button.clicked.connect(self.create_schedule)

        layout.addWidget(self.schedule_combo)
        layout.addWidget(self.set_schedule_button)
        layout.addWidget(self.create_schedule_button)

        self.setLayout(layout)
        self.fill_schedules()
        self.resize(225, 30)

    
    def create_schedule(self):
        self.schedule_composer = ScheduleComposer(self.user)
        self.schedule_composer.move(self.x(), self.y())
        self.schedule_composer.show()


    def set_schedule(self):
        selected_schedule = self.schedule_combo.currentText()

        if not selected_schedule:
            self.show_error_message("Please select a schedule.")
            return

        set_request = f"SET SCHEDULE name = {selected_schedule}, FOR GROUP name = {self.billboard_group}"
        set_response = self.user.client.Get_response(set_request)

        if set_response == "Schedules set successfully":
            self.show_success_message(f"Schedule '{selected_schedule}' set for the group.")
            self.set_signal.emit(self.user.login)
            self.hide()

        else:
            self.show_error_message(set_response)


    def clear_schedules(self):
        self.schedules = []
        self.schedule_combo.clear()

    
    def fill_schedules(self):
        schedules_request = f"GET ALL SCHEDULES FOR user = {self.user.login}"
        schedules_response = self.user.client.Get_response(schedules_request)

        schedules_pattern = r'Schedule Name = (\w+(?: \w+)*)'

        for match in re.finditer(schedules_pattern, schedules_response):
            self.schedules.append(match.group(1))

        self.schedule_combo.addItems(self.schedules)

    
    def update_schedules(self):
        self.clear_schedules()
        self.fill_schedules()


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

