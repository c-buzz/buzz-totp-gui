from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from ui.BTNewAccount import Ui_FormNewAccount
from PyQt5.QtWidgets import QDialog
from BTErrorManager import bt_raise_error, bt_ask_for_confirm
from models.BTAccount import BTAccount
from BTUtils import digest_table

class NewAccountWindow(Ui_FormNewAccount, QDialog):
    def __init__(self):
        super(NewAccountWindow, self).__init__()
        self.setupUi(self)

        self.editAccountName.setValidator(QRegExpValidator(QRegExp('[A-Za-z0-9 ]{0,15}')))

        self.buttonSaveProfile.clicked.connect(self.on_click_save)
        self.account = None

    def on_click_save(self):
        account_name = self.editAccountName.text()
        if not account_name:
            bt_raise_error('Account name is empty')
            return

        if self.toolBox.currentIndex() == 0:
            # Parse by URI
            URI = self.editURI.text()
            try:
                self.account = BTAccount.fromURI(URI, account_name)
                self.accept()
            except:
                bt_raise_error("URI passed not valid")
        else:
            secret = self.editSecret.text()
            digest = digest_table[self.comboDigest.currentText()]
            digits = self.spinDigits.value()
            interval = self.spinInterval.value()
            try:
                account = BTAccount(account_name, secret, interval, digits, digest)
                self.account = account
                self.accept()
            except:
                bt_raise_error('Some parameter entered are not acceptable')

    def createNewAccount(self) -> BTAccount:
        if self.exec() == QDialog.DialogCode.Accepted:
            return self.account
        else:
            return None