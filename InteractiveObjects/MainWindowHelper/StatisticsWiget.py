from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import QTimer

from InteractiveObjects.MainWindowHelper.AdsStatisticsWiget import AdsStatisticsWiget

from Entity.User import User

#Handler of 'Show statistics' button
class StatisticsWiget(QWidget):
    def __init__(self, user : User):
        super().__init__()

        self.user = user

        self.init_ui()

    
    #Init necessary graphics items
    def init_ui(self):
        self.setWindowTitle("Statistics")

        self.label_ads_show = QLabel("Ads show: 0", self)
        self.label_ads_watched = QLabel("Ads watched: 0", self)

        self.button_show_statistics = QPushButton("Show watched ad statistics", self)
        self.button_show_statistics.clicked.connect(self.show_statistics_clicked)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label_ads_show)
        layout.addWidget(self.label_ads_watched)
        layout.addWidget(self.button_show_statistics)
        self.setLayout(layout)

        self.update_ads_counts()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_ads_counts)
        self.timer.start(2000)

        self.resize(200, 75)


    #Ask server about SHOWED and WATCHED ads
    def update_ads_counts(self):
        ads_show_request = f"GET ADS SHOWED"
        ads_show_response = self.user.client.Get_response(ads_show_request)

        ads_watched_request = "GET ADS WATCHED"
        ads_watched_response = self.user.client.Get_response(ads_watched_request)

        ads_show_value = int(ads_show_response)
        ads_watched_value = int(ads_watched_response) 

        self.label_ads_show.setText(f"Ads show: {ads_show_value}")
        self.label_ads_watched.setText(f"Ads watched: {ads_watched_value}")

    
    def show_statistics_clicked(self):
        self.adsStatisticsWiget = AdsStatisticsWiget(self.user)
        self.adsStatisticsWiget.move(self.x(), self.y())
        self.adsStatisticsWiget.show()


    #Perform exit
    def closeEvent(self, event):
        self.timer.stop()
        event.accept()

