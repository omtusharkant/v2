import math
from PyQt5.QtGui import *
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from contextmenu import RightClickMenu


class NodeScene(QGraphicsScene):
    mouseMoveSignal = pyqtSignal(QGraphicsSceneMouseEvent)
    def __init__(self, parent=None):
        super(NodeScene, self).__init__(parent)
        self.gridSize = 20
        self.gridSquares = 5
        self._color_background = QColor("#393939")
        self._color_light = QColor("#2f2f2f")
        self._color_dark = QColor("#292929")
        self._pen_light = QPen(self._color_light)
        self._pen_light.setWidth(1)
        self._pen_dark = QPen(self._color_dark)
        self._pen_dark.setWidth(2)
        self.setSceneRect(-50000 // 2, -50000 // 2, 50000, 50000)
        self.setBackgroundBrush(self._color_background)
        self._zoom_factor = 1.0
        self.selectionChanged.connect(self.check_item_selected)
        self.selectedNode = None
        self.setStickyFocus(True)
        self.isfollowing = False

    def check_item_selected(self):
        #print("selected x")
        self.selectedNode = self.selectedItems()
        for item in self.selectedNode:
            item_name = item.data(0)  # Assuming the name is stored in data role 0
            print(f"Selected item: {item_name}")

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)
        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.ceil(rect.bottom()))
        first_left = left - (left % self.gridSize)
        first_top = top - (top % self.gridSize)

        lines_light, lines_dark = [], []
        for x in range(first_left, right, self.gridSize):
            if x % (self.gridSize * self.gridSquares) != 0:
                lines_light.append(QLine(x, top, x, bottom))
            else:
                lines_dark.append(QLine(x, top, x, bottom))

        for y in range(first_top, bottom, self.gridSize):
            if y % (self.gridSize * self.gridSquares) != 0:
                lines_light.append(QLine(left, y, right, y))
            else:
                lines_dark.append(QLine(left, y, right, y))

        painter.setPen(self._pen_light)
        painter.drawLines(lines_light)

        painter.setPen(self._pen_dark)
        painter.drawLines(lines_dark)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new_position):
        self._position = new_position

    def cursorChangeHandler(self):
        cursor = self.views()[0].viewport().cursor()
        print(f"Cursor changed to: {cursor}")

    def mousePressEvent(self, event):
        
        if event.button() == Qt.RightButton:
            #print(f"y={event.screenPos().y()},x={event.screenPos().x()},\nSy={event.scenePos().y()},Sx={event.scenePos().x()}")
            self.position = event.scenePos()
            menu = RightClickMenu(self.views()[0], self)
            menu.exec_(event.screenPos())
        

    def mouseMoveEvent(self, event):
        self.mouseMoveSignal.emit(event)
        
        
    def wheelEvent(self, event):
        # Zoom in or out based on the mouse wheel delta
        zoom_in_factor = 1.2
        zoom_out_factor = 1.0 / zoom_in_factor

        if event.delta() > 0:
            # Zoom in
            self._zoom_factor *= zoom_in_factor
        else:
            # Zoom out
            self._zoom_factor *= zoom_out_factor

        # Apply a scale transformation to the view
        self.views()[0].setTransform(QTransform().scale(self._zoom_factor, self._zoom_factor))

    
    