
#Simple billboard container
class BillBoard:
    def __init__(self, x_pos : float, y_pos : float, billboards_groop_name : str, owner_name : str, schedules_name : str):
        self.x_pos = x_pos  
        self.y_pos = y_pos
        self.billboards_groop_name = billboards_groop_name
        self.owner_name = owner_name
        self.schedules_name = schedules_name 
        
