import re

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem

from Entity.User import User

class AdsStatisticsWiget(QWidget):
    def __init__(self, user : User):
        super().__init__()

        self.user = user

        self.init_ui()


    def init_ui(self):
        self.setWindowTitle("Ads statistics")

        self.list_widget = QListWidget(self)

        self.fill_list()

        layout = QVBoxLayout(self)
        layout.addWidget(self.list_widget)
        self.setLayout(layout)


    def fill_list(self):
        ads_request = f"GET_ADS STATISTICS"
        ads_response = self.user.client.Get_response(ads_request)

        ads_pattern = r'AD name = (\w+), views = (\w+)'

        ads_list: list[str] = []

        for match in re.finditer(ads_pattern, ads_response):
            ad_name = match.group(1)
            views = int(match.group(2))
            ads_list.append((ad_name, views))

        sorted_ads_list = sorted(ads_list, key=lambda x: x[1], reverse=True)

        sorted_ads_strings = [f"Ad {ad_name} was watched {views} times" for ad_name, views in sorted_ads_list]

        self.list_widget.addItems(sorted_ads_strings)


