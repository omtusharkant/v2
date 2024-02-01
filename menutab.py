from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi  # Import loadUi to load UI files

from scene import NodeScene

class EditorView(QGraphicsView):
    def __init__(self):
        super(EditorView, self).__init__()

        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.scene = NodeScene()
        self.setScene(self.scene)

        self.last_scene_pos = QPointF()

        self.scene.mouseMoveSignal.connect(self.handleMouseMove)
        

    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonPress(event)

        
        elif event.button() == Qt.LeftButton:
            
            self.item = self.itemAt(event.pos())
            if self.item:
                self.item.setSelected(True)
                self.scene.isfollowing = not self.scene.isfollowing
                print(f" item pressed!")
                self.offset = self.item.pos() - self.mapToScene(event.pos())
                

        
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonRelease(event)


        elif event.button() == Qt.LeftButton:
            self.scene.isfollowing = False
            self.item.setSelected(False)

            
        else:
            super().mouseReleaseEvent(event)

    def handleMouseMove(self, event):
        
        selecteditem = self.scene.selectedNode
        if self.scene.isfollowing:
            #self.offset = self.item.pos() - event.screenPos()
            
            selecteditem[0].setPos(event.scenePos() + self.offset)

    def middleMouseButtonPress(self, event):
        releaseEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(),
                                   Qt.LeftButton, Qt.NoButton, event.modifiers())
        super().mouseReleaseEvent(releaseEvent)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
        super().mousePressEvent(fakeEvent)



    def middleMouseButtonRelease(self, event):
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                Qt.LeftButton, event.buttons() & ~Qt.LeftButton, event.modifiers())
        super().mouseReleaseEvent(fakeEvent)
        self.setDragMode(QGraphicsView.NoDrag)


    

    

class MenuBar(QMainWindow):
    def __init__(self):
        super(MenuBar, self).__init__()

        # Load the UI file
        loadUi(r"ui\tabbar.ui", self)

        

        # Create a button for adding tabs
        add_tab_button = QPushButton("New")
        add_tab_button.clicked.connect(self.addTab)

        # Assuming you have a QTabWidget in your UI named Tabar
        self.tab_widget = self.Tabar

        # Connect the tab close request signal to a function
        self.tab_widget.tabCloseRequested.connect(self.closeTab)
        # Create a vertical layout and add the button to it
        layout = QVBoxLayout()
        layout.addWidget(add_tab_button)

        self.editor_view = EditorView()

        # Create a container widget and set the layout
        container_widget = QWidget()
        container_widget.setLayout(layout)

        # Add the container widget to the right side of the menu bar
        self.menuBar().setCornerWidget(container_widget, Qt.TopRightCorner)
        #intial fitting
        #self.tab_widget.addTab(self.editor_view, "New Tab")
        for T in range(2):
            self.tab_widget.removeTab(0)
            

    def addTab(self):
        # Create a new instance of EditorView for each tab
        

        # Add the EditorView as the widget for the new tab
        new_tab_index = self.tab_widget.addTab(self.editor_view, "New Tab")

        # You can set the current tab to the new one if you want
        self.tab_widget.setCurrentIndex(new_tab_index)

    def closeTab(self, index):
        # Handle tab close request
        if index >= 0:
            self.tab_widget.removeTab(index)