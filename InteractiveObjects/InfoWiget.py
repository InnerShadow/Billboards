from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap

class InfoWiget(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    
    def init_ui(self):  
        self.setWindowTitle("Info")

        self.label1 = QLabel(self)
        pixmap1 = QPixmap("Data/My_billboard.jpg")
        self.label1.setPixmap(pixmap1)
        self.text1 = QLabel("My billboard", self)
        
        self.label2 = QLabel(self)
        pixmap2 = QPixmap("Data/Others_billboard.jpg")
        self.label2.setPixmap(pixmap2)
        self.text2 = QLabel("Others Billboard", self)
        
        self.close_button = QPushButton("Close", self)
        self.close_button.clicked.connect(self.close)
        
        layout = QVBoxLayout()
        
        pair1_layout = QHBoxLayout()
        pair2_layout = QHBoxLayout()
        
        pair1_layout.addWidget(self.label1)
        pair1_layout.addWidget(self.text1)
        
        pair2_layout.addWidget(self.label2)
        pair2_layout.addWidget(self.text2)
        
        layout.addLayout(pair1_layout)
        layout.addLayout(pair2_layout)
        
        layout.addWidget(self.close_button)
        
        self.setLayout(layout)

