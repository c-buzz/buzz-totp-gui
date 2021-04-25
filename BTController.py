from BTSettings import BTSettings
import os
import sys
from typing import Union, final

import pyotp
from PyQt5 import QtCore
from PyQt5.QtCore import QSettings, QStandardPaths, Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QDialogButtonBox, QFileDialog

import BTUtils as utils
from BTSettings import BTSettings
from BTErrorManager import bt_raise_error
from BTProfile import BTProfileController
from views.InputPasswordView import BTInputPasswordView
from views.ProfileLoaderView import BTProfileLoaderView

app = QApplication(sys.argv)

app.setApplicationName('BuzzTOTP')
app.setApplicationVersion('0.0.1')
QSettings.setDefaultFormat(QSettings.Format.IniFormat)

class BTController(object):
    profile_loader = BTProfileLoaderView()
    password_handler = BTInputPasswordView()
    __currentProfile : BTProfileController = None
    settings = BTSettings()
    def __init__(self) -> None:
        self.profile_loader.signalLoadProfileResult.connect(self.onProfileLoaded)
        lp = self.load_last_profile()
        if lp:
            self.current_profile = lp
        else:
            self.profile_loader.show()

    @property
    def current_profile(self):
        return self.__currentProfile if self.__currentProfile else None

    @current_profile.setter
    def current_profile(self, profile : BTProfileController):
        if self.__currentProfile:
            self.__currentProfile.destroy()
            self.__currentProfile = None

        self.__currentProfile = profile
        self.__currentProfile.actionChangeProfile.triggered.connect(self.onChangeProfile)
        self.__currentProfile.show()

    def onProfileLoaded(self, profile_ctr : BTProfileController):
        if profile_ctr:
            self.current_profile = profile_ctr
            self.profile_loader.close()
        else:
            if self.current_profile:
                self.current_profile.show()

    def load_last_profile(self) -> Union[bool, BTProfileController]:
        last_profile = self.settings.last_profile
        if os.path.exists(last_profile) and os.path.isfile(last_profile):
            message = f'Last profile opened detected:\n\
                {last_profile}\n\
                Type the password for it to be opened or close whit window to choose another profile'
            self.password_handler.profile_check = last_profile
            password = self.password_handler.input(message)
            if password:
                return BTProfileController(last_profile, password)
        return False

    def onChangeProfile(self):
        self.profile_loader.show()
