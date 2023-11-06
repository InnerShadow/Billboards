from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar

class VideoDownloaderWiget(QWidget):
    def __init__(self, x : int, y : int):
        super().__init__()

        self.x_pos = x
        self.y_pos = y

        self.init_ui()
        self.move(self.x_pos + 160, self.y_pos - 80)
        self.show()

    
    def init_ui(self):
        layout = QVBoxLayout()
        self.progress_label = QLabel('Downloading video...')
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)

        layout.addWidget(self.progress_label)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.activateWindow()


    def finish_work(self):
        self.progress_label.setText('Download complete')
        self.progress_bar.setRange(0, 1)
        self.progress_bar.setValue(1)
        self.hide()
        
