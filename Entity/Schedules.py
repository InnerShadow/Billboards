import re

from Entity.Ad import *

class Schedules:

    ad_queue : list[Ad] = []

    def __init__(self, schedules_name : str):
        self.schedules_name = schedules_name
        

    def fill_from_response(self, response : str):
        pattern = r'Video_url: (.*?), Ad_name: (.*?), Ad_duration: (.*?) '
        matches = re.findall(pattern, response)

        for video_url, ad_name, ad_duration in matches:
            ad = Ad(video_url, ad_name, int(float(ad_duration)))
            self.ad_queue.append(ad)
        
        pass

