import os
import sys
from PyQt5.QtWidgets import QApplication
from Windows.MainWindow import MainWindow
from PyQt5.QtCore import Qt

if __name__ == '__main__':
    #os.environ["QT_QPA_PLATFORM"] = "xcb"
    #QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())

