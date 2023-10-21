from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PyQt5.QtCore import Qt
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

        coordinates = [(int(x), int(y)) for x, y in matches]
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

        client = Client('127.0.0.1', 2000)
        billboards_positions = self.parse_billboards(client.Get_Billboards('GET_BILLBOARDS'))

        rectangles = []
        for i in billboards_positions:
            rectangles.append(i + (self.billboard_w, self.billboard_h))

        for rect in rectangles:
            x, y, w, h = rect
            item = QGraphicsRectItem(x, y, w, h)
            item.setBrush(Qt.black)
            self.scene.addItem(item)

        self.show()
