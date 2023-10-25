from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
import re

from ServerData.Client import *

class MainWindow(QMainWindow):

    billboard_w = 75
    billboard_h = 40

    def __init__(self):
        super().__init__()

        self.initUI()

    
    def parse_billboards(self, response_text):
        pattern = r'X: (\d+), Y: (\d+)'
        matches = re.findall(pattern, response_text)

        coordinates = [(int(x) / 1000, int(y) / 1000) for x, y in matches]
        return coordinates


    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('BillBoards')

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
        client = Client('127.0.0.1', 2000)
        bg_width = self.view.viewport().width()
        bg_height = self.view.viewport().height()
        self.background_item.setPixmap(self.background_image.scaled(bg_width, bg_height, Qt.KeepAspectRatio))

        for item in self.scene.items():
            if isinstance(item, QGraphicsRectItem):
                self.scene.removeItem(item)

        billboards_positions = self.parse_billboards(client.Get_Billboards('GET_BILLBOARDS'))
        for x, y in billboards_positions:
            x = int(x * bg_width)
            y = int(y * bg_height)

            rect = QRect(x, y, self.billboard_w, self.billboard_h)
            scaled_rect = rect.intersected(self.background_item.boundingRect().toRect())
            x, y, w, h = scaled_rect.x(), scaled_rect.y(), scaled_rect.width(), scaled_rect.height()
            item = QGraphicsRectItem(x, y, w, h)
            item.setBrush(Qt.black)
            self.scene.addItem(item)
