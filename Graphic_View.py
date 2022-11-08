
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from Graphics_Socket import *
from node_graphics_edge import *
from node_edge import *

MODE_NOOP = 1
MODE_EDGE_DRAG = 2

EDGE_DRAG_START_THRESHOLD = 10

DEBUG = True

class CrGraphicsView(QGraphicsView):
    def __init__(self, myGrScene, parent=None):
        super().__init__(parent)
        self.myGrScene = myGrScene

        self.initUI()

        self.last_scene_mouse_position = QPoint(0,0)
        self.zoomInFactor = 1.25
        self.zoomClamp = True
        self.zoom = 10
        self.zoomStep = 1
        self.zoomRange = [0, 20]

        self.setScene(self.myGrScene)
        self.mode = MODE_NOOP


    def initUI(self):
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)

        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.RubberBandDrag)

        # enable dropping
        self.setAcceptDrops(True)

    def mousePressEvent(self, event: QMouseEvent):
        """Dispatch Qt's mousePress event to corresponding function below"""
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonPress(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonPress(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonPress(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        """Dispatch Qt's mouseRelease event to corresponding function below"""
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonRelease(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonRelease(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)

    def middleMouseButtonPress(self,event):
        releaseEvent =QMouseEvent(QEvent.MouseButtonRelease,event.localPos(), event.screenPos(),
                                  Qt.LeftButton,Qt.NoButton,event.modifiers())
        super().mouseReleaseEvent(releaseEvent)
        self.setDragMode(QGraphicsView.ScrollHandDrag)

        fakeEvent = QMouseEvent(event.type(),event.localPos(),event.screenPos(),
                                Qt.LeftButton, event.buttons()|Qt.LeftButton,event.modifiers())
        super().mousePressEvent(fakeEvent)

    def middleMouseButtonRelease(self, event: QMouseEvent):
        """When Middle mouse button was released"""
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                Qt.LeftButton, event.buttons() & ~Qt.LeftButton, event.modifiers())
        super().mouseReleaseEvent(fakeEvent)
        self.setDragMode(QGraphicsView.RubberBandDrag)

    def leftMouseButtonPress(self, event):
        # Getting the last item we pressed the mouse on
        item = self.getItemAtClick(event)
        # Here we are storing the position of the last left mouse click
        self.last_lmb_click_scene_pos = self.mapToScene(event.pos())

        # Printing the logic on the run
        if type(item) is QDMGraphicSocket:
            if self.mode == MODE_NOOP:
                self.mode = MODE_EDGE_DRAG
                self.edgeDragStart(item)
                return

        if self.mode == MODE_EDGE_DRAG:
            res = self.edgeDragEnd(item)
            if res: return

        super().mousePressEvent(event)

    def leftMouseButtonRelease(self, event):
        # Gets which item we released the mouse on
        item = self.getItemAtClick(event)

        if self.mode == MODE_EDGE_DRAG:
            if self.distanceBetweenClickAndReleaseIsOFF(event):
                res = self.edgeDragEnd(item)
                if res: return

        super().mouseReleaseEvent(event)

    def rightMouseButtonPress(self, event):
        super().mousePressEvent(event)

        item = self.getItemAtClick(event)
        if DEBUG:
            if isinstance(item, GraphicsEdge): print('RMB DEBUG:', item.edge, ' connecting sockets:',
                                                        item.edge.start_socket, '<-->', item.edge.end_socket)
            if type(item) is QDMGraphicSocket: print("RMB DEBUG: ", item.socket, 'has edge:', item.socket.edge)

            if item is None:
                print('SCENE: ')
                print(' Nodes:')
                for node in self.myGrScene.scene.nodes: print('    ', node)
                print(' Edges:')
                for edge in self.myGrScene.scene.edges: print('    ', edge)




    def rightMouseButtonRelease(self, event):
        super().mouseReleaseEvent(event)

        # Return whichever object we are clicking on

    def mouseMoveEvent(self, event):
        if self.mode == MODE_EDGE_DRAG:
            pos = self.mapToScene(event.pos())
            self.dragEdge.grEdge.setDestination(pos.x(), pos.y())
            self.dragEdge.grEdge.update()

        super().mouseMoveEvent(event)


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.deleteSelected()
        else:
            super().keyPressEvent(event)


    def deleteSelected(self):
        for item in self.myGrScene.selectedItems():
            if isinstance(item, GraphicsEdge):
                item.edge.remove()
            elif hasattr(item, 'node'):
                item.node.remove()


    def getItemAtClick(self, event):
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj

    def edgeDragStart(self, item):
        if DEBUG: print('View::edgeDragStart ~ Start dragging edge')
        if DEBUG: print('View::edgeDragStart ~ assign Start Socket to:', item.socket)
        self.previousEdge = item.socket.edge
        self.las_start_socket = item.socket
        self.dragEdge = Edge(self.myGrScene.scene, item.socket, None, EDGE_TYPE_BEZIER)
        if DEBUG: print('View::edgeDragStart ~  dragEdge:', self.dragEdge)

    def edgeDragEnd(self, item):
        self.mode = MODE_NOOP

        if type(item) is QDMGraphicSocket:
            if item.socket != self.las_start_socket:
                if DEBUG: print('View::edgeDragEnd ~  , previous edge:', self.previousEdge)
                if item.socket.hasEdge():
                    item.socket.edge.remove()
                if DEBUG: print('View::edgeDragEnd ~ Assign end socket', item.socket)
                if self.previousEdge is not None: self.previousEdge.remove()
                if DEBUG: print('View::edgeDragEnd ~ previous edge removed')
                self.dragEdge.start_socket = self.las_start_socket
                self.dragEdge.end_socket = item.socket
                self.dragEdge.start_socket.setConnectedEdge(self.dragEdge)
                self.dragEdge.end_socket.setConnectedEdge(self.dragEdge)
                if DEBUG: print('View::edgeDragEnd ~  reassigned start & end sockets to drag edge')
                self.dragEdge.updatePosition()

                return True

        if DEBUG: print('View::edgeDragEnd ~ End dragging edge')
        self.dragEdge.remove()
        self.dragEdge = None
        if DEBUG: print('View::edgeDragEnd ~ about to set socket to previous edge:', self.previousEdge)
        if self.previousEdge is not None:
            self.previousEdge.start_socket.edge = self.previousEdge
        # if DEBUG: print('View::edgeDragEnd ~ about to set socket to previous edge:', self.previousEdge)
        # if self.previousEdge is not None:
        #     self.previousEdge.start_socket.edge = self.previousEdge
        if DEBUG: print('View::edgeDragEnd ~ everything is done.')

        return False

    def distanceBetweenClickAndReleaseIsOFF(self, event):
        new_lmb_release_scene_pos = self.mapToScene(event.pos())
        dist_scene = new_lmb_release_scene_pos - self.last_lmb_click_scene_pos
        edge_drag_threshold_sq = EDGE_DRAG_START_THRESHOLD * EDGE_DRAG_START_THRESHOLD
        return (dist_scene.x() * dist_scene.x() + dist_scene.y() * dist_scene.y()) > edge_drag_threshold_sq
    def wheelEvent(self, event: QWheelEvent):
        # calculate our zoom Factor
        zoomOutFactor = 1 / self.zoomInFactor

        # calculate zoom
        if event.angleDelta().y() > 0:
            zoomFactor = self.zoomInFactor
            self.zoom += self.zoomStep
        else:
            zoomFactor = zoomOutFactor
            self.zoom -= self.zoomStep


        clamped = False
        if self.zoom < self.zoomRange[0]:
            self.zoom, clamped = self.zoomRange[0], True
        if self.zoom > self.zoomRange[1]:
            self.zoom, clamped = self.zoomRange[1], True

        # set scene scale
        if not clamped or self.zoomClamp is False:
            self.scale(zoomFactor, zoomFactor)