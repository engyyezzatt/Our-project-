import json
import os
import sys
from collections import OrderedDict
from Node_Serializable import *
from Graphic_Scene import *
from Draw_Node import *
from node_edge import *


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

    def clear(self):
        while len(self.nodes) > 0 :
            self.nodes[0].remove()

    def saveToFile(self, filename):
        with open(filename, "w") as file:
            file.write(json.dumps(self.serialize(), indent=4))
        print("saving to", filename, "was successfull.")

    def loadFromFile(self, filename=str):
        with open(filename, "r") as file:
            raw_data = file.read()
            try:
                if sys.version_info >= (3, 9):
                    data = json.loads(raw_data)
                else:
                    data = json.loads(raw_data, encoding='utf-8')
                self.filename = filename
                self.deserialize(data)
                self.has_been_modified = False
            # except json.JSONDecodeError:
            #     raise InvalidFile("%s is not a valid JSON file" % os.path.basename(filename))
            except Exception as e:
                print(e)

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

        self.clear()

        hashmap ={}

        # create nodes

        for node_data in data['nodes']:
            Node(self).deserialize(node_data, hashmap)

        # create edges

        for edge_data in data['nodes']:
            Node(self).deserialize(edge_data,hashmap)

        # all_edges = self.edges.copy()
        #
        # # go through deserialized edges:
        # for edge_data in data['edges']:
        #     # can we find this node in the scene?
        #     found = False
        #     for edge in all_edges:
        #         if edge.id == edge_data['id']:
        #             found = edge
        #             break
        #
        #     if not found:
        #         new_edge = Edge(self).deserialize(edge_data, hashmap)
        #         # print("New edge for", edge_data)
        #     else:
        #         found.deserialize(edge_data, hashmap)
        #         all_edges.remove(found)
        #
        # # remove nodes which are left in the scene and were NOT in the serialized data!
        # # that means they were not in the graph before...
        # while all_edges != []:
        #     edge = all_edges.pop()
        #     edge.remove()

        return True