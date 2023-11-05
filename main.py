import sys
from PyQt5.QtWidgets import QApplication
from Windows.MainWindow import MainWindow
from Windows.ErrorDialog import ErrorDialog

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        mainWindow = MainWindow()
        
    except ConnectionRefusedError:
        error_dialog = ErrorDialog()

    finally:
        sys.exit(app.exec_())

