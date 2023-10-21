from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PyQt5.QtCore import Qt

from ServerData.Client import *

class MainWindow(QMainWindow):

    billboard_w = 75
    billboard_h = 40

    def __init__(self):
        super().__init__()

        self.initUI()

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
        client.send_number_to_server(5)

        rectangles = [
            (200, 200, self.billboard_w, self.billboard_h)
        ]

        for rect in rectangles:
            x, y, w, h = rect
            item = QGraphicsRectItem(x, y, w, h)
            item.setBrush(Qt.black)
            self.scene.addItem(item)

        self.show()
