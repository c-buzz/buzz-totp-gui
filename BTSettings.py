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
        v = self.value('lastProfile', type=str)
        return self.value('lastProfile', type=str)

    @last_profile.setter
    def last_profile(self, filename : str):
        filename = os.path.abspath(filename) if filename else ''
        self.setValue('lastProfile',filename)




    # @property
    # def user_data_dir(self):
    #     return self.__user_data_dir
    
    # @user_data_dir.setter
    # def user_data_dir(self, user_data_dir : str = ''):
    #     user_data_dir = os.path.abspath(user_data_dir)
    #     if not user_data_dir:
    #         # If no user_data_dir passed, default dir given by appdirs lib
    #         self.user_data_dir = appdirs.user_data_dir(self.app_name, self.app_author)
        
    #     # Check if already exists, otherwise create it
    #     if not(os.path.exists(user_data_dir) and os.path.isdir(user_data_dir)):
    #         try:
    #             os.mkdir(os.path.abspath(user_data_dir))
    #         except:
    #             bt_raise_error(f'Cannot create user data dir at {user_data_dir}')

    #         # Check for writing permission
    #         if not os.access(user_data_dir, os.W_OK):
    #             bt_raise_error(f'No permission for writing in directory {user_data_dir}')
    #             return
        
    #     self.__user_data_dir = user_data_dir
            

    # @property
    # def config_dir(self):
    #     return self.__config_dir

    # @config_dir.setter
    # def config_dir(self, config_dir : str = ''):
    #     self.__config_dir = appdirs.user_config_dir(self.app_name, self.app_author) if not config_dir else config_dir

    # def save_config(self, content : BTConfiguration):
    #     if not os.path.exists(self.config_dir):
    #         os.mkdir(self.config_dir)
    #     # Fullname of config file
    #     cfn = os.path.join(self.config_dir, self.config_filename)
    #     with open(cfn, 'w') as configfile:
    #         content.write(configfile)

    # def load_config(self):
    #     config_fullname = os.path.join(self.config_dir, self.config_filename)
    #     if not os.path.exists(config_fullname):
    #         # No configuration was found. New Setup is launched
            
    #         return None
    #     else:
    #         #config = ConfigParser()
    #         config.read(cfn)

    # def load_default_profile(self):
    #     config = self.load_config()
    #     config.has_option()
    #     default_profile = config.get(option='defaultProfile')

    # def save_user_data(self, filename, content : Union[str, bytearray]):
    #     try:
    #         filename = os.path.abspath(filename)
    #         f = open(filename, 'w')
    #         f.write(content)
    #     except:
    #         e = sys.exc_info()[0]
    #         bt_raise_error("Exception writing user data to {filename} : {e}")
    #         return False
    #     else:
    #         return True
        
    # def onCreate(self) -> Tuple[str, str, str]:
    #     filename, profile_name, password = super().onCreate()

    #     if not profile_name:
    #         bt_raise_error("Profile name is empty")
    #         return
        
    #     if not utils.validate_password(password):
    #         # ToDo: Display requirements
    #         bt_raise_error("Password not valid")
    #         return
        
    #     #Check writebility 
    #     try:
    #         path = os.path.abspath(filename)
    #         f = open(path, 'w')
    #         f.close()
    #         os.remove(path) # Delete it because it is later encoded by the BTProfile
    #     except:
    #        e = sys.exc_info()[0]
    #        bt_raise_error("Exception writing the profile file: " + e)
    #        return

    # def onLoadProfile(self):
    #     filename, password = super().onLoadProfile()
    #     if not(os.path.exists(filename) and os.path.isfile(filename)):
    #         bt_raise_error('File not found')
    #     elif not utils.validate_password(password):
    #         bt_raise_error('Password not valid')
    #     self.profileLoadingRequested.emit(filename, password)
        
    # def onProfileLoaded(self, success: bool):
    #     if success:
    #         self.close()


# app = QApplication(sys.argv)
# c = BTConfigManager('BuzzTotp','buzz')
# c.launch_ui()
# sys.exit(app.exec_())