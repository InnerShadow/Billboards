from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton

from Entity.User import User
from InteractiveObjects.CreateUserWidget import CreateUserWidget
from InteractiveObjects.DeleteUserWidget import DeleteUserWidget

class UserManagementWidget(QWidget):
    def __init__(self, user : User):
        super().__init__()

        self.user = user

        self.initUI()


    def initUI(self):
        layout = QVBoxLayout()

        self.setWindowTitle("Users menu")

        create_user_button = QPushButton("Create User")
        delete_user_button = QPushButton("Delete User")

        create_user_button.clicked.connect(self.create_user_clicked)
        delete_user_button.clicked.connect(self.delete_user_clicked)

        layout.addWidget(create_user_button)
        layout.addWidget(delete_user_button)

        self.setLayout(layout)

        self.resize(200, 75)


    def create_user_clicked(self):
        self.createUserWidget = CreateUserWidget(self.user)
        self.createUserWidget.move(self.x(), self.y())
        self.createUserWidget.show()
        self.createUserWidget.created.connect(self.hide)


    def delete_user_clicked(self):
        self.deleteUserWidget = DeleteUserWidget(self.user)
        self.deleteUserWidget.move(self.x(), self.y())
        self.deleteUserWidget.show()
        self.deleteUserWidget.deleted.connect(self.hide)

