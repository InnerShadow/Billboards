from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox

from Entity.User import User
from InteractiveObjects.Video.Video_uploader import VideoUploader

#Video uploader wiget
class UploadVideoWidget(QWidget):
    def __init__(self, user: User):
        super().__init__()

        self.user = user

        self.init_ui()


    #Init all necessary graphics items
    def init_ui(self):
        layout = QVBoxLayout()

        self.setWindowTitle("Upload Video")

        self.ad_name_input = QLineEdit()
        self.ad_name_input.setPlaceholderText("Ad Name")

        self.file_path_label = QLabel("Selected File:")
        self.file_path_label.setWordWrap(True)

        self.browse_button = QPushButton("Browse Video")
        self.browse_button.clicked.connect(self.browse_video)

        self.upload_button = QPushButton("Upload to Server")
        self.upload_button.clicked.connect(self.upload_to_server)

        layout.addWidget(self.ad_name_input)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.file_path_label)
        layout.addWidget(self.upload_button)

        self.setLayout(layout)

        self.resize(400, 200)


    #Choose file button handler
    def browse_video(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("MP4 Files (*.mp4)")
        file_dialog.setViewMode(QFileDialog.List)
        file_dialog.setOptions(options)

        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.file_path = selected_files[0]
                self.file_path_label.setText(f"Selected File: {self.file_path}")


    #Perform server uploader
    def upload_to_server(self):
        ad_name = self.ad_name_input.text().strip()

        if not ad_name:
            self.show_error_message("Please enter an ad name.")
            return

        if not hasattr(self, 'file_path'):
            self.show_error_message("Please select a video file.")
            return

        self.video_uploader = VideoUploader(ad_name, self.file_path, self.user.client)
        self.video_uploader.finished.connect(self.show_success_message)
        self.video_uploader.run()


    #Show specific error message
    def show_error_message(self, message):
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle("Error")
        error_dialog.setText(message)
        error_dialog.move(self.x(), self.y())
        error_dialog.exec_()


    #Show specific success message
    def show_success_message(self, message):
        success_dialog = QMessageBox()
        success_dialog.setIcon(QMessageBox.Information)
        success_dialog.setWindowTitle("Success")
        success_dialog.setText(message)
        success_dialog.move(self.x(), self.y())
        success_dialog.exec_()
        self.hide()

