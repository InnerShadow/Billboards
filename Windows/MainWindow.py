import re

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap

from ServerData.Client import *
from Entity.BillBoard_groop import *
from InteractiveObjects.Graphic_BillBoard import *
from Entity.Schedules import *
from Windows.AuthenticationWindow import AuthenticationWindow

class MainWindow(QMainWindow):

    billboard_w : int = 75
    billboard_h : int = 40 

    def __init__(self):
        super().__init__()

        self.billboards_groops : list[BillBoard_groop] = [] 

        self.initClient()
        self.initBillboards()
        self.initUI()


    def initClient(self):
        self.client = Client('127.0.0.1', 2000)
        #print(self.client.get_ip_address())


    def initBillboards(self):
        groop_pattern = r'Group: ([\w\s_]+), Owner: [\w\s_]+, Schedule: ([\w\s_]+)'
        groop_response = self.client.Get_response('GET_BILLBOARDS')

        for match in re.finditer(groop_pattern, groop_response):
            groop_name = match.group(1)
            schedules_name = match.group(2)

            schedules_request = f"GET GROUP SCHEDULES schedules_name = {schedules_name}"
            schedules_repsnose = self.client.Get_response(schedules_request)

            if_add = True

            for i in self.billboards_groops:
                if i.groop_name == groop_name and i.schedules.schedules_name == schedules_name:
                    if_add = False

            if if_add:
                schedules = Schedules(schedules_name)
                schedules.fill_from_response(schedules_repsnose)

                groop = BillBoard_groop(groop_name, schedules)
                self.billboards_groops.append(groop)


        for i in self.billboards_groops:
            i.fill_BillBoards(groop_response)
            

    def initUI(self):
        self.setWindowTitle('BillBoards')
        self.setWindowState(Qt.WindowFullScreen)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)

        self.view = QGraphicsView()
        layout.addWidget(self.view)

        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)

        self.login_window = AuthenticationWindow(self.client)

        self.init_beckground()

        self.init_close_button()

        self.resizeEvent = self.handleResize

        self.updateGraphicsItems()

        self.init_menuBar()

        self.show()

        self.show_login_window()


    def init_menuBar(self):
        log_in_action = QAction('Log In', self)
        log_in_action.triggered.connect(self.show_login_window)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('Log in')
        file_menu.addAction(log_in_action)


    @pyqtSlot()
    def handleResize(self, event):
        self.updateGraphicsItems()


    def updateGraphicsItems(self):
        bg_width = self.view.viewport().width()
        bg_height = self.view.viewport().height()

        self.updateCloseButton(bg_width)

        self.updateBeackground(bg_width, bg_height)

        self.clearScene()

        self.updateBillboards(min([bg_width, bg_height]))

        self.update_login_window()


    def updateBeackground(self, bg_width : int, bg_height : int):
        self.background_item.setPixmap(self.background_image.scaled(bg_width, bg_height, Qt.KeepAspectRatio))


    def updateCloseButton(self, bg_width : int):
        self.close_button.setGeometry(bg_width - 78, 32, self.close_button.width(), self.close_button.height())


    def updateBillboards(self, min_size : int):
        for groop in self.billboards_groops:
            for billboard in groop.BillBoards:
                x = int(billboard.x_pos * min_size)
                y = int(billboard.y_pos * min_size)

                graphic_billboard = GraphicBillboard(x, y, self.billboard_w, self.billboard_h, billboard, self.client)

                self.scene.addItem(graphic_billboard)

    
    def update_login_window(self):
        print(int(self.view.viewport().height() // 1.25), self.view.viewport().width() // 4)
        self.login_window.move(int(self.view.viewport().height() // 1.25), self.view.viewport().width() // 4)


    def clearScene(self):
        for item in self.scene.items():
            if isinstance(item, QGraphicsRectItem):
                self.scene.removeItem(item)


    def init_beckground(self):
        self.background_image = QPixmap('Data/Jodino.png')
        self.background_item = QGraphicsPixmapItem(self.background_image)
        self.background_item.setZValue(0)
        self.scene.addItem(self.background_item)


    def init_close_button(self):
        self.close_button = QPushButton('Exit', self)
        self.close_button.clicked.connect(self.close)


    def show_login_window(self):
        self.login_window = AuthenticationWindow(self.client)
        self.login_window.show()
        self.login_window.move(int(self.view.viewport().height() // 1.25), self.view.viewport().width() // 4)
        self.login_window.login_successful.connect(self.handle_login_success)
        
    
    def handle_login_success(self, message):
        print(message)

