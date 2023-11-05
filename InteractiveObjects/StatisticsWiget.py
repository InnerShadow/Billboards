from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import QTimer

from Entity.User import User

class StatisticsWiget(QWidget):
    def __init__(self, user : User):
        super().__init__()

        self.user = user

        self.init_ui()

    
    def init_ui(self):
        self.setWindowTitle("Statistics")

        self.label_ads_show = QLabel("Ads show: 0", self)
        self.label_ads_watched = QLabel("Ads watched: 0", self)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label_ads_show)
        layout.addWidget(self.label_ads_watched)
        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_ads_counts)
        self.timer.start(2000)

        self.resize(200, 75)


    def update_ads_counts(self):
        ads_show_value = 42
        ads_watched_value = 15 

        self.label_ads_show.setText(f"Ads show: {ads_show_value}")
        self.label_ads_watched.setText(f"Ads watched: {ads_watched_value}")

