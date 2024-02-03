import inspect
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
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
        GetND.triggered.connect(lambda: self.addNode(GetND))
        
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

        print(menu_action.text())
        
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






class PRINTND(QGraphicsItem):
    def __init__(self, text, specific_position, scene):
        super(PRINTND, self).__init__()
        self.scene = scene
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)
        self.setAcceptHoverEvents(True)
        self.specific_position = specific_position
        self.rect_width = 250
        self.rect_height =400

        # Set some example data
        self.setData(0, "Print node")
        self.setData(1, "AdditionalInfo")


    def boundingRect(self):
        return QRectF(self.specific_position.x(), self.specific_position.y(), self.rect_width, self.rect_height)

    def paint(self, painter, option, widget):
        ndbg = QRectF(self.specific_position.x(), self.specific_position.y(), self.rect_width, self.rect_height)
        painter.setBrush(QBrush(Qt.red))
        painter.drawRect(ndbg)

        
        titlebg = QRectF(self.specific_position.x() , self.specific_position.y(), self.rect_width,50)
        painter.setBrush(QBrush(Qt.blue))
        painter.drawRect(titlebg)


        font = QFont("winter storm", 16, QFont.Bold)  # Node title
        painter.setFont(font)

        title_text = "Print"  # Change this to your actual title text
        text_rect = QRectF(self.specific_position.x()+15, self.specific_position.y(), self.rect_width, 50)
        painter.setPen(Qt.white)  # Set text color
        painter.drawText(text_rect, title_text)

        font = QFont("lemon milk", 8, )  # description 
        painter.setFont(font)
        description_text = "prints in the console"  # Change this to your actual title text
        dest_rect = QRectF(self.specific_position.x()+15, self.specific_position.y()+25, self.rect_width, 50)
        painter.setPen(Qt.white)  # Set text color
        painter.drawText(dest_rect, description_text)