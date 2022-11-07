from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from Graphics_Socket import *

MODE_NOOP = 1
MODE_EDGE_DRAG = 2

EDGE_DRAG_START_THRESHOLD = 10

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

    def rightMouseButtonRelease(self, event):
        super().mouseReleaseEvent(event)

        # Return whichever object we are clicking on

    def getItemAtClick(self, event):
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj

    def edgeDragStart(self, item):
        print('Start dragging edge')
        print('  assign Start Socket')

    def edgeDragEnd(self, item):
        self.mode = MODE_NOOP
        print("End dragging edge")

        if type(item) is QDMGraphicSocket:
            print(" Assign end socket")
            return True

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