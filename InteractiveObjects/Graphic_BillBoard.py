from datetime import datetime, timedelta

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

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
        
    
    def getToolTip(self):

        current_ad = None

        tmp_init = self.init_time

        start_point = datetime.now()
        if_break = False

        while tmp_init < start_point:
            for ad in self.schedules.ad_queue:
                current_ad = ad.ad_name
                delta_time = timedelta(seconds = ad.ad_duration)
                tmp_init += delta_time

                if tmp_init > start_point:
                    if_break = True
                    break

            if if_break:
                break
    

        text = f"""Group: {self.billboard.billboards_groop_name};\nOwner: {self.billboard.owner_name};\nSchedules: {self.billboard.schedules_name};\nCurrent ad: {current_ad}."""
        
        return text

