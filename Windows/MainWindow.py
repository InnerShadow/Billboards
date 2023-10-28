from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
import re

from ServerData.Client import *
from Entity.BillBoard_groop import *

class MainWindow(QMainWindow):

    billboard_w = 75
    billboard_h = 40

    billboards_groops = []

    def __init__(self):
        super().__init__()
        self.initClient()
        self.initBillboards()
        self.initUI()


    def initClient(self):
        self.client = Client('127.0.0.2', 2000)
        #print(self.client.get_ip_address())


    def initBillboards(self):
        groop_pattern = r'Group: ([\w\s_]+), Owner: [\w\s_]+, Schedule: ([\w\s_]+)'
        response = self.client.Get_Billboards('GET_BILLBOARDS')

        for match in re.finditer(groop_pattern, response):
            groop_name = match.group(1)
            schedules = match.group(2)
            groop = BillBoard_groop(groop_name, schedules)

            if_add = True

            for i in self.billboards_groops:
                if i.groop_name == groop_name and i.schedules == schedules:
                    if_add = False

            if if_add:
                self.billboards_groops.append(groop)


        for i in self.billboards_groops:
            i.fill_BillBoards(response)
            


    def initUI(self):
        self.setWindowTitle('BillBoards')
        self.setWindowState(Qt.WindowFullScreen)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)

        self.view = QGraphicsView()
        layout.addWidget(self.view)

        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)

        self.background_image = QPixmap('Data/Jodino.png')
        self.background_item = QGraphicsPixmapItem(self.background_image)
        self.background_item.setZValue(0)
        self.scene.addItem(self.background_item)

        self.resizeEvent = self.handleResize

        self.updateGraphicsItems()

        self.show()


    @pyqtSlot()
    def handleResize(self, event):
        self.updateGraphicsItems()


    def updateGraphicsItems(self):
        bg_width = self.view.viewport().width()
        bg_height = self.view.viewport().height()
        self.background_item.setPixmap(self.background_image.scaled(bg_width, bg_height, Qt.KeepAspectRatio))

        for item in self.scene.items():
            if isinstance(item, QGraphicsRectItem):
                self.scene.removeItem(item)

        # for x, y in self.billboards_positions:
        #     x = int(x * bg_width)
        #     y = int(y * bg_height)

        #     rect = QRect(x, y, self.billboard_w, self.billboard_h)
        #     scaled_rect = rect.intersected(self.background_item.boundingRect().toRect())
        #     x, y, w, h = scaled_rect.x(), scaled_rect.y(), scaled_rect.width(), scaled_rect.height()
        #     item = QGraphicsRectItem(x, y, w, h)
        #     item.setBrush(Qt.black)
        #     self.scene.addItem(item)
