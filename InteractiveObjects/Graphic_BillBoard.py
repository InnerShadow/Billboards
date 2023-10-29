from datetime import datetime, timedelta

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsItem

from Entity.Billboard import *
from ServerData.Client import *
from Entity.Schedules import *

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

        self.setBrush(Qt.black)
        self.setToolTip(self.getToolTip())

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

        start_point = datetime.now()
        if_break = False

        while tmp_init < start_point:
            for ad in self.schedules.ad_queue:
                self.current_ad = ad
                delta_time = timedelta(seconds = ad.ad_duration)
                tmp_init += delta_time

                if tmp_init > start_point:
                    if_break = True
                    break

            if if_break:
                break

            self.init_time = tmp_init
    

        text = f"""Group: {self.billboard.billboards_groop_name};\nOwner: {self.billboard.owner_name};\nSchedules: {self.billboard.schedules_name};\nCurrent ad: {self.current_ad.ad_name}."""
        
        return text


    def get_video(self):
        ad_request = f"GET AD ad_path = {self.current_ad.vidio_url}"
        ad_repsnose = self.client.Get_response(ad_request)

        with open(self.current_ad.vidio_url, 'wb') as file:
            file.write(ad_repsnose)

        pass