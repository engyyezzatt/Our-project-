
from Graphic_Scene import *


class Scene:
    def __init__(self):
        self.nodes = []
        self.edges = []

        self.width_scene = 64000
        self.height_scene = 64000

        self.initUI()

    def initUI(self):
        self.myGrScene = CrGraphicScene(self)
        self.myGrScene.setScene(self.width_scene, self.height_scene)

    def addNode(self, node):
        self.nodes.append(node)

    def addEdge(self, edge):
        self.edges.append(edge)

    def removeNode(self, node):
        self.nodes.remove(node)

    def removeEdge(self, edge):
        self.edges.remove(edge)