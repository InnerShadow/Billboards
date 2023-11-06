from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QWidget
from PyQt5.QtGui import QColor

from Entity.Schedules import Schedules
from Entity.Ad import Ad

#Wuget that helps show actual schedule
class ScheduleViewer(QWidget):
    def __init__(self, schedules : Schedules, current_ad : Ad):
        super().__init__()

        self.schedules = schedules
        self.current_ad = current_ad

        self.setWindowTitle(f"{schedules.schedules_name} schedule")
        self.setGeometry(250, 100, 380, 380)

        self.init_ui()

        self.show()


    #Init all necessary graphics items
    def init_ui(self):
        list_widget = QListWidget(self)
        list_widget.setGeometry(10, 10, 380, 380)

        for ad in self.schedules.ad_queue:
            item = QListWidgetItem(f"Ad Name: {ad.ad_name}, Duration: {ad.ad_duration} seconds")
            list_widget.addItem(item)

            if ad != self.current_ad:
                item.setForeground(QColor(128, 128, 128))


        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.activateWindow()

