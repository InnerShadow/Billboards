from PyQt5.QtWidgets import QVBoxLayout, QListWidget, QDialog, QDialogButtonBox, QLineEdit
from Entity.User import User

#Handler of add ad button
class InsertAdDialog(QDialog):
    def __init__(self, advertisement_names : list[str], user : User):
        super().__init__()

        self.user = user
        self.advertisement_names = advertisement_names
        self.selected_ad = None

        self.init_ui()
        self.show()


    #Init all necessary graphics items
    def init_ui(self):
        layout = QVBoxLayout()

        self.ad_list = QListWidget()
        self.ad_list.addItems(self.advertisement_names)
        self.ad_list.itemDoubleClicked.connect(self.select_advertisement)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Find ad")
        self.search_input.textChanged.connect(self.filter_advertisements)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addWidget(self.search_input)
        layout.addWidget(self.ad_list)
        layout.addWidget(button_box)

        self.setLayout(layout)
        self.setWindowTitle("Choose ad")


    #Handle selected ad
    def select_advertisement(self, item):
        self.selected_ad = item.text()
        self.accept()


    #Perform filter
    def filter_advertisements(self):
        search_text = self.search_input.text().lower()
        self.ad_list.clear()
        matching_ads = [ad for ad in self.advertisement_names if search_text in ad.lower()]
        self.ad_list.addItems(matching_ads)


    #Static ad creation method
    @staticmethod
    def get_selected_advertisement(advertisement_names : str, user : User):
        dialog = InsertAdDialog(advertisement_names, user)
        dialog.ad_list.itemActivated.connect(dialog.select_advertisement)
        result = dialog.exec_()
        return dialog.selected_ad, result == QDialog.Accepted

