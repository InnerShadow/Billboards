from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import QTimer

from Entity.User import User

#Handler of 'Show statistics' button
class StatusBarWiget(QWidget):
    def __init__(self, user : User):
        super().__init__()

        self.user = user

        self.init_ui()

    
    #Init necessary graphics items
    def init_ui(self):
        self.setWindowTitle("Status Bar")

        self.label_total_users = QLabel("Total Users: 0", self)
        self.label_total_billboards = QLabel("Total billboards: 0", self)
        self.label_uoloaded_files = QLabel("Total uploaded files: 0", self)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label_total_users)
        layout.addWidget(self.label_total_billboards)
        layout.addWidget(self.label_uoloaded_files)
        self.setLayout(layout)

        self.update_status_bar_counts()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_status_bar_counts)
        self.timer.start(2000)

        self.resize(200, 75)


    #Ask server about all necessary data
    def update_status_bar_counts(self):
        users_request = f"GET TOTAL USERS"
        users_response = self.user.client.Get_response(users_request)

        billboards_request = "GET TOTAL BILLBOARDS"
        billboards_response = self.user.client.Get_response(billboards_request)

        files_request = "GET ALL UPLOADED FILES"
        files_response = self.user.client.Get_response(files_request)

        total_users = int(users_response)
        total_billboards = int(billboards_response) 
        total_files = int(files_response)

        self.label_total_users.setText(f"Total Users: {total_users}")
        self.label_total_billboards.setText(f"Total billboards: {total_billboards}")
        self.label_uoloaded_files.setText(f"Total uploaded files: {total_files}")


    #Perform exit
    def closeEvent(self, event):
        self.timer.stop()
        event.accept()

