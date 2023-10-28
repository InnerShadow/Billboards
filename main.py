import os
import sys
from PyQt5.QtWidgets import QApplication
from Windows.MainWindow import MainWindow
from PyQt5.QtCore import Qt

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())

