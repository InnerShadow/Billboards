import re

from Entity.Billboard import *
from Entity.Schedules import *

class BillBoard_groop:

    def __init__(self, groop_name : str, schedules : Schedules):
        self.groop_name = groop_name
        self.schedules = schedules

        self.BillBoards : list[BillBoard] = []
        

    def fill_BillBoards(self, response):
        response += ' '
        pattern = re.compile(f'Group: {self.groop_name}, Owner: (.*?), Schedule: .*?, X: (.*?), Y: (.*?) ')

        matches = pattern.findall(response)

        for match in matches:
            owner, x, y = match
            billBoard = BillBoard(float(x), float(y), self.groop_name, owner, self.schedules.schedules_name)
            self.BillBoards.append(billBoard)

