import re

from Entity.Billboard import *
from Entity.Schedules import *

class BillBoard_groop:

    BillBoards : list = []

    def __init__(self, groop_name : str, schedules : Schedules):
        self.groop_name = groop_name
        self.schedules = schedules
        

    def fill_BillBoards(self, response):
        response += ' '
        pattern = re.compile(f'Group: {self.groop_name}, Owner: (.*?), Schedule: .*?, X: (.*?), Y: (.*?) ')

        matches = pattern.findall(response)

        for match in matches:
            owner, x, y = match
            billBoard = BillBoard(float(x), float(y), self.schedules.schedules_name, owner)
            self.BillBoards.append(billBoard)

