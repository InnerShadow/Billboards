import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
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

        rectangles = [
            (200, 200, 150, 80)
        ]

        for rect in rectangles:
            x, y, w, h = rect
            item = QGraphicsRectItem(x, y, w, h)
            item.setBrush(Qt.black)
            self.scene.addItem(item)

        self.show()

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
