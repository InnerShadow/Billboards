import re

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem, QHBoxLayout, QMenu, QMessageBox

from InteractiveObjects.MainWindowHelper.InsertAdDialog import InsertAdDialog

from Entity.User import User
from Entity.Schedules import Schedules

#Edit schedule helper
class ScheduleEditor(QWidget):
    def __init__(self, user: User, schedules : Schedules):
        super().__init__()
        self.ads = []
        self.user = user
        self.schedules = schedules

        self.schedule_list = QListWidget()
        self.add_button = QPushButton("Add ad")
        self.remove_button = QPushButton("Remove last ad")
        self.save_button = QPushButton("Save changes")

        self.init_ui()


    #Init all graphics objects
    def init_ui(self):
        layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        self.setWindowTitle(f"Edit Schedule: {self.schedules.schedules_name}")

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.remove_button)

        layout.addWidget(self.schedule_list)
        layout.addLayout(button_layout)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

        self.add_button.clicked.connect(self.add_advertisement)
        self.remove_button.clicked.connect(self.remove_advertisement)
        self.save_button.clicked.connect(self.save_changes)

        self.schedule_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.schedule_list.customContextMenuRequested.connect(self.show_context_menu)

        self.get_ads()
        self.fill_schedule()


    #All ad helper manegment
    def show_context_menu(self, point):
        selected_item = self.schedule_list.itemAt(point)
        if selected_item:
            menu = QMenu(self)
            add_below_action = menu.addAction("Add Ad Below")
            delete_action = menu.addAction("Delete Current Item")

            action = menu.exec_(self.schedule_list.mapToGlobal(point))

            if action == add_below_action:
                self.add_advertisement_below(selected_item)
            elif action == delete_action:
                self.delete_advertisement(selected_item)


    #Get all posible ads from the server
    def get_ads(self):
        ads_request = "GET ALL ADS"
        ads_response = self.user.client.Get_response(ads_request)

        ads_pattern = r'Ad = (\w+(?: \w+)*)'

        for match in re.finditer(ads_pattern, ads_response):
            self.ads.append(match.group(1))


    #Fill current schedule
    def fill_schedule(self):
        for ad in self.schedules.ad_queue:
            item = QListWidgetItem(ad.ad_name)
            self.schedule_list.addItem(item)


    #Add advertisement below option
    def add_advertisement_below(self, selected_item):
        if self.ads:
            selected_ad, ok = InsertAdDialog(self.ads, self.user).get_selected_advertisement(self.ads, self.user)
            if ok:
                item = QListWidgetItem(selected_ad)
                if item.text() != '':
                    row = self.schedule_list.row(selected_item)
                    self.schedule_list.insertItem(row + 1, item)


    #Delete advertisement option
    def delete_advertisement(self, selected_item):
        row = self.schedule_list.row(selected_item)
        if row != -1:
            self.schedule_list.takeItem(row)

    
    #Button add ad handler
    def add_advertisement(self):
        if self.ads:
            selected_ad, ok = InsertAdDialog(self.ads, self.user).get_selected_advertisement(self.ads, self.user)
            if ok:
                item = QListWidgetItem(selected_ad)
                if item.text() != '':
                    self.schedule_list.addItem(item)


    #Button remove last add handler
    def remove_advertisement(self):
        if self.schedule_list.count() > 0:
            item = self.schedule_list.takeItem(self.schedule_list.count() - 1)
            if item:
                del item

    
    #Save current schedule and tell server about it
    def save_changes(self):
        schedule = [self.schedule_list.item(i).text() for i in range(self.schedule_list.count())]
        if not schedule:
            self.show_error_message("Please add at least one advertisement to the schedule.")
            return

        editRequest = f"EDIT SCHEDULES schedules_name = {self.schedules.schedules_name} \n"
        for i in range(len(schedule)):
            editRequest += f"ad_preority = {i}, ad_name = {schedule[i]} \n "

        schedules_response = self.user.client.Get_response(editRequest)

        if schedules_response == "Schedule updated successfully":
            self.show_success_message(schedules_response)
            self.hide()
        
        else:
            self.show_error_message(schedules_response)


    #Show specific error message box
    def show_error_message(self, message):
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle("Error")
        error_dialog.setText(message)
        error_dialog.move(self.x(), self.y())
        error_dialog.exec_()


    #Show specific success message box
    def show_success_message(self, message):
        success_dialog = QMessageBox()
        success_dialog.setIcon(QMessageBox.Information)
        success_dialog.setWindowTitle("Success")
        success_dialog.setText(message)
        success_dialog.move(self.x(), self.y())
        success_dialog.exec_()


