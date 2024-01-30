from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi  # Import loadUi to load UI files

from scene import NodeScene

class MenuBar(QMainWindow):
    def __init__(self):
        super(MenuBar, self).__init__()

        # Load the UI file
        loadUi(r"ui\tabbar.ui", self)
        
       # Create a container widget
        container_widget = QWidget()

        # Create a QGraphicsView to display NodeScene
        self.graphics_view = QGraphicsView()
        self.graphics_view.setScene(NodeScene())

        # Set up a layout for the container widget
        container_layout = QVBoxLayout(container_widget)
        container_layout.addWidget(self.graphics_view)
        
        # Add the container widget to a tab
        for i in range(self.Tabar.count()):
            self.Tabar.removeTab(0)
        self.Tabar.addTab(container_widget, f"New Tab {self.Tabar.count()+1}")

        
        
        
    def graphics_view(self):
        # Create a QGraphicsView to display NodeScene
        self.graphics_view = QGraphicsView()
        self.graphics_view.setScene(NodeScene())

        

