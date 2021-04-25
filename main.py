# This Python file uses the following encoding: utf-8
from BTController import BTController
import sys
import os


from PyQt5.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = BTController()
    sys.exit(app.exec_())
