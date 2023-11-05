from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QPushButton, QLineEdit, QLabel

class MemoryLimitWidget(QWidget):
    new_memory = pyqtSignal(int)

    def __init__(self, current_memory_limit : int):
        super().__init__()

        self.current_memory_limit = current_memory_limit
        self.initUI()


    def initUI(self):
        layout = QVBoxLayout()

        current_memory_label = QLabel(f"Current Memory Limit: {self.current_memory_limit} MB")
        self.new_memory_input = QLineEdit()
        set_limit_button = QPushButton("Set Limit")

        self.setWindowTitle("Memory meneger")

        set_limit_button.clicked.connect(self.set_memory_limit)
        self.new_memory_input.returnPressed.connect(self.set_memory_limit)

        layout.addWidget(current_memory_label)
        layout.addWidget(self.new_memory_input)
        layout.addWidget(set_limit_button)

        self.setLayout(layout)


    def set_memory_limit(self):
        new_limit = self.new_memory_input.text()
        try:
            new_limit = int(new_limit)
            if new_limit > 10:
                self.current_memory_limit = new_limit

                self.show_success_message(f"Memory limit change to {new_limit}")
                self.new_memory.emit(new_limit)
                self.hide()

                with open("Data/memory.txt", 'w') as f:
                    f.write(str(new_limit))

            else:
                self.show_error_message("Memory limit must be at least 10 MB")

        except ValueError:
            self.show_error_message("Memory limit must be positive integer")


    def update_ui(self):
        current_memory_label = self.findChild(QLabel)
        if current_memory_label:
            current_memory_label.setText(f"Current Memory Limit: {self.current_memory_limit} MB")


    def show_error_message(self, message):
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle("Error")
        error_dialog.setText(message)
        error_dialog.move(self.x(), self.y())
        error_dialog.exec_()


    def show_success_message(self, message):
        success_dialog = QMessageBox()
        success_dialog.setIcon(QMessageBox.Information)
        success_dialog.setWindowTitle("Success")
        success_dialog.setText(message)
        success_dialog.move(self.x(), self.y())
        success_dialog.exec_()