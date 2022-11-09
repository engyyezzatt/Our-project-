import json
from collections import OrderedDict
from Node_Serializable import *
from Graphic_Scene import *


class Scene(Serializable):
    def __init__(self):
        super().__init__()
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

    def saveToFile(self, filename):
        with open(filename, "w") as file:
            file.write(json.dumps(self.serialize(), indent=4))
        print("saving to", filename, "was successfull.")

    def loadFromFile(self, filename):
        with open(filename, "r") as file:
            raw_data = file.read()
            data = json.loads(raw_data, encoding='utf-8')
            self.deserialize(data)

    def saveToFile(self, filename):
        with open(filename, "w") as file:
            file.write( json.dumps( self.serialize(), indent=4 ) )
        print("saving to", filename, "was successfull.")

    def loadFromFile(self, filename):
        with open(filename, "r") as file:
            raw_data = file.read()
            data = json.loads(raw_data, encoding='utf-8')
            self.deserialize(data)


    def serialize(self):
        nodes, edges = [], []
        for node in self.nodes: nodes.append(node.serialize())
        for edge in self.edges: edges.append(edge.serialize())
        return OrderedDict([
            ('id', self.id),
            ('scene_width', self.width_scene),
            ('scene_height', self.height_scene),
            ('nodes', nodes),
            ('edges', edges),
        ])

    def deserialize(self, data, hashmap={}):
        print("deserializating data", data)
        return False
