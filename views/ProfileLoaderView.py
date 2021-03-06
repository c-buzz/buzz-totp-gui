import os
from BTErrorManager import bt_raise_error
from BTProfile import BTProfileController
from PyQt5.QtCore import QStandardPaths, Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QDialogButtonBox, QFileDialog

from views.InputPasswordView import BTInputPasswordView

class BTProfileLoaderView(QDialogButtonBox):
    signalLoadProfileResult = pyqtSignal(BTProfileController)
    def __init__(self) -> None:
        super().__init__()
        load_button = self.addButton("Load Existing Profile", QDialogButtonBox.ButtonRole.ApplyRole)
        load_button.clicked.connect(self.loadProfileRequest)
        create_button = self.addButton("Create New Profile", QDialogButtonBox.ButtonRole.ApplyRole)
        create_button.clicked.connect(self.createProfileRequest)
        self.setFixedSize(300, 50)
        self.setWindowTitle('BuzzTOTP')
        self.setOrientation(Qt.Orientation.Vertical)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

    def loadProfileRequest(self):
        docsdir = QStandardPaths.standardLocations(QStandardPaths.StandardLocation.DocumentsLocation)[0]
        filename = QFileDialog.getOpenFileName(self, "Select BuzzTOTP Profile", docsdir, "*.bt")[0]
        if filename:
            password_handler = BTInputPasswordView()
            password = password_handler.prompt('Type the password for the selected account')
            if password:
                profile = None
                try:
                    profile = BTProfileController(filename, password)
                except FileNotFoundError as e:
                    bt_raise_error(e.strerror())
                except:
                    bt_raise_error('Credentials are not valid or profile file corrupted')
                finally:
                    self.signalLoadProfileResult.emit(profile)
    
    def createProfileRequest(self):
        docsdir = QStandardPaths.standardLocations(QStandardPaths.StandardLocation.DocumentsLocation)[0]
        filename = QFileDialog.getSaveFileName(self, "Create a new BuzzTOTP Profile", docsdir, "*.bt")[0]
        if filename:
            profile = None
            try:
                # Check the file is writable in passed directory
                f = open(os.path.abspath(filename), 'w')
                f.close()
                os.remove(filename) # The file will be generated by the profile manager
                password = BTInputPasswordView().prompt('Please, choose a password for your new profile file')
                profile = BTProfileController(filename, password)
            except:
                bt_raise_error('Error while create the new BuzzTOTP profile file.\nThe directory might not exist or it is not accessible')
            finally:
                self.signalLoadProfileResult.emit(profile)