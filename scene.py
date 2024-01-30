import math
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi



class NodeScene(QGraphicsScene):
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
    
    
    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            print(f"y={event.screenPos().y()},x={event.screenPos().x()},\nSy={event.scenePos().y()},Sx={event.scenePos().x()}")
            self.position = event.scenePos()
            menu = RightClickMenu(self.views()[0],self)
            menu.exec_(event.screenPos())
            
        
    
class RightClickMenu(QMenu):
    def __init__(self,scene,node_scene, parent=None):
        super(RightClickMenu, self).__init__("Right-Click Menu", parent)
        self.scene = scene
        self.node_scene = node_scene

        self.search_box = QLineEdit(self)
        self.search_box.setPlaceholderText("Enter text...")
        self.search_box.setContextMenuPolicy(Qt.NoContextMenu)  # Disable default context menu
        search_action = QWidgetAction(self)
        search_action.setDefaultWidget(self.search_box)
        self.addAction(search_action)
        self.dropdown = QComboBox(self)
        self.dropdown.addItem("Option 1")
        self.dropdown.addItem("Option 2")
        self.dropdown.addItem("Option 3")

        self.addAction("Print Location")
        self.addAction("Custom Action 1")
        self.addAction("Custom Action 2")
        self.addSeparator()
        
        add_node_action = QAction("Add Node", self)
        self.addAction(add_node_action)
        add_node_action.triggered.connect(self.addNode)

        dropdown_action = QWidgetAction(self)
        dropdown_action.setDefaultWidget(self.dropdown)
        self.addAction(dropdown_action)

        self.addAction("Exit")

        self.search_box.textChanged.connect(self.filterActions)
        self.dropdown.currentIndexChanged.connect(self.handleDropdown)
    def addNode(self):
         # Change the cursor to move or drag
        self.setCursor(Qt.ClosedHandCursor)
        print(self.node_scene.position)
        # Retrieve the scene position from the last right-click event
        
        specific_position = self.node_scene.position

        rect_item = QGraphicsRectItem(specific_position.x(), specific_position.y(), 50, 50)  # Adjust the size as needed
        rect_item.setBrush(Qt.red)  # Set the brush color
        rect_item.setFlag(QGraphicsItem.ItemIsMovable)
        rect_item.setFlag(QGraphicsItem.ItemIsSelectable)

        self.node_scene.addItem(rect_item)
            

    def filterActions(self, text):
        for action in self.actions():
            action.setVisible(text.lower() in action.text().lower() or not text)

    def handleDropdown(self, index):
        print(f"Selected option: {self.dropdown.itemText(index)}")

