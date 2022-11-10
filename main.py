from PyQt5 import QtWidgets
import sys
from Window_Editor import WindowEditor
from PyQt5.QtWidgets import QMainWindow, QApplication

if __name__ == "__main__":

    myApp = QApplication(sys.argv)
    myWindow = WindowEditor()

    sys.exit(myApp.exec())
