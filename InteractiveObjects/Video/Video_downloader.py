from PyQt5.QtCore import QThread, pyqtSignal
from ServerData.Client import *

from InteractiveObjects.Video.VideoDownloaderWiget import VideoDownloaderWiget

class VideoDownloader(QThread):
    finished = pyqtSignal()

    def __init__(self, video_url : str, client : Client, x : int, y : int):
        super().__init__()
        self.video_url = video_url
        self.client = client

        self.x = x
        self.y = y


    def run(self):
        self.videoDownloaderWiget = VideoDownloaderWiget(self.x, self.y)
        ad_request = f"GET AD ad_path = {self.video_url}"
        ad_response = self.client.Get_response(ad_request)

        with open(self.video_url, 'wb') as file:
            file.write(ad_response)

        self.videoDownloaderWiget.finish_work()

        self.finished.emit()

