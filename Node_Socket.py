from collections import OrderedDict
from Node_Serializable import *
from Graphics_Socket import *

LEFT_TOP = 1
LEFT_BOTTOM = 2
RIGHT_TOP = 3
RIGHT_BOTTOM = 4


class Socket(Serializable):
    def __init__(self, node, index=0, position=LEFT_TOP,socket_type=1, multi_edges=True):
        super().__init__()
        self.node = node
        self.index = index
        self.position = position
        self.socket_type = socket_type # da w ely fl constractor w kman f class draw node lazmto en el node llma yt3mlha create tt3ml create b default 1 input
        self.is_multi_edges =multi_edges

        # print("Socket -- creating with", self.index, self.position, "for node", self.node)

        self.grSockets = QDMGraphicSocket(self, self.socket_type)
        self.grSockets.setPos(*self.node.getSocketPosition(index, position))

        self.edges = []

    def __str__(self):
        return "<Socket %s %s..%s>" % ("ME" if self.is_multi_edges else "SE", hex(id(self))[2:5], hex(id(self))[-3:])
    def getSocketPosition(self):
        #print(" GSP: ", self.index, self.position, "node:", self.node)
        res = self.node.getSocketPosition(self.index, self.position)
        #print("  res", res)
        return res

    def addEdge(self, edge):
        self.edges.append(edge)
    def removeEdge(self, edge):
        if edge in self.edges:self.edges.remove(edge)
        else: print("!W:","Socket::removeEdges", "wanna remove edge",edge,"from self.edges but its not in the list!")


# 3shan n7rk el edges m3 el sockets
    def hasEdge(self):
        return self.edges is not None

    def serialize(self):
        return OrderedDict([
            ('id', self.id),
            ('index', self.index),
            ('multi_edges', self.is_multi_edges),
            ('position', self.position),
            ('socket_type', self.socket_type),
        ])

    def deserialize(self, data, hashmap={}):
        self.id = data['id']
        self.is_multi_edges = data['multi_edges']
        hashmap[data['id']] = self

        return True

