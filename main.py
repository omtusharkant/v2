import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

from window import *


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NodeCode()
    window.showMaximized()
    sys.exit(app.exec_())
