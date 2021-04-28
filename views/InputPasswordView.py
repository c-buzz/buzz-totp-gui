#from BTProfile import BTProfileController
from typing import Union
from ui.BTDialogInputPassword import Ui_PasswordInputDialog
from BTErrorManager import bt_raise_error
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QDialog, QLineEdit
import BTUtils as utils

class BTInputPasswordView(Ui_PasswordInputDialog, QDialog):
    def __init__(self, message : str = '', profile_check : str = None) -> None:
        super().__init__()
        self.setupUi(self)
        self.__password = ''
        
        self.buttonShowHidePassword.clicked.connect(self.show_hide_password)
        if message:
            self.labelMessage.setText(message)
        else:
            self.labelMessage.hide()
        
        self.profile_check = None if (profile_check is None or profile_check == '') else profile_check
        self.icon_visible_password = QIcon(QPixmap('ui/icon/pwd_show.png'))
        self.icon_hidden_password = QIcon(QPixmap('ui/icon/pwd_hide.png'))
        self.show_hide_password('hide')

    def show_hide_password(self, force):
        if force == 'hide':
            show = False
        elif force == 'show':
            show = True
        else:
            show = self.editPassword.echoMode() == QLineEdit.EchoMode.Password
        if show:
            self.editPassword.setEchoMode(QLineEdit.EchoMode.Normal)
            self.buttonShowHidePassword.setIcon(self.icon_hidden_password)
        else:
            self.buttonShowHidePassword.setIcon(self.icon_visible_password)
            self.editPassword.setEchoMode(QLineEdit.EchoMode.Password)

    def accept(self) -> None:
        pwd = self.editPassword.text()
        valid = True
        if not utils.validate_password(pwd):
            valid = False
        elif self.profile_check is not None:
            valid = utils.checkPassword(self.profile_check, pwd)
        if valid:
            self.__password = pwd
            super().accept()
        else:
            bt_raise_error('Password not valid')

    def prompt(self, message : str = '') -> str:
        if message:
            self.labelMessage.setText(message)
            self.labelMessage.show()
        if self.exec() == QDialog.DialogCode.Accepted:
            return self.__password
        else:
            return None

