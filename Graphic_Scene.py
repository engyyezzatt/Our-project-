from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import math


class CrGraphicScene(QGraphicsScene):
    def __init__(self, scene ,parent=None):
        super().__init__(parent)

        self.scene = scene

        self.BG_Color = QColor("#283448")#212B3B
        self.setBackgroundBrush(self.BG_Color)

        self.grid_size = 30
        self.grid_Squares = 3

        self.color_light = QColor("#2f4155")#
        self.pen_light = QPen(self.color_light)
        self.pen_light.setWidth(1)

        self.color_dark = QColor("#cdcdcd")#212B3B
        self.pen_dark = QPen(self.color_dark)
        self.pen_dark.setWidth(1)

    def setScene(self, width, height):
        self.setSceneRect(-width//2,-height//2,width, height)


    # Grid:
    def drawBackground(self, painter: QPainter, rect: QRect):
        """Draw background scene grid"""
        super().drawBackground(painter, rect)

        # here we create our grid
        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.ceil(rect.bottom()))

        first_left = left - (left % self.grid_size)
        first_top = top - (top % self.grid_size)

        # compute all lines to be drawn
        lines_light, lines_dark = [], []
        for x in range(first_left, right, self.grid_size):
            if x % (self.grid_size * self.grid_Squares) != 0:
                lines_light.append(QLine(x, top, x, bottom))
            else:
                lines_dark.append(QLine(x, top, x, bottom))

        for y in range(first_top, bottom, self.grid_size):
            if y % (self.grid_size * self.grid_Squares) != 0:
                lines_light.append(QLine(left, y, right, y))
            else:
                lines_dark.append(QLine(left, y, right, y))

        # draw the lines
        painter.setPen(self.pen_light)
        try:
            painter.drawLines(*lines_light)  # supporting PyQt5
        except TypeError:
            painter.drawLines(lines_light)  # supporting PySide2

        painter.setPen(self.pen_dark)
        try:
            painter.drawLines(*lines_dark)  # supporting PyQt5
        except TypeError:
            painter.drawLines(lines_dark)  # supporting PySide2
