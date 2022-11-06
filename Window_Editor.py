from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtGui
from Graphic_View import *
from Node_Scene import *
from Draw_Node import *
from Node_Socket import Socket


class WindowEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.MyUI()

    def MyUI(self):
        self.setGeometry(90, 80, 1200, 600)
        self.myLayout = QVBoxLayout()
        self.myLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.myLayout)

        # create the scene
        self.myScene = Scene()
        # self.myGrScene =self.myScene.myGrScene

        node = Node(self.myScene, "My Awesome Node", inputs=[1, 2, 3], outputs=[1])
        node = Node(self.myScene, "Second Node", inputs=[1, 2], outputs=[1])
        nodeContent = NodeContent()

        # create the graphic view
        self.view = CrGraphicsView(self.myScene.myGrScene, self)
        self.myLayout.addWidget(self.view)

        self.setWindowIcon(QIcon("VP logo Trial.png"))
        self.setWindowTitle("VP")

        self.show()
