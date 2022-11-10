from collections import OrderedDict
from Node_Serializable import *
from node_graphics_edge import *

EDGE_TYPE_DIRECT = 1
EDGE_TYPE_BEZIER = 2

DEBUG = False


class Edge(Serializable):
    def __init__(self, scene, start_socket= None, end_socket = None, edge_type=EDGE_TYPE_DIRECT):
        super().__init__()
        self.myScene = scene

        #default init
        self._start_socket=None
        self._end_socket=None

        self.start_socket = start_socket
        self.end_socket = end_socket
        self.edge_type = edge_type

        # 3shan n7rk el edges m3 el sockets #deleted
        # self.start_socket.edge = self
        # if self.end_socket is not None:
        #     self.end_socket.edge = self

       ### deleted line self.grEdge = GraphicsEdgeDirect(self) if edge_type == EDGE_TYPE_DIRECT else GraphicsEdgeBezier(self)

        self.updatePosition()
        # if DEBUG: print("Edge: ", self.grEdge.posSource, "to ", self.grEdge.posDestination)
        ### deleted self.myScene.myGrScene.addItem(self.grEdge)
        self.myScene.addEdge(self)

    def __str__(self):
        return "<Edge %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])

    @property
    def start_socket(self): return self._start_socket

    @start_socket.setter
    def start_socket(self,value):
        # if we assigned to some sockets before, delete us from the socket
        if self._start_socket is not None:
            self._start_socket.removeEdge(self)

         #assign new start socket
        self._start_socket = value
        # addEdge to the socket class
        if self.start_socket is not None:
            self.start_socket.setConnectedEdge(self)


    @property
    def end_socket(self):
        return self._end_socket

    @end_socket.setter
    def end_socket(self, value):
        if self._end_socket is not None:
            self._end_socket.removeEdge(self)
        # if we assigned to some sockets before, delete us from the socket
        # assign new end socket
        self._end_socket = value
        #addEdge to the socket class
        if self.end_socket is not None:
            self.end_socket.setConnectEdge(self)

    @property
    def edge_type(self): return self._edge_type

    @edge_type.setter
    def edge_type(self,value):
        if hasattr(self, 'grEdge') and self.grEdge is not None:
            self.myScene.myGrScene.removeItem(self.grEdge)

        self._edge_type =value
        if self.edge_type == EDGE_TYPE_DIRECT:
            self.grEdge= GraphicsEdgeDirect(self)
        elif self.edge_type== EDGE_TYPE_BEZIER:
            self.grEdge = GraphicsEdgeBezier(self)
        else:
            self.grEdge = GraphicsEdgeBezier(self)

        self.myScene.myGrScene.addItem(self.grEdge)

        if self.start_socket is not None:
            self.updatePosition()

    def updatePosition(self):
        source_pos = self.start_socket.getSocketPosition()
        source_pos[0] += self.start_socket.node.grNode.pos().x()
        source_pos[1] += self.start_socket.node.grNode.pos().y()
        self.grEdge.setSource(*source_pos)
        if self.end_socket is not None:
            end_pos = self.end_socket.getSocketPosition()
            end_pos[0] += self.end_socket.node.grNode.pos().x()
            end_pos[1] += self.end_socket.node.grNode.pos().y()
            self.grEdge.setDestination(*end_pos)
        else:
            self.grEdge.setDestination(*source_pos)
        self.grEdge.update()

    def remove_from_socket(self):
        #TODO: FIX ME !!!
        #if self.start_socket is not None:
         #   self.start_socket.removeEdge(None)
        #if self.end_socket is not None:
         #   self.end_socket.removeEdge(None)
        self.end_socket = None
        self.start_socket = None

    def remove(self):
        if DEBUG: print("# Removing Edge", self)
        if DEBUG: print(" - remove edge from all sockets")
        self.remove_from_socket()
        if DEBUG: print(" - remove grEdge")
        self.myScene.myGrScene.removeItem(self.grEdge)
        self.grEdge = None
        if DEBUG: print(" - remove edge from scene")
        try:
            self.myScene.removeEdge(self)
        except ValueError:
            pass
        if DEBUG: print(" - everything is done.")


    def serialize(self):
        return OrderedDict([
            ('id', self.id),
            ('edge_type', self.edge_type),
            ('start', self.start_socket.id),
            ('end', self.end_socket.id),
        ])

    def deserialize(self, data, hashmap={}):
        self.id = data['id']
        self.start_socket = hashmap[data['start']]
        self.end_socket = hashmap[data['end']]
        self.edge_type = data['edge_type']
        return True
