from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class GraphicsNode(QGraphicsItem):
    def __init__(self, node, parent=None):
        super().__init__(parent)
        self.node = node
        self.content = self.node.content


        # init our flags
        self.hovered = False
        self._last_selected_state = False

        self.initSizes()
        self.initAssets()

        #init Sockets here
        self.initSocket()


        #init content here
        self.initContent()

        self.initUI()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.node.updateConnectedEdges()


    @property
    # title of this `Node` (getter: current Graphics Node title) (setter: stores and make visible the new title)
    def title(self):
        return self._title
    @title.setter
    def title(self, value):
        self._title = value
        self.title_item.setPlainText(self._title)

    def initSizes(self):
        """Set up internal attributes like `width`, `height`, etc."""
        self.width = 200
        self.height = 240

        self.edge_roundness = 10
        self.edge_padding = 10

        self.title_height = 25
        self.title_horizontal_padding = 40
        self.title_vertical_padding = 1

    def initUI(self):
        """Set up this ``QGraphicsItem``"""
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setAcceptHoverEvents(True)

        # init title
        self.initTitle()
        self.title = self.node.title


    def initAssets(self):
        """Initialize ``QObjects`` like ``QColor``, ``QPen`` and ``QBrush``"""
        self._title_color = QColor("#FFFFFF")
        self._title_font = QFont("Cairo", 10)

        self._color = QColor("#ef974d") # 7dod el node nfsha
        self._color_selected = QColor("#F87217") # 7dod el node when selected
        self._color_hovered = QColor("#F87217") # outer color ll node ely est5dmtha,msh byzhr 3'er lma at least a selectha mara

        self._pen_default = QPen(self._color)
        self._pen_default.setWidthF(2)
        self._pen_selected = QPen(self._color_selected)
        self._pen_selected.setWidthF(2)
        self._pen_hovered = QPen(self._color_hovered)
        self._pen_hovered.setWidthF(0)

        self._brush_title = QBrush(QColor("#131922")) # color of the title node background, lon el node fl goz2 bta3 el title
        self._brush_background = QBrush(QColor("#1A202C"))  # color of the content background , lon el node fl goz2 bta3 el content

    def boundingRect(self):
        """Defining Qt' bounding rectangle"""
        return QRectF(0,0,self.width,self.height).normalized()

    def initTitle(self):
        """Set up the title Graphics representation: font, color, position, etc."""
        self.title_item = QGraphicsTextItem(self)
        self.title_item.node = self.node
        self.title_item.setDefaultTextColor(self._title_color)
        self.title_item.setFont(self._title_font)
        self.title_item.setPos(self.title_horizontal_padding, 0)
        self.title_item.setTextWidth(self.width - 2 * self.title_horizontal_padding)



    def initContent(self):
        self.grContent = QGraphicsProxyWidget(self)
        self.content.setGeometry(self.edge_roundness,self.title_height + self.edge_roundness,
                                 self.width - 2 * self.edge_roundness, self.height - 2 * self.edge_roundness - self.title_height)
        self.grContent.setWidget(self.content)

    def initSocket(self):
        pass

    def onSelected(self):
        self.node.scene.grScene.itemSelected.emit()

    def doSelect(self, new_state=True):
        self.setSelected(new_state)
        self._last_selected_state = new_state
        if new_state: self.onSelected()

    def hoverEnterEvent(self, event: 'QGraphicsSceneHoverEvent'):
         self.hovered = False
         self.update()

    def hoverLeaveEvent(self, event: 'QGraphicsSceneHoverEvent'):
        """Handle hover effect"""
        self.hovered = True
        self.update()

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        # title
        path_title = QPainterPath()
        path_title.setFillRule(Qt.WindingFill)
        path_title.addRoundedRect(0, 0, self.width, self.title_height, self.edge_roundness, self.edge_roundness)
        path_title.addRect(0, self.title_height - self.edge_roundness, self.edge_roundness, self.edge_roundness)
        path_title.addRect(self.width - self.edge_roundness, self.title_height - self.edge_roundness, self.edge_roundness, self.edge_roundness)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_title)
        painter.drawPath(path_title.simplified())


        # content
        path_content = QPainterPath()
        path_content.setFillRule(Qt.WindingFill)
        path_content.addRoundedRect(0, self.title_height, self.width, self.height - self.title_height, self.edge_roundness, self.edge_roundness)
        path_content.addRect(0, self.title_height, self.edge_roundness, self.edge_roundness)
        path_content.addRect(self.width - self.edge_roundness, self.title_height, self.edge_roundness, self.edge_roundness)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPath(path_content.simplified())


        # outline
        path_outline = QPainterPath()
        path_outline.addRoundedRect(-1, -1, self.width+2, self.height+2, self.edge_roundness, self.edge_roundness)
        painter.setBrush(Qt.NoBrush)
        if self.hovered:
            painter.setPen(self._pen_hovered)
            painter.drawPath(path_outline.simplified())
            painter.setPen(self._pen_default)
            painter.drawPath(path_outline.simplified())
        else:
            painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
            painter.drawPath(path_outline.simplified())