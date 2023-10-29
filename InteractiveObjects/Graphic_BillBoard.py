import os
import threading

from datetime import datetime, timedelta

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor

from Entity.Billboard import *
from ServerData.Client import *
from Entity.Schedules import *
from InteractiveObjects.Video_downloader import *
from InteractiveObjects.Video_player import VideoPlayer

class GraphicBillboard(QGraphicsRectItem):
    def __init__(self, x : int, y : int, w : int, h : int, billboard : BillBoard, client : Client):
        super().__init__(x, y, w, h)

        self.billboard = billboard
        self.client = client

        init_time = datetime.fromisoformat(self.client.Get_response("GET_TIME"))

        schedules_request = f"GET GROUP SCHEDULES schedules_name = {self.billboard.schedules_name}"
        schedules_repsnose = self.client.Get_response(schedules_request)

        self.schedules = Schedules(self.billboard.schedules_name)
        self.schedules.fill_from_response(schedules_repsnose)

        self.init_time = init_time

        brush = QBrush(QColor(0, 0, 0, int(255 * 3 / 4)))
        self.setBrush(brush)

        self.setToolTip(self.getToolTip())

        self.video_player = None

        self.setAcceptHoverEvents(True)
        self.setAcceptTouchEvents(True)


    def hoverEnterEvent(self, event):
        self.setToolTip(self.getToolTip())
        super().hoverEnterEvent(event)


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.get_video()

        super().mousePressEvent(event)
    
    
    def getToolTip(self):

        self.current_ad = None

        tmp_init = self.init_time
        self.start_play_time = self.init_time

        start_point = datetime.now()
        if_break = False

        while tmp_init < start_point:
            for ad in self.schedules.ad_queue:
                self.current_ad = ad
                delta_time = timedelta(seconds = ad.ad_duration)
                tmp_init += delta_time
                self.start_play_time += delta_time

                if tmp_init > start_point:
                    if_break = True
                    break

            if if_break:
                break

            self.init_time = tmp_init
    

        text = f"""Group: {self.billboard.billboards_groop_name};\nOwner: {self.billboard.owner_name};\nSchedules: {self.billboard.schedules_name};\nCurrent ad: {self.current_ad.ad_name}."""
        
        return text


    def get_video(self):
        if not os.path.exists(self.current_ad.vidio_url):
            self.video_downloader = VideoDownloader(self.current_ad.vidio_url, self.client)
            self.video_downloader.finished.connect(self.on_download_finished)
            self.video_downloader.start()

        else:
            self.on_download_finished()


    def on_download_finished(self):
        self.video_player = VideoPlayer(self.current_ad.vidio_url)
        time_diffrence = self.current_ad.ad_duration - int((self.start_play_time - datetime.now()).total_seconds())
        print(time_diffrence)
        playback_thread = threading.Thread(target = self.video_player.play, args = (time_diffrence, ))
        playback_thread.start()

