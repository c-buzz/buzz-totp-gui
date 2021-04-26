# This Python file uses the following encoding: utf-8
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QSettings
from BTController import BTController
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName('BuzzTOTP')
    app.setApplicationVersion('0.0.1')
    QSettings.setDefaultFormat(QSettings.Format.IniFormat)
    controller = BTController()
    sys.exit(app.exec_())
