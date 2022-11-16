from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtGui
from Graphic_View import *
from Node_Scene import *
from Draw_Node import *
from node_edge import *


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

        self.addNodes()

        # nodeContent = NodeContent()

        # create the graphic view
        self.view = CrGraphicsView(self.myScene.grScene, self)
        self.myLayout.addWidget(self.view)

        self.setWindowIcon(QIcon("VP logo Trial.png"))
        self.setWindowTitle("VP")

        self.show()

    def addNodes(self):
        node1 = Node(self.myScene, "Node 1", inputs=[1, 2, 3], outputs=[1])
        node2 = Node(self.myScene, "Node 2", inputs=[1, 2, 3], outputs=[1])
        node3 = Node(self.myScene, "Node 3", inputs=[1, 2, 3], outputs=[1])

        node1.setpos(-350, -250)
        node2.setpos(-75, 0)
        node3.setpos(200, -150)

        edge0 = Edge(self.myScene, node1.outputs[0], node2.inputs[1], edge_type=EDGE_TYPE_BEZIER)
        # edge1 = Edge(self.myScene, node1.outputs[0], node2.inputs[1], edge_type=EDGE_TYPE_BEZIER)
        # edge2 = Edge(self.myScene, node1.outputs[0], node2.inputs[2], edge_type=EDGE_TYPE_BEZIER)

        # edge9 = Edge(self.myScene, node1.outputs[0], node3.inputs[0], edge_type=EDGE_TYPE_BEZIER)
        # edge10 = Edge(self.myScene, node1.outputs[0], node3.inputs[1], edge_type=EDGE_TYPE_BEZIER)
        # edge11 = Edge(self.myScene, node1.outputs[0], node3.inputs[2], edge_type=EDGE_TYPE_BEZIER)

        edge3 = Edge(self.myScene, node2.outputs[0], node3.inputs[0], edge_type=EDGE_TYPE_BEZIER)
        # edge4 = Edge(self.myScene, node2.outputs[0], node3.inputs[1], edge_type=EDGE_TYPE_BEZIER)
        # edge5 = Edge(self.myScene, node2.outputs[0], node3.inputs[2], edge_type=EDGE_TYPE_BEZIER)

        # edge6 = Edge(self.myScene, node1.outputs[0], node3.inputs[2], edge_type=EDGE_TYPE_BEZIER)
        # edge7 = Edge(self.myScene, node1.outputs[0], node3.inputs[2], edge_type=EDGE_TYPE_BEZIER)
        # edge8 = Edge(self.myScene, node1.outputs[0], node3.inputs[2], edge_type=EDGE_TYPE_BEZIER)
