from PyQt5.QtWidgets import QDialog, QTextEdit, QVBoxLayout

#Log export handler
class LogViewerWidget(QDialog):
    def __init__(self, logs):
        super().__init__()
        self.logs = logs
        self.initUI()


    #Init all necessary graphics items
    def initUI(self):
        self.setWindowTitle("Log Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.log_text_edit = QTextEdit()
        self.log_text_edit.setReadOnly(True)

        self.init_logs()

        layout = QVBoxLayout()
        layout.addWidget(self.log_text_edit)

        self.setLayout(layout)


    #Fill log info
    def init_logs(self):
        logs = self.logs
        self.log_text_edit.setPlainText(logs)

