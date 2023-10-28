import re

from Entity.Billboard import *

class BillBoard_groop:

    BillBoards = []

    def __init__(self, groop_name : str, schedules_name : str):
        self.groop_name = groop_name
        self.schedules_name = schedules_name
        

    def fill_BillBoards(self, response):
        response += ' '
        pattern = re.compile(f'Group: {self.groop_name}, Owner: (.*?), Schedule: .*?, X: (.*?), Y: (.*?) ')

        matches = pattern.findall(response)

        for match in matches:
            owner, x, y = match
            billBoard = BillBoard(float(x), float(y), self.groop_name, owner)
            self.BillBoards.append(billBoard)
