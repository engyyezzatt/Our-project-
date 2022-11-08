from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import Qt
from PyQt5.QtCore import *


class NodeContent(QWidget):
    def __init__(self, node, parent=None):
        self.node = node
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)

        self.wdg_label = QLabel("Some Title")
        self.wdg_label.setFont(QFont("Ubuntu ", 10))
        self.wdg_label.setAlignment(Qt.AlignCenter)
        #self.wdg_label.setStyleSheet('backgroud-color:yellow')
        self.layout.addWidget(self.wdg_label)
        self.textEdit=QTextEdit()
        #self.textEdit.setStyleSheet('background-color:yellow')
        self.layout.addWidget(QDMTextEdit("Node"))

    def setEditingFlag(self, value):
        self.node.scene.myGrScene.views()[0].editingFlag = value



class QDMTextEdit(QTextEdit):
    def focusInEvent(self, event):
        self.parentWidget().setEditingFlag(True)
        super().focusInEvent(event)


    def focusOutEvent(self, event):
        self.parentWidget().setEditingFlag(False)
        super().focusOutEvent(event)