from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar

#Simply 'Downloading...' object
class VideoDownloaderWiget(QWidget):
    def __init__(self, x : int, y : int):
        super().__init__()

        self.x_pos = x
        self.y_pos = y

        self.init_ui()
        self.move(self.x_pos + 160, self.y_pos - 80)
        self.show()

    
    #Init necessary graphics items
    def init_ui(self):
        layout = QVBoxLayout()

        self.setWindowTitle("Downloading...")

        self.progress_label = QLabel('Downloading video...')
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)

        layout.addWidget(self.progress_label)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.activateWindow()


    #Close when downloading finished
    def finish_work(self):
        self.progress_label.setText('Download complete')
        self.progress_bar.setRange(0, 1)
        self.progress_bar.setValue(1)
        self.hide()
        
