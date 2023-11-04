import re

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap

from ServerData.Client import *
from Entity.BillBoard_groop import *
from InteractiveObjects.Graphic_BillBoard import *
from Entity.Schedules import *
from Entity.User import User
from Windows.AuthenticationWindow import AuthenticationWindow
from InteractiveObjects.ScheduleComposer import ScheduleComposer
from InteractiveObjects.GroupComposer import GroupComposer
from InteractiveObjects.ChangePasswordWidget import ChangePasswordWidget
from InteractiveObjects.UploadVideoWidget import UploadVideoWidget

class MainWindow(QMainWindow):
    billboard_w : int = 75
    billboard_h : int = 40 

    def __init__(self):
        super().__init__()

        self.billboards_groops : list[BillBoard_groop] = [] 

        self.initClient()
        self.initBillboards()
        self.initUI()

        self.show()

        self.show_login_window()


    def initClient(self):
        self.user = User('viewer', 'viewer')
        #print(self.user.client.get_ip_address())


    def initBillboards(self):
        groop_pattern = r'Group: ([\w\s_]+), Owner: [\w\s_]+, Schedule: ([\w\s_]+)'
        groop_response = self.user.client.Get_response('GET_BILLBOARDS')

        for match in re.finditer(groop_pattern, groop_response):
            groop_name = match.group(1)
            schedules_name = match.group(2)

            schedules_request = f"GET GROUP SCHEDULES schedules_name = {schedules_name}"
            schedules_repsnose = self.user.client.Get_response(schedules_request)

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

        self.windowLayout = QVBoxLayout(self.central_widget)

        self.view = QGraphicsView()
        self.windowLayout.addWidget(self.view)

        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)

        self.login_window = AuthenticationWindow(self.user.client)

        self.init_beckground()
        self.init_close_button()
        self.resizeEvent = self.handleResize
        self.updateGraphicsItems()
        self.init_menuBar()
        self.init_createSchedules()
        self.init_createGroup()
        self.init_uploadAd()
        

    def init_menuBar(self):
        log_in_action = QAction('Log In', self)
        log_in_action.triggered.connect(self.show_login_window)

        change_password_action = QAction('Change password', self)
        change_password_action.triggered.connect(self.change_password)

        menubar = self.menuBar()
        login_menu = menubar.addMenu('Log in')
        login_menu.addAction(log_in_action)

        account_menu = menubar.addMenu('Account')
        account_menu.addAction(change_password_action)


    def init_createSchedules(self):
        self.create_schedules_button = QPushButton('Create schedules', self)
        self.create_schedules_button.clicked.connect(self.showScheduleComposer)
        self.create_schedules_button.setFixedWidth(125)
        self.create_schedules_button.setFixedHeight(30)
        self.create_schedules_button.hide()


    def init_createGroup(self):
        self.create_group_button = QPushButton('Create group', self)
        self.create_group_button.clicked.connect(self.showGroupComposer)
        self.create_group_button.setFixedWidth(125)
        self.create_group_button.setFixedHeight(30)
        self.create_group_button.hide()


    def init_uploadAd(self):
        self.uploadAd_button = QPushButton('Upload ad', self)
        self.uploadAd_button.clicked.connect(self.showUploadAd)
        self.uploadAd_button.setFixedWidth(125)
        self.uploadAd_button.setFixedHeight(30)
        self.uploadAd_button.hide()


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

        if self.user.role == 'owner' or self.user.role == 'admin':
            self.update_create_schedules()
            self.update_create_group()
            self.update_UploadAd()


    def updateBeackground(self, bg_width : int, bg_height : int):
        self.background_item.setPixmap(self.background_image.scaled(bg_width, bg_height, Qt.KeepAspectRatio))


    def updateCloseButton(self, bg_width : int):
        self.close_button.setGeometry(bg_width - 90, self.view.viewport().height(), self.close_button.width(), self.close_button.height())


    def updateBillboards(self, min_size : int):
        for groop in self.billboards_groops:
            for billboard in groop.BillBoards:
                x = int(billboard.x_pos * min_size)
                y = int(billboard.y_pos * min_size)

                graphic_billboard = GraphicBillboard(x, y, self.billboard_w, self.billboard_h, billboard, self.user)

                self.scene.addItem(graphic_billboard)

    
    def update_login_window(self):
        self.login_window.move(int(self.view.viewport().height() // 1.25), self.view.viewport().width() // 4)

    
    def update_create_schedules(self):
        self.create_schedules_button.setGeometry(self.view.viewport().width() - 135, self.view.viewport().height() // 2, 
                                                 self.create_schedules_button.width(), self.create_schedules_button.height())
        
    
    def update_create_group(self):
        self.create_group_button.setGeometry(self.view.viewport().width() - 135, self.view.viewport().height() // 2 + 30 + 25, 
                                            self.create_schedules_button.width(), self.create_schedules_button.height())
        

    def update_UploadAd(self):
        self.uploadAd_button.setGeometry(self.view.viewport().width() - 135, self.view.viewport().height() // 2 -30 - 25, 
                                            self.create_schedules_button.width(), self.create_schedules_button.height())


    def showScheduleComposer(self):
        self.scheduleComposer = ScheduleComposer(self.user)
        self.scheduleComposer.move(int(self.view.viewport().height() // 1.25), self.view.viewport().width() // 4)
        self.scheduleComposer.show()


    def showGroupComposer(self):
        self.scheduleComposer = GroupComposer(self.user)
        self.scheduleComposer.move(int(self.view.viewport().height() // 1.25), self.view.viewport().width() // 4)
        self.scheduleComposer.show()

    
    def showUploadAd(self):
        self.uploadVideoWidget = UploadVideoWidget(self.user)
        self.uploadVideoWidget.move(int(self.view.viewport().height() // 1.25), self.view.viewport().width() // 4)
        self.uploadVideoWidget.show()


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
        self.login_window = AuthenticationWindow(self.user.client)
        self.login_window.show()
        self.login_window.move(int(self.view.viewport().height() // 1.25), self.view.viewport().width() // 4)
        self.login_window.login_successful.connect(self.handle_login_success)

    
    def change_password(self):
        if self.user.role == 'viewer':
            self.passwordChangeFailed()

        else:
            self.changePasswordWidget = ChangePasswordWidget(self.user)
            self.changePasswordWidget.move(int(self.view.viewport().height() // 1.25), self.view.viewport().width() // 4)
            self.changePasswordWidget.show()
            
        
    def passwordChangeFailed(self):
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle("Error")
        error_dialog.setText("You need to log in before change password")
        error_dialog.move(self.x(), self.y())
        error_dialog.exec_()
    

    def handle_login_success(self, response : str):
        login_patter = r'Logged in successfully username = (\w+), role = (\w+)'
        login_match = re.search(login_patter, response)
        self.user.login = login_match.group(1)
        self.user.role = login_match.group(2)

        if self.user.role == 'owner' or self.user.role == 'admin':
            self.create_schedules_button.show()
            self.create_group_button.show()
            self.uploadAd_button.show()
        
        self.updateGraphicsItems()

