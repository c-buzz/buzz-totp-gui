from PyQt5 import QtGui
from PyQt5 import QtCore
from models.BTAccount import BTAccount
from PyQt5.QtCore import QEvent, QItemSelection, QModelIndex, QObject, Qt
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QKeyEvent, QKeySequence
from ui.BTUIProfileMainWindow import Ui_ProfileMainWindow
from models.ProfileAccountsModel import CustomRoleAccessAccountObject, ProfileAccountsModel
from PyQt5.QtWidgets import QAbstractItemView, QApplication, QMainWindow

class ProfileMainWindow(Ui_ProfileMainWindow, QMainWindow):
    def __init__(self, model : ProfileAccountsModel = None):
        super().__init__()
        self.setupUi(self)
        if model:
            self.listProfiles.setModel(model)

        self.baseTitle = self.windowTitle()

        # Actions connection
        self.actionDeleteAccount.triggered.connect(self.deleteAccount)
        self.actionAddAccount.triggered.connect(self.addAccount)
        self.actionRenameAccount.triggered.connect(self.onActionRenameAccount)
        self.actionChangePassword.triggered.connect(self.onChangePassword)
        self.listProfiles.addAction(self.actionAddAccount)
        self.listProfiles.addAction(self.actionRenameAccount)
        self.listProfiles.addAction(self.actionDeleteAccount)

        # Signals connection
        self.listProfiles.doubleClicked.connect(self.onItemDoubleClick)
        self.listProfiles.selectionModel().selectionChanged.connect(self.onListProfilesSelectionChanged)
        self.listProfiles.model().dataChanged.connect(self.onDataChanged)
        self.listProfiles.model().dataSaved.connect(self.onDataSaved)
        self.buttonShowTOTP.clicked.connect(lambda: self.onItemDoubleClick(self.listProfiles.currentIndex()))

        # Widgets configuration
        self.listProfiles.setAcceptDrops(True)
        self.listProfiles.setDropIndicatorShown(True)
        self.listProfiles.installEventFilter(self)
        self.listProfiles.setDragDropMode(QAbstractItemView.DragDropMode.DropOnly)

        # Check if any events are to be saved yed
        self.pendingChanges = False


    def eventFilter(self, obj:QObject, event:QEvent):
        if event.type() == QEvent.Type.KeyPress or event.Type == QEvent.Type.ShortcutOverride:
            keyEvent = QKeyEvent(event)
            if keyEvent.matches(QKeySequence.StandardKey.Paste):
                self.onPaste()
            elif keyEvent.matches(QKeySequence.StandardKey.Save):
                self.onSave()
        return False

    def onProfileListDropEvent(self, e:QDropEvent):
        """ To be reimplemented """
        pass

    def onProfileListDragEnterEvent(self, event:QDragEnterEvent):
        """ To be reimplemented """
        return

    def onPaste(self):
        """ To be reimplemented by the controller """
        data = QApplication.clipboard().mimeData()
        action = Qt.DropAction.CopyAction
        row = self.listProfiles.model().rowCount()
        if self.listProfiles.model().canDropMimeData(data, action, row, 0, QModelIndex()):
            self.listProfiles.model().dropMimeData(data, action, row, 0, QModelIndex())
        pass

    def onSave(self):
        """ To be reimplemented by the controller """
        
        pass

    def onDataChanged(self):
        self.pendingChanges = True
        self.setWindowTitle(self.baseTitle + '*')

    def onDataSaved(self):
        self.pendingChanges = False
        self.setWindowTitle(self.baseTitle)

    def onActionRenameAccount(self):
        current_index = self.listProfiles.currentIndex()
        self.listProfiles.edit(current_index)

    def onActionDeleteAccountTriggered(self):
        account_index = self.listProfiles.currentIndex()
        self.deleteAccount(account_index)
  
    def deleteAccount(self):
        account_index = self.listProfiles.currentIndex()
        account = account_index.data(CustomRoleAccessAccountObject)
        account_row = self.listProfiles.currentIndex().row()
        self.listProfiles.model().removeRow(account_row)
        return account

    def addAccount(self):
        """ To be reimplemented """
        pass

    def onItemDoubleClick(self,  index:QModelIndex()):
        """ To be reimplemented """
        pass

    def onListProfilesSelectionChanged(self, selected:QItemSelection, deselected:QItemSelection):
        if not selected.isEmpty():
            account : BTAccount = selected.indexes()[0].data(CustomRoleAccessAccountObject)
            if account.is_totp_visible:
                self.buttonShowTOTP.setText("Hide TOTP")
            else:
                self.buttonShowTOTP.setText("Show TOTP")

    def onChangePassword(self):
        # To be reimplemented
        return
 