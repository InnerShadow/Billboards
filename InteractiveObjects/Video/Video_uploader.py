from PyQt5.QtCore import QThread, pyqtSignal
from ServerData.Client import Client

#Handle of video uploader action
class VideoUploader(QThread):
    finished = pyqtSignal(str)

    def __init__(self, video_name : str, video_url : str, client : Client):
        super().__init__()

        self.video_name = video_name
        self.video_url = video_url
        self.client = client


    #Uploaed necessary file on server
    def run(self):
        ad_response = self.client.Send_ad(self.video_name, self.video_url)
        self.finished.emit(ad_response)

