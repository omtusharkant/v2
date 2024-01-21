from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from scene import NodeScene

class MenuBar(QMainWindow):
    def __init__(self):
        super(MenuBar, self).__init__()

        # Create a central widget with a graphics view
        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)

        layout = QVBoxLayout(self.tab_widget)

        self.add_tab()

        # Create actions for the file menu
        self.new_action = QAction("New", self)
        self.new_action.triggered.connect(self.add_tab)

        self.open_action = QAction("Open", self)
        self.open_action.triggered.connect(self.open_document)

        # Create a file menu
        file_menu = self.menuBar().addMenu("File")
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.open_action)

    def add_tab(self):
        # Create a new QGraphicsScene and QGraphicsView for each document
        self.scene = NodeScene(self)
        self.view = QGraphicsView(self.scene)

        # Set up the view properties
        self.view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.view.setRenderHint(QPainter.Antialiasing)

        # Add the view as a new tab
        self.tab_widget.addTab(self.view, f"Document {self.tab_widget.count() + 1}")

    def open_document(self):
        # Open a file dialog to select a file to open
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "Open Document", "", "All Files (*);;Text Files (*.txt)")

        if file_path:
            # Create a new document and load content from the file
            self.add_document()