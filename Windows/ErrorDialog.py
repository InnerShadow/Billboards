from PyQt5.QtWidgets import QMessageBox


class ErrorDialog(QMessageBox):
    def __init__(self):
        super().__init__()

        self.init_ui()

        self.show()

    
    def init_ui(self):
        self.setIcon(QMessageBox.Critical)
        self.setWindowTitle("Connection Error")
        self.setText("Failed to connect to the server.")
        self.setStandardButtons(QMessageBox.Ok)

