import inspect
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import time
from random import randint

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
        #add +
        add_node_action = QMenu("Add Node", self)
        
        PRINTND = add_node_action.addAction("Print")
        PRINTND.triggered.connect(lambda: self.addNode(PRINTND))
        
        GetND=add_node_action.addAction("get")
        GetND.triggered.connect(lambda: self.addNode(PRINTND))
        
        self.addMenu(add_node_action)
        
        

        dropdown_action = QWidgetAction(self)
        dropdown_action.setDefaultWidget(self.dropdown)
        self.addAction(dropdown_action)

        submenu = QMenu("Submenu", self)
        

        self.addMenu(submenu)

        self.addAction("Exit")

        self.search_box.textChanged.connect(self.filterActions)
        self.dropdown.currentIndexChanged.connect(self.handleDropdown)
    def addNode(self,menu_action):
        
         
        # Change the cursor to move or drag
        self.setCursor(Qt.ClosedHandCursor)
        print(self.node_scene.position)
        # Retrieve the scene position from the last right-click event
        
        all_classes = inspect.getmembers(__import__(__name__), inspect.isclass)

        for i in all_classes:
            print(i,)
        else:
                pass
        
        specific_position = self.node_scene.position
        
        # Create a new PRINTND
        print_node = PRINTND("New Node",specific_position, self.node_scene)
        #print_node.setPos(specific_position)

        # Add the PRINTND to the scene
        self.node_scene.addItem(print_node)
        

    def filterActions(self, text):
        for action in self.actions():
            action.setVisible(text.lower() in action.text().lower() or not text)

    def handleDropdown(self, index):
        print(f"Selected option: {self.dropdown.itemText(index)}")






class PRINTND(QGraphicsTextItem):
    def __init__(self, text, specific_position, scene):
        super(PRINTND, self).__init__(text)
        self.scene = scene
        self.setAcceptHoverEvents(True)
        self.specific_position = specific_position
        self.printNodeInfo()

    def printNodeInfo(self):
        print(f"Node Text: {self.toPlainText()}")
        print(f"Node Position: {self.scenePos()}")
        self.setCursor(Qt.ClosedHandCursor)

        PrintBg = QGraphicsRectItem(self.specific_position.x(), self.specific_position.y(), 350, 450)
        PrintBg.setBrush(Qt.red)
        PrintBg.setFlag(QGraphicsItem.ItemIsMovable)
        PrintBg.setFlag(QGraphicsItem.ItemIsSelectable)
        PrintBg.setData(0, randint(0, 10))
        self.scene.addItem(PrintBg)

    def boundingRect(self):
        return self.childrenBoundingRect()

    def paint(self, painter, option, widget):
        pass 
    