
import json
from BTErrorManager import bt_raise_error
from typing import List, Union

from PyQt5.QtCore import QAbstractListModel, QMimeData, QModelIndex, QUrl, QVariant, Qt, pyqtSignal
from models.BTAccount import BTAccount
import BTUtils as utils
import os
import imghdr


CustomRole = {}
CustomRole['AccessAccountObject'] = Qt.ItemDataRole.UserRole + 1
CustomRoleAccessAccountObject = Qt.ItemDataRole.UserRole + 1

class ProfileAccountsModel(QAbstractListModel):
    
    
    dataSaved = pyqtSignal()

    def __init__(self, filename, password : str, parent = None):
        super().__init__(parent)
        self.accounts : List[BTAccount] = []
        self.__password = password
        # If the profile file exists, load it, otherwise create a blank one
        if os.path.exists(filename):
            self.load_from_file(filename) 
        else:
            self.write_to_file(filename)
        self.filename = os.path.abspath(filename)

    def setPassword(self, password : str):
        self.__password = password

    def data(self, index:QModelIndex, role:int=Qt.ItemDataRole.DisplayRole):
        if index.isValid():

            account = self.accounts[index.row()]
            if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
                if account.is_totp_visible:
                    return f'{account.name} - {account.now()}'
                else:
                    return account.name
            elif role == CustomRole['AccessAccountObject'] :
                return account

    def rowCount(self, parent = QModelIndex()):
        return len(self.accounts)

    def addAccount(self, account : BTAccount, persist : bool = False):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self.accounts.append(account)
        self.endInsertRows()
        self.dataChanged.emit(QModelIndex(),QModelIndex(), [])
    
    def removeRow(self, row : int):
        self.accounts.pop(row)
        super().removeRow(row)
        self.dataChanged.emit(QModelIndex(), QModelIndex(), [])

    def removeAccount(self, account : Union[BTAccount, str, int], persist : bool = False):
        row = self.get_row(account)
        self.removeRow(row)

        if persist:
            self.write_to_file()

    def setData(self, index : QModelIndex, value : QVariant, role : int = Qt.ItemDataRole.EditRole):
        if (index.isValid() and role == Qt.ItemDataRole.EditRole):
            row = index.row()
                        
            # Check if the name already exists
            if self.get_account(value) is not None:
                return False
            
            # Manage check on update
            if self.accounts[row].update(value):
                self.dataChanged.emit(index, index, [])
                return True
            else:
                bt_raise_error('Name passed not valid')
                return False
        else:
            return False

    def dropMimeData(self, data: QMimeData, action, row, column, parent):
        if self.canDropMimeData(data, action, row, column, parent):
            accounts = utils.get_account_from_mime_data(data)
            for account in accounts:
                self.addAccount(account)
            return True

    def supportedDropActions(self) -> Qt.DropActions:
        return Qt.DropAction.CopyAction | Qt.DropAction.MoveAction

    def canDropMimeData(self, data: QMimeData, action: Qt.DropAction, row: int, column: int, parent: QModelIndex) -> bool:
        if data.hasUrls():
            for url in data.urls():
                if url.isLocalFile():
                    return (imghdr.what(url.toLocalFile()) is not None) # Check if valid image file
                elif url.scheme() == 'otpauth':
                    return True
        elif data.hasText():
            url = QUrl(data.text())
            if url.isValid() and url.scheme() == 'otpauth':
                return True

    def flags(self, index):
        defaultFlags = super().flags(index) | Qt.ItemFlag.ItemIsDropEnabled
        if not index.isValid():
            return Qt.ItemFlag.ItemIsEnabled | defaultFlags
        return defaultFlags | Qt.ItemFlag.ItemIsEditable
    
    def write_to_file(self, filename = None):
        if filename is None:
            filename = self.filename
        writable_accounts_list = []
        for account in self.accounts:
            name = account.name
            uri = account.provisioning_uri()
            dict_account = {"name" : name, "uri": uri}
            writable_accounts_list.append(dict_account)
        writable_object = {'accounts' : writable_accounts_list}
        json_content = json.dumps(writable_object)
        utils.encrypt_file(filename, json_content, self.__password)
        # Check if the dataSaved signal was connected
        if self.receivers(self.dataSaved) > 0:
            self.dataSaved.emit()

    def load_from_file(self, filename = None):
        """
            Load the profile accounts from a file .bt
        """
        if filename is None:
            filename = self.filename

        content = utils.decrypt_file(filename, self.__password)
        content = json.loads(content)

        if 'accounts' not in content:
            raise Exception('No valid bt file')

        json_account_list = content['accounts']

        for json_account in json_account_list:
            name = json_account['name']
            uri = json_account['uri']
            account = BTAccount.fromURI(uri, name)
            self.addAccount(account)
        # Todo: Manage exceptions

    def get_account(self, account : Union[str, BTAccount]) -> BTAccount:
        if type(account) == str:
            l = list(x for x in self.accounts if x.name == account)
            return l[0] if l else None
        else:
            return account if account in self.accounts else None
        
    def get_row(self, account : Union[str, BTAccount]) -> int:
        account = self.get_account(account)
        if account:
            return self.accounts.index(account)
