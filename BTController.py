from BTSettings import BTSettings
import os
from typing import Union
from BTSettings import BTSettings
from BTErrorManager import bt_raise_error
from BTProfile import BTProfileController
from views.InputPasswordView import BTInputPasswordView
from views.ProfileLoaderView import BTProfileLoaderView

class BTController(object):
    def __init__(self) -> None:
        self.settings = BTSettings()
        self.profile_loader = BTProfileLoaderView()
        self.password_handler = BTInputPasswordView()
        self.__currentProfile : BTProfileController = None

        # Notify the controller of the result of a new loading 
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
            # FIXME --> When closing profile after changes, the application does not quit
            self.profile_loader.close()
        else:
            if self.current_profile:
                self.current_profile.show()

    def load_last_profile(self) -> Union[bool, BTProfileController]:
        last_profile = self.settings.last_profile
        if os.path.exists(last_profile) and os.path.isfile(last_profile):
            # FIXME --> Adjust message indentation
            message = f'Last profile opened detected:\n\
                {last_profile}\n\
                Type the password for it to be opened or close whit window to choose another profile'
            self.password_handler.profile_check = last_profile
            password = self.password_handler.prompt(message)
            if password:
                return BTProfileController(last_profile, password)
        return False

    def onChangeProfile(self):
        # FIXME: If wrong password input, error arise. Manage the Exception
        self.profile_loader.show()
