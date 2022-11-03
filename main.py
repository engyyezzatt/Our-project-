from PyQt5 import QtWidgets
import sys
from Window_Editor import WindowEditor

if __name__ == '__main__':
    myApp = QtWidgets.QApplication(sys.argv)

    myWindow = WindowEditor()

    myApp.exec_()


