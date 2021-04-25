
from PyQt5.QtWidgets import QMessageBox

def bt_raise_error(message):
    #box = QMessageBox(icon=QMessageBox.Icon.Critical, title="Error", text=message)
    box = QMessageBox(QMessageBox.Icon.Critical, "Error", message)
    box.exec()
    # to be completed

def bt_ask_for_confirm(message):
    buttons = QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel
    box = QMessageBox(QMessageBox.Icon.Question, "Confirm Request", message,buttons)
    
    return box.exec()