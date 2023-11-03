from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem, QHBoxLayout

from InteractiveObjects.InsertAdDialog import InsertAdDialog

class ScheduleComposer(QWidget):
    def __init__(self, advertisement_names):
        super().__init__()

        self.advertisement_names = advertisement_names
        self.schedule_list = QListWidget()
        self.add_button = QPushButton("Add ad")
        self.remove_button = QPushButton("Remove last add")
        self.save_button = QPushButton("Save schedules")

        self.init_ui()


    def init_ui(self):
        layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.remove_button)

        layout.addWidget(self.schedule_list)
        layout.addLayout(button_layout)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

        self.add_button.clicked.connect(self.add_advertisement)
        self.remove_button.clicked.connect(self.remove_advertisement)
        self.save_button.clicked.connect(self.save_schedule)


    def add_advertisement(self):
        if self.advertisement_names:
            selected_ad, ok = InsertAdDialog.get_selected_advertisement(self.advertisement_names)
            if ok:
                item = QListWidgetItem(selected_ad)
                if item.text() != '':
                    self.schedule_list.addItem(item)


    def remove_advertisement(self):
        if self.schedule_list.count() > 0:
            item = self.schedule_list.takeItem(self.schedule_list.count() - 1)
            if item:
                del item


    def save_schedule(self):
        schedule = [self.schedule_list.item(i).text() for i in range(self.schedule_list.count())]
        print(schedule)

