import socket
import sys
from moviepy.editor import VideoFileClip
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import *
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QPalette

def send_number_to_server(number):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('127.0.0.1', 2000))

        client.send(str(number).encode('utf-8'))

        response = b''
        while True:
            data = client.recv(1024)
            if not data:
                break
            response += data

        print(response.decode('utf-8'))
    finally:
        client.close()

if __name__ == '__main__':
    number = 5
    send_number_to_server(number)












class VideoPlayer(QMainWindow):
    def __init__(self, videio_url):
        super().__init__()

        self.videio_url = videio_url

        self.setWindowTitle("Video player")
        self.setGeometry(250, 100, 700, 500)

        p = self.palette()
        p.setColor(QPalette.Window, Qt.black)
        self.setPalette(p)

        self.init_ui()

        self.show()

    
    def init_ui(self):
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        video_widget = QVideoWidget()

        self.hboxLayout = QHBoxLayout()
        self.hboxLayout.setContentsMargins(0, 0, 0, 0)

        central_widget = QWidget() 
        self.setCentralWidget(central_widget)  

        vboxLayout = QVBoxLayout(central_widget)
        vboxLayout.addWidget(video_widget)
        vboxLayout.addLayout(self.hboxLayout)

        self.open_video()

        self.mediaPlayer.setVideoOutput(video_widget)
        

    
    def open_video(self):
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.videio_url)))
        

    def play_video(self):
        self.mediaPlayer.play()

