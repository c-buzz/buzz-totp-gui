from genericpath import isfile
import os
import os.path
from BTErrorManager import *
from PyQt5.QtCore import QSettings, QStandardPaths

class BTSettings(QSettings):
    def __init__(self):
        filename = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.ConfigLocation)
        filename = os.path.join(filename, 'settings.ini')
        super().__init__(filename, QSettings.Format.IniFormat)

        # If no configuration found, write a default one
        if not os.path.exists(filename):
            self.reset_to_default(True)
        else:
            self.sync()
    
    def reset_to_default(self, persist = True):
        self.auto_hide_totp = True
        self.copy_to_clipboard = True
        self.last_profile = ''

    @property
    def auto_hide_totp(self) -> bool:
        return self.value('autoHideTotp', type=bool)

    @auto_hide_totp.setter
    def auto_hide_totp(self, auto_hide : bool = True):
        self.setValue('autoHideTotp',auto_hide)

    @property
    def copy_to_clipboard(self) -> bool:
        return self.value('autoHideTotp', type=bool)

    @auto_hide_totp.setter
    def copy_to_clipboard(self, copy : bool = True):
        self.setValue('copyToClipboard',copy)

    @property
    def last_profile(self) -> str:
        current = self.value('lastProfile', type=str)
        if current and not (os.path.exists(current) and os.path.isfile(current)):
            self.last_profile = ''
        return self.value('lastProfile', type=str)

    @last_profile.setter
    def last_profile(self, filename : str):
        filename = os.path.abspath(filename) if filename else ''
        self.setValue('lastProfile',filename)