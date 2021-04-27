from BTSettings import BTSettings
import os
import time
from typing import List, Optional, Union

from PyQt5 import QtCore
from PyQt5.QtCore import QModelIndex, QThread
from PyQt5.QtGui import QCloseEvent, QDragEnterEvent
from PyQt5.QtWidgets import QApplication

import BTUtils as utils
from BTErrorManager import *
from models.BTAccount import BTAccount
from models.ProfileAccountsModel import ProfileAccountsModel
from views.NewAccountView import NewAccountWindow
from views.ProfileWindowView import ProfileMainWindow


class BTProfileController(ProfileMainWindow):
    
    def __init__(self, filename, password):
        self.__accounts_list : List[BTAccount] = []
        self.__password = ''
        self.accounts_model = ProfileAccountsModel(filename, password)
        self.new_account_handler = NewAccountWindow()
        super().__init__(self.accounts_model)
        self.baseTitle = "BuzzTotp - " + os.path.basename(filename)
        self.setWindowTitle(self.baseTitle)

        # Load settings from app
        self.settings = BTSettings()
        self.actionCopy2Clipboard.setChecked(self.settings.copy_to_clipboard)
        self.actionAutoTOTPHide.setChecked(self.settings.auto_hide_totp)
        self.actionAutoTOTPHide.changed.connect(self.onActionAutoTOTPHideChanged)
        self.actionCopy2Clipboard.changed.connect(self.onActionAutoTOTPHideChanged)

        # NB! The action Change Profile is managed and connected into the main controller (outside this object)

    def onActionCopy2CliboardChange(self):
        self.settings.copy_to_clipboard = self.actionCopy2Clipboard.isChecked()
        self.settings.sync()

    def onActionAutoTOTPHideChanged(self):
        self.settings.auto_hide_totp = self.actionAutoTOTPHide.isChecked()
        self.settings.sync()
        
    def checkPassword(filename, password) -> bool:
        if not(os.path.exists(filename) and os.path.isfile(filename)):
            return False
        try:
            m = ProfileAccountsModel(filename,password)
            return True
        except:
            return False

    def deleteAccount(self):
        if bt_ask_for_confirm('An account is being deleted') == QMessageBox.StandardButton.Yes:
            account = super().deleteAccount()

    def delete_account(self, account : Union[str, BTAccount], persist : bool = False):
        account = self.get_account(account)
        if account is not None:
            self.__accounts_list.remove(account)
            if persist:
                self.write_to_file()
        else:
            bt_raise_error("Account passed to be deleted not found")

    def addAccount(self, account : Optional[BTAccount], persist : bool = False) -> bool:
        out = True
        if not account:
            account = self.new_account_handler.createNewAccount()
        if account:
            self.accounts_model.addAccount(account)
        else:
            out = False
        
        if out and persist:
            self.write_to_file()
        return out

    def onItemDoubleClick(self, index:QModelIndex):
        self.toggleTOTP(index)
        btn_text = "Hide TOTP" if self.getAccount(index).is_totp_visible else "Show TOTP"
        self.buttonShowTOTP.setText(btn_text)

    def toggleTOTP(self, account:Union[QModelIndex, BTAccount, int]):
        account = self.getAccount(account)
        if account.is_totp_visible:
            self.hideTOTP(account)
        else:
            self.showTOTP(account)

    def showTOTP(self, account:Union[QModelIndex, BTAccount, int]):
        account = self.getAccount(account)
        if account:
            if account.visibility_thread:
                account.visibility_thread.terminate()
            account.visibility_thread = None

            if not account.is_totp_visible:
                """ Show request from hidden condition --> Timed function to be launched"""
                # TODO: Base this upon configuration file
                delay = account.time_to_change + account.interval
                self.visibilityThreadFunction(account, delay)
            
            account.is_totp_visible = True
            self.accounts_model.layoutChanged.emit()
            if self.actionCopy2Clipboard.isChecked():
                QApplication.clipboard().setText(account.now())

        else:
            bt_raise_error('Account passed not valid')

    def visibilityThreadFunction(self, account:BTAccount, timer:int):
        
        class SubThread(QThread):
            func = QtCore.pyqtSignal()
            def __init__(self,delay):
                super().__init__()
                self.delay = delay
            def run(self):                
                time.sleep(self.delay)
                self.func.emit()

        thread = SubThread(timer)
        thread.func.connect(lambda: self.hideTOTP(account))
        account.visibility_thread = thread
        thread.start()
        
    def hideTOTP(self, account:Union[QModelIndex, BTAccount, int]):
        account = self.getAccount(account)
        if account:
            if account.visibility_thread:
                account.visibility_thread.terminate()
            account.visibility_thread = None
            account.is_totp_visible = False
            self.accounts_model.layoutChanged.emit()
            QApplication.clipboard().clear()

    def isTOTPVisible(self, account:Union[QModelIndex, BTAccount, int]):
        account = self.getAccount(account)
        if account:
            return account.is_totp_visible
        else:
            bt_raise_error('Account passed not valid')

    def getAccount(self,account:Union[QModelIndex, BTAccount, int]):
        if type(account) == QModelIndex:
            return self.accounts_model.accounts[account.row()] if account.isValid() else None
        elif type(account) == int:
            index = self.accounts_model.index(account)
            if index.isValid():
                account = self.accounts_model.accounts[account]
            else:
                return None
        return account

    def onProfileListDragEnterEvent(self, event:QDragEnterEvent):
        if utils.mime_data_valid(event.mimeData()):
            event.acceptProposedAction()

    def onSave(self):
        super().onSave()
        self.accounts_model.write_to_file()

    def closeEvent(self, event: QCloseEvent) -> None:
        accept = True
        if self.pendingChanges:
            message = 'Some changes have not been saved. Save them before closing?'
            buttons = QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel
            response = QMessageBox.question(self, "Pending Changes", message, buttons)
            if response == QMessageBox.StandardButton.Cancel:
                accept = False
            elif response == QMessageBox.StandardButton.Yes:
                self.accounts_model.write_to_file()
        if accept:
            event.accept()
        else:
            event.ignore()

    def show(self) -> None:
        # Update the settings with last profile
        self.settings.last_profile = self.accounts_model.filename
        return super().show()