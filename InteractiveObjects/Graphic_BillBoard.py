from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from Entity.Billboard import *

class GraphicBillboard(QGraphicsRectItem):
    def __init__(self, x, y, w, h, billboard : BillBoard):
        super().__init__(x, y, w, h)
        self.billboard = billboard
        self.setBrush(Qt.black)
        self.setToolTip(self.getToolTip())
        
    
    def getToolTip(self):
        text = f"""Group: {self.billboard.billboards_groop_name};\nOwner: {self.billboard.owner_name}."""
        
        return text

