from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from menutab import MenuBar

class NodeCode(QMainWindow):
    def __init__(self):
        super(NodeCode, self).__init__()

        # Set up the main window
        self.setWindowTitle("Node Code")
        self.setStyleSheet("background-color: #424242;")

        self.menu = MenuBar()
        self.setCentralWidget(self.menu)
       # Maximize the window
        self.showMaximized()

        


    