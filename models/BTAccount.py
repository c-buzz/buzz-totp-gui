from ui.new_account import Ui_FormNewAccount
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp
import pyotp
from BTErrorManager import *
from datetime import datetime

class BTAccount(pyotp.TOTP):
    def __init__(self, name : str, secret = None, interval = None, digits = None, digest = None):
        super().__init__(secret, digits, digest, name, interval=interval)
        self._time_to_change = False
        self._is_totp_visible = False
        self._visible_counter = 0
        self.visibility_thread = None
        
    @property
    def time_to_change(self):
        return self.interval - (datetime.now().second % self.interval)

    @property
    def is_totp_visible(self) -> bool :
        return self._is_totp_visible

    @is_totp_visible.setter
    def is_totp_visible(self, visible:bool):
        self._is_totp_visible = visible

    def toggle_visibility(self):
        self.is_totp_visible = not self.is_totp_visible

    def validate_name(self, name:str) -> bool :
        """
            Valid name for alphanumeric characters and spaces only
        """
        return name.replace(' ','').isalnum()

    def validate_digits(self, digits: int) -> bool :
        return digits > 0 and digits <= 32

    def validate_interval(self, interval : int) -> bool :
        return interval > 0 and interval < 60

    def validate_hash(self, name) -> bool :
        """
            To be Done
        """
        return True

    def validate_secret(self, secret : str) -> bool :
        """
            To be done
        """
        return True

    def update(self, name: str = None, secret : str = None, interval : int = None, digits : int = None, _hash = None) -> bool:
        args = [name, secret, interval, digits, _hash]
        methods = [self.validate_name, self.validate_secret, self.validate_interval, self.validate_digits, self.validate_hash]
        l = list(zip(args, methods))

        # Iterting only among non None arguments
        for (arg,method) in [e for e in l if e[0] is not None]:
            if not method(arg):
                return False
            
        if name is not None and self.validate_name(name.strip()):
            self.name = name.strip()
        
        if interval is not None and self.validate_interval(interval):
            self.interval = interval

        if digits is not None and self.validate_digits(digits):
            self.digits = digits

        if _hash is not None and self.validate_hash(_hash):
            self.digest = _hash

        if secret is not None and self.validate_secret(secret):
            self.secret = secret
        
        return True

    def fromURI(URI : str, name : str = None):
        totp = pyotp.parse_uri(URI)
        if name is None:
            name = totp.name
        return BTAccount(name, totp.secret, totp.interval, totp.digits, totp.digest)


