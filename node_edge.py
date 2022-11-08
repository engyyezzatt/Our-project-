from node_graphics_edge import *


EDGE_TYPE_DIRECT = 1
EDGE_TYPE_BEZIER = 2

DEBUG = False

class Edge:
    def __init__(self, scene, start_socket, end_socket, edge_type=EDGE_TYPE_DIRECT):

        self.myScene = scene

        self.start_socket = start_socket
        self.end_socket = end_socket

        # 3shan n7rk el edges m3 el sockets
        self.start_socket.edge = self
        if self.end_socket is not None:
            self.end_socket.edge = self

        self.grEdge = GraphicsEdgeDirect(self) if edge_type == EDGE_TYPE_DIRECT else GraphicsEdgeBezier(self)

        self.updatePosition()
        #if DEBUG: print("Edge: ", self.grEdge.posSource, "to ", self.grEdge.posDestination)
        self.myScene.myGrScene.addItem(self.grEdge)
        self.myScene.addEdge(self)

    def __str__(self):
        return "<Edge %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])

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
        if self.start_socket is not None:
            self.start_socket.edge = None
        if self.end_socket is not None:
            self.end_socket.edge = None
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