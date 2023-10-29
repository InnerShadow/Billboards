import re

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QListWidget, QListWidgetItem

class OwnerViewer(QWidget):
    def __init__(self, owner_name: str, response : str, billboards_groop_name : str):
        super().__init__()

        self.owner_name = owner_name
        self.billboards_groop_name = billboards_groop_name

        self.setWindowTitle("Owner Viewer")
        self.setGeometry(250, 100, 500, 500)

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


    def deparse_response(self, response : str):
        response += " "
        pattern = r'Group: (.*?), Billboard_Count: (.*?) '

        matches = re.findall(pattern, response)

        for group, billboard_Count in matches:
            self.groops.append(group)
            self.counts.append(int(billboard_Count))


