import re

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QListWidget, QListWidgetItem, QMenu, QAction

from InteractiveObjects.TransferOwnershipWiget import TransferOwnershipWiget
from Entity.User import User

class OwnerViewer(QWidget):
    def __init__(self, owner_name: str, response : str, billboards_groop_name : str, user : User):
        super().__init__()

        self.owner_name = owner_name
        self.billboards_groop_name = billboards_groop_name
        self.user = user

        self.setWindowTitle("Owner Viewer")
        self.setGeometry(250, 100, 380, 380)

        self.groops : list[str] = []
        self.counts : list[int] = []

        self.deparse_response(response)

        self.init_ui()

        self.show()


    def init_ui(self):
        layout = QVBoxLayout()

        owner_label = QLabel(f"<b><font size='6'>{self.owner_name}</font></b>")
        owner_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(owner_label)

        groups_list = QListWidget(self)
        layout.addWidget(groups_list)

        for group_name, billboard_count in zip(self.groops, self.counts):
            item = QListWidgetItem(f"Group: {group_name}, Num of billboards: {billboard_count}")
            groups_list.addItem(item)

            if self.billboards_groop_name == group_name:
                item.setForeground(QColor(255, 0, 0))

        self.setLayout(layout)

        if self.user.role == 'admin' or self.owner_name == self.user.login:
            groups_list.setContextMenuPolicy(Qt.CustomContextMenu)
            groups_list.customContextMenuRequested.connect(self.show_context_menu)


    def deparse_response(self, response : str):
        response += " "
        pattern = r'Group: (.*?), Billboard_Count: (.*?) '

        matches = re.findall(pattern, response)

        for group, billboard_Count in matches:
            self.groops.append(group)
            self.counts.append(int(billboard_Count))


    def show_context_menu(self, pos):
        list_widget = self.sender()
        item = list_widget.itemAt(pos)

        if item:
            context_menu = QMenu(self)
            transfer_action = QAction("Transfer Ownership", self)
            transfer_action.triggered.connect(self.transfer_ownership)
            context_menu.addAction(transfer_action)
            context_menu.exec_(list_widget.mapToGlobal(pos))


    def transfer_ownership(self):
        self.transferWiget = TransferOwnershipWiget(self.user, self.billboards_groop_name)
        self.transferWiget.move(self.x(), self.y())
        self.transferWiget.show()

        self.transferWiget.transer_signal.connect(self.updateInfo)

    
    def updateInfo(self, new_owner_name: str):
        self.owner_name = new_owner_name
        self.clearInfo()
        self.createInfo()


    def clearInfo(self):
        layout = self.layout()
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()


    def createInfo(self):
        layout = self.layout()

        owner_label = QLabel(f"<b><font size='6'>{self.owner_name}</font></b>")
        owner_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(owner_label)

        groups_list = QListWidget(self)
        layout.addWidget(groups_list)

        for group_name, billboard_count in zip(self.groops, self.counts):
            item = QListWidgetItem(f"Group: {group_name}, Num of billboards: {billboard_count}")
            groups_list.addItem(item)

            if self.billboards_groop_name == group_name:
                item.setForeground(QColor(255, 0, 0))

            if self.user.role == 'admin' or self.owner_name == self.user.login:
                groups_list.setContextMenuPolicy(Qt.CustomContextMenu)
                groups_list.customContextMenuRequested.connect(self.show_context_menu)


