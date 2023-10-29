import re

from Entity.Ad import *

class Schedules:

    def __init__(self, schedules_name : str):
        self.schedules_name = schedules_name
        self.ad_queue : list[Ad] = []
        

    def fill_from_response(self, response : str):
        response += " "
        pattern = r'Video_url: (.*?), Ad_name: (.*?), Ad_duration: (.*?) '
        matches = re.findall(pattern, response)

        for video_url, ad_name, ad_duration in matches:
            ad = Ad(video_url, ad_name, int(float(ad_duration)))
            self.ad_queue.append(ad)
        
        pass

