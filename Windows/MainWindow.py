import re
from datetime import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QCursor

from Entity.User import User
from Entity.Schedules import Schedules
from Entity.BillBoard_groop import BillBoard_groop

from InteractiveObjects.BillboardsHelpers.Graphic_BillBoard import GraphicBillboard

from InteractiveObjects.Video.UploadVideoWidget import UploadVideoWidget

from InteractiveObjects.MainWindowHelper.InfoWiget import InfoWiget
from InteractiveObjects.MainWindowHelper.GroupComposer import GroupComposer
from InteractiveObjects.MainWindowHelper.LogExportWidget import LogExportWidget
from InteractiveObjects.MainWindowHelper.StatisticsWiget import StatisticsWiget
from InteractiveObjects.MainWindowHelper.ScheduleComposer import ScheduleComposer
from InteractiveObjects.MainWindowHelper.MemoryLimitWidget import MemoryLimitWidget
from InteractiveObjects.MainWindowHelper.ChangePasswordWidget import ChangePasswordWidget
from InteractiveObjects.MainWindowHelper.UserManagementWidget import UserManagementWidget
from InteractiveObjects.MainWindowHelper.BillboardCreatorWidget import BillboardCreatorWidget

from Windows.AuthenticationWindow import AuthenticationWindow

class MainWindow(QMainWindow):
    #Static billboards param
    billboard_w : int = 75
    billboard_h : int = 40 

    def __init__(self):
        super().__init__()

        #Init data
        self.billboards_groops : list[BillBoard_groop] = [] 
        self.waiting_for_create_billboard = False

        self.memoryLimit : int = self.loadMemoryLimit()
        self.last_update : datetime = datetime.now()

        self.initClient()
        self.initBillboards()
        self.initUI()

        self.show()

        self.showLoginWindow()


    #Init all visible objects
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

        self.timer = QTimer()
        self.timer.timeout.connect(self.tryUpdateBillboards)
        self.timer.start(2000)

        self.login_window = AuthenticationWindow(self.user.client)

        self.init_beckground()
        self.init_close_button()
        self.init_info()
        self.init_statistics()
        self.updateGraphicsItems()
        self.init_menuBar()
        self.init_createSchedules()
        self.init_createGroup()
        self.init_uploadAd()
        self.init_createBillboardButton()
        self.init_usersMenuButton()
        self.resizeEvent = self.handleResize


    #Create client, firstly as viewer
    def initClient(self):
        self.user = User('viewer', 'viewer')
        #print(self.user.client.get_ip_address())


    #Ask server about billboards, fill nesessary data & draw billboards
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
            

    #Fill all necessary options in menu bar
    def init_menuBar(self):
        log_in_action = QAction('Log In', self)
        log_in_action.triggered.connect(self.showLoginWindow)

        change_password_action = QAction('Change password', self)
        change_password_action.triggered.connect(self.showChangePassword)

        memory_limit_action = QAction('Set Memory Limit', self)
        memory_limit_action.triggered.connect(self.showMemoryLimit)

        export_logs_action = QAction('Export logs', self)
        export_logs_action.triggered.connect(self.showExportLogs)

        menubar = self.menuBar()

        login_menu = menubar.addMenu('Log in')
        login_menu.addAction(log_in_action)

        memory_menu = menubar.addMenu('Memory')
        memory_menu.addAction(memory_limit_action)

        account_menu = menubar.addMenu('Account')
        account_menu.addAction(change_password_action)

        logs_menu = menubar.addMenu('Logs')
        logs_menu.addAction(export_logs_action)


    #Init infi button
    def init_info(self):
        self.info_button = QPushButton('Info', self)
        self.info_button.clicked.connect(self.showInfo)
        self.info_button.setFixedWidth(125)
        self.info_button.setFixedHeight(30)
        self.info_button.show()


    #Init Statistics button
    def init_statistics(self):
        self.statistica_button = QPushButton('Show statistics', self)
        self.statistica_button.clicked.connect(self.showStatistics)
        self.statistica_button.setFixedWidth(125)
        self.statistica_button.setFixedHeight(30)
        self.statistica_button.show()

    
    #Init Create schedules button
    def init_createSchedules(self):
        self.create_schedules_button = QPushButton('Create schedules', self)
        self.create_schedules_button.clicked.connect(self.showScheduleComposer)
        self.create_schedules_button.setFixedWidth(125)
        self.create_schedules_button.setFixedHeight(30)
        self.create_schedules_button.hide()


    #Init create group button
    def init_createGroup(self):
        self.create_group_button = QPushButton('Create group', self)
        self.create_group_button.clicked.connect(self.showGroupComposer)
        self.create_group_button.setFixedWidth(125)
        self.create_group_button.setFixedHeight(30)
        self.create_group_button.hide()


    #Init ypload Ad button
    def init_uploadAd(self):
        self.uploadAd_button = QPushButton('Upload ad', self)
        self.uploadAd_button.clicked.connect(self.showUploadAd)
        self.uploadAd_button.setFixedWidth(125)
        self.uploadAd_button.setFixedHeight(30)
        self.uploadAd_button.hide()

    
    #Init create billboard button
    def init_createBillboardButton(self):
        self.create_billboard_button = QPushButton('Create Billboard', self)
        self.create_billboard_button.clicked.connect(self.showCreateBillboardInstructions)
        self.create_billboard_button.setFixedWidth(125)
        self.create_billboard_button.setFixedHeight(30)
        self.create_billboard_button.hide()


    #Init users menu bitton    
    def init_usersMenuButton(self):
        self.user_menu_button = QPushButton('Users Menu', self)
        self.user_menu_button.clicked.connect(self.showUserMenu)
        self.user_menu_button.setFixedWidth(125)
        self.user_menu_button.setFixedHeight(30)
        self.user_menu_button.hide()


    #Init beckground
    def init_beckground(self):
        self.background_image = QPixmap('Data/Jodino.png')
        self.background_item = QGraphicsPixmapItem(self.background_image)
        self.background_item.setZValue(0)
        self.scene.addItem(self.background_item)


    #Init Exit button
    def init_close_button(self):
        self.close_button = QPushButton('Exit', self)
        self.close_button.clicked.connect(self.doExit)
        

    #Resizer of beckground when window geometry is changes
    @pyqtSlot()
    def handleResize(self, event):
        self.updateGraphicsItems()

    
    #Check if create billboard options is used
    #Then create a billborad
    #Else do nothig
    def mousePressEvent(self, event):
        if self.waiting_for_create_billboard and event.button() == Qt.LeftButton:
            self.createBillboard()
            self.waiting_for_create_billboard = False 


    #Update all nedded graphics items
    def updateGraphicsItems(self):
        bg_width = self.view.viewport().width()
        bg_height = self.view.viewport().height()

        #Update base graphics items
        self.updateCloseButton(bg_width)
        self.updateBeackground(bg_width, bg_height)
        self.clearScene()
        self.updateBillboards(bg_width, bg_height)
        self.updateLoginWindow()
        self.updateInfo()
        self.updateStatistics()

        #Update graphics items for owner & admin
        if self.user.role == 'owner' or self.user.role == 'admin':
            self.updateCreateSchedules()
            self.updateCreateGroup()
            self.updateUploadAd()

        #Update graphics items only for admin
        if self.user.role == 'admin':
            self.updateCreateBillboards()
            self.updateUserMenu()


    #Beackground updader
    def updateBeackground(self, bg_width : int, bg_height : int):
        self.background_item.setPixmap(self.background_image.scaled(bg_width, bg_height, Qt.KeepAspectRatio))


    #Close button updader
    def updateCloseButton(self, bg_width : int):
        self.close_button.setGeometry(bg_width - 90, self.view.viewport().height(), self.close_button.width(), self.close_button.height())


    #Billboards updader
    def updateBillboards(self, x_scale : int, y_scale):
        for groop in self.billboards_groops:
            for billboard in groop.BillBoards:
                x = int(billboard.x_pos * x_scale)
                y = int(billboard.y_pos * y_scale)

                graphic_billboard = GraphicBillboard(x, y, self.billboard_w, self.billboard_h, billboard, self.user)

                self.scene.addItem(graphic_billboard)

    
    #Login updader
    def updateLoginWindow(self):
        self.login_window.move(int(self.view.viewport().height() // 1.25), self.view.viewport().width() // 4)

    
    #Schedules updader
    def updateCreateSchedules(self):
        self.create_schedules_button.setGeometry(self.view.viewport().width() - 135, self.view.viewport().height() // 2, 
                                                 self.create_schedules_button.width(), self.create_schedules_button.height())
        
    
    #Groups updader
    def updateCreateGroup(self):
        self.create_group_button.setGeometry(self.view.viewport().width() - 135, self.view.viewport().height() // 2 + 30 + 25, 
                                            self.create_schedules_button.width(), self.create_schedules_button.height())
        

    #Upload updader
    def updateUploadAd(self):
        self.uploadAd_button.setGeometry(self.view.viewport().width() - 135, self.view.viewport().height() // 2 - 30 - 25, 
                                            self.create_schedules_button.width(), self.create_schedules_button.height())
        
    
    #Create billboard updader
    def updateCreateBillboards(self):
        self.create_billboard_button.setGeometry(self.view.viewport().width() - 135, self.view.viewport().height() // 2 - 60 - 50, 
                                            self.create_schedules_button.width(), self.create_schedules_button.height())
        

    #Users menu updader
    def updateUserMenu(self):
        self.user_menu_button.setGeometry(self.view.viewport().width() - 135, self.view.viewport().height() // 2 + 60 + 50, 
                                            self.create_schedules_button.width(), self.create_schedules_button.height())

    
    #Info updader
    def updateInfo(self):
        self.info_button.setGeometry(30, self.view.viewport().height() // 2 + 27, 
                                            self.info_button.width(), self.info_button.height())
        
    
    #Statistics updader
    def updateStatistics(self):
        self.statistica_button.setGeometry(30, self.view.viewport().height() // 2 - 27, 
                                            self.statistica_button.width(), self.statistica_button.height())
        
    
    #Clear all billboards and ask sever to get new grousp
    def updateBillbordsGroops(self):
        self.billboards_groops = []
        self.initBillboards()
        self.updateGraphicsItems()

    
    #Check if last server update younger then current last update
    def tryUpdateBillboards(self):
        update_request = f"GET LAST UPDATE"
        update_response = self.user.client.Get_response(update_request)

        last_server_update = datetime.fromisoformat(update_response)

        #If younger the ask server to get new information about billboards
        if self.last_update < last_server_update:
            self.updateBillbordsGroops()
            self.last_update = last_server_update
        
    
    #Show info wiget
    def showInfo(self):
        self.infoWiget = InfoWiget()
        self.infoWiget.move(int(self.view.viewport().height() // 1.25), self.view.viewport().width() // 4)
        self.infoWiget.show()


    #show statistics wiget
    def showStatistics(self):
        self.statisticsWiget = StatisticsWiget(self.user)
        self.statisticsWiget.move(int(self.view.viewport().height() // 1.25), self.view.viewport().width() // 4)
        self.statisticsWiget.show()


    #Show schedule composer wiget
    def showScheduleComposer(self):
        self.scheduleComposer = ScheduleComposer(self.user)
        self.scheduleComposer.move(int(self.view.viewport().height() // 1.25), self.view.viewport().width() // 4)
        self.scheduleComposer.show()


    #Show group composer wiget
    def showGroupComposer(self):
        self.scheduleComposer = GroupComposer(self.user)
        self.scheduleComposer.move(int(self.view.viewport().height() // 1.25), self.view.viewport().width() // 4)
        self.scheduleComposer.show()

    
    #Show ad uploader wiget
    def showUploadAd(self):
        self.uploadVideoWidget = UploadVideoWidget(self.user)
        self.uploadVideoWidget.move(int(self.view.viewport().height() // 1.25), self.view.viewport().width() // 4)
        self.uploadVideoWidget.show()


    #Sgow users menu wiget
    def showUserMenu(self):
        self.userManagementWidget = UserManagementWidget(self.user)
        self.userManagementWidget.move(int(self.view.viewport().height() // 1.25), self.view.viewport().width() // 4)
        self.userManagementWidget.show()

    
    #Show Message box that inform how to create a billboard
    def showCreateBillboardInstructions(self):
        instructions = "Click on the map to create a billboard."
        QMessageBox.information(self, "Create Billboard Instructions", instructions)
        self.waiting_for_create_billboard = True

    
    #Show log in wiget
    def showLoginWindow(self):
        self.updateGraphicsItems()
        self.login_window = AuthenticationWindow(self.user.client)
        self.login_window.show()
        self.login_window.move(int(self.view.viewport().height() // 1.25), self.view.viewport().width() // 4)
        self.login_window.login_successful.connect(self.handle_login_success)

    
    #Show change password widget
    def showChangePassword(self):
        if self.user.role == 'viewer':
            #Only if user not viewer
            self.passwordChangeFailed()

        else:
            self.changePasswordWidget = ChangePasswordWidget(self.user)
            self.changePasswordWidget.move(int(self.view.viewport().height() // 1.25), self.view.viewport().width() // 4)
            self.changePasswordWidget.show()


    #Show memory limit wiget
    def showMemoryLimit(self):
        self.memoryLimitWidget = MemoryLimitWidget(self.memoryLimit)
        self.memoryLimitWidget.move(int(self.view.viewport().height() // 1.25), self.view.viewport().width() // 4)
        self.memoryLimitWidget.new_memory.connect(self.setMemoryLimit)
        self.memoryLimitWidget.show()

    
    #Show log export wiget for admins only
    def showExportLogs(self):
        if self.user.role != 'admin':
            self.exportLogsFailed()
        
        else:
            self.logExportWidget = LogExportWidget(self.user)
            self.logExportWidget.move(int(self.view.viewport().height() // 1.25), self.view.viewport().width() // 4)
            self.logExportWidget.show()


    #Remove all graphics imeps from the scene
    def clearScene(self):
        for item in self.scene.items():
            if isinstance(item, QGraphicsRectItem):
                self.scene.removeItem(item)

    
    #Error about log export
    def exportLogsFailed(self):
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle("Error")
        error_dialog.setText("Only admin can export logs")
        error_dialog.move(int(self.view.viewport().height() // 1.25), self.view.viewport().width() // 4)
        error_dialog.exec_()
            
    
    #Error about password change
    def passwordChangeFailed(self):
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle("Error")
        error_dialog.setText("You need to log in before change password")
        error_dialog.move(int(self.view.viewport().height() // 1.25), self.view.viewport().width() // 4)
        error_dialog.exec_()


    #Error about billboards creation
    def createBillboardFail(self):
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle("Error")
        error_dialog.setText("Only admin can create billboards")
        error_dialog.move(int(self.view.viewport().height() // 1.25), self.view.viewport().width() // 4)
        error_dialog.exec_()
    

    #Success in log in 
    def handle_login_success(self, response : str):
        login_patter = r'Logged in successfully username = (\w+), role = (\w+)'
        login_match = re.search(login_patter, response)
        self.user.login = login_match.group(1)
        self.user.role = login_match.group(2)

        if self.user.role == 'owner' or self.user.role == 'admin':
            self.create_schedules_button.show()
            self.create_group_button.show()
            self.uploadAd_button.show()

        if self.user.role == 'admin':
            self.create_billboard_button.show()
            self.user_menu_button.show()
        
        self.updateGraphicsItems()


    #Create billboard heandler
    def createBillboard(self):
        if self.user.role != 'admin':
            self.createBillboardFail()

        else:
            cursor_pos = QCursor.pos()
            pos_in_view = self.view.mapFromGlobal(cursor_pos)
            pos_in_scene = self.view.mapToScene(pos_in_view)

            x = round(pos_in_scene.x() / self.scene.width(), 3)
            y = round(pos_in_scene.y() / self.scene.height(), 3)

            self.billboardCreatorWidget = BillboardCreatorWidget(self.user, x, y)
            self.billboardCreatorWidget.move(int(self.view.viewport().height() // 1.25), self.view.viewport().width() // 4)
            self.billboardCreatorWidget.show()
            self.billboardCreatorWidget.created.connect(self.updateBillbordsGroops)


    #Memory setter
    def setMemoryLimit(self, new_limit : int):
        self.memoryLimit = new_limit


    #Memory loader
    def loadMemoryLimit(self):
        try:
            with open("Data/memory.txt", 'r') as f:
                return int(f.read())
            
        except Exception:
            return 50
        

    #Exit button handler
    def doExit(self):
        exit_request = f"EXIT APP"
        _ = self.user.client.Get_response(exit_request)

        self.close()

