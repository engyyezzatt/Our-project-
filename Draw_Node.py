from Graphics_Node import *
from Node_Content import *
from Node_Socket import *


class Node():
    def __init__(self, scene, title="Node Undefined", inputs=[], outputs=[]):
        if outputs is None:
            outputs = []
        self.scene = scene

        self.title = title

        self.content = NodeContent()
        self.grNode = GraphicsNode(self)

        self.scene.addNode(self)
        self.scene.myGrScene.addItem(self.grNode)

        # Create sockets for inputs and outputs
        self.inputs = []
        self.outputs = []
        counter = 0

        for item in inputs:
            socket = Socket(node=self, index=counter, position=LEFT_TOP,socket_type =item )
            counter += 1
            self.inputs.append(socket)

        counter = 0
        for item in outputs:
            socket = Socket(node=self, index=counter, position=RIGHT_BOTTOM,socket_type =item)
            counter += 1
            self.outputs.append(socket)

    def __str__(self):
        return "<Node %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])

    @property
    def pos(self):
        return self.grNode.pos()

    def setpos(self, x, y):
        self.grNode.setPos(x,y)

    def getSocketPosition(self, index, position):
        x = 0 if (position in (LEFT_TOP, LEFT_BOTTOM)) else self.grNode.width

        if position in (LEFT_BOTTOM, RIGHT_BOTTOM):
            # start from bottom
            y = self.grNode.height - self.grNode.edge_roundness - self.grNode.edge_padding - index * 22
        else:
            # start from top
            y = self.grNode.title_height + self.grNode.edge_padding + self.grNode.edge_roundness + index * 22

        return [x, y]

        # 3shan n7rk el edges m3 el sockets with one edge only not multiple
    def updateConnectedEdges(self):
        for socket in self.inputs + self.outputs:
            if socket.hasEdge():
                socket.edge.updatePosition()
