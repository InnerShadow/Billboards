from PyQt5.QtCore import QThread, pyqtSignal
from ServerData.Client import *

class VideoDownloader(QThread):
    finished = pyqtSignal()

    def __init__(self, video_url : str, client : Client):
        super().__init__()
        self.video_url = video_url
        self.client = client


    def run(self):
        ad_request = f"GET AD ad_path = {self.video_url}"
        ad_response = self.client.Get_response(ad_request)

        with open(self.video_url, 'wb') as file:
            file.write(ad_response)

        self.finished.emit()

