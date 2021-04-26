# AES 256 encryption/decryption using pycryptodome library
import json
from typing import List, Union

import pyotp
from models.BTAccount import BTAccount
import hashlib
from base64 import b64encode, b64decode
from password_validator import PasswordValidator

from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes


from PyQt5.QtCore import QMimeData, QUrl
from PyQt5.QtCore import QEvent
import imghdr

def encrypt(plain_text, password):
    # generate a random salt
    salt = get_random_bytes(AES.block_size)

    # use the Scrypt KDF to get a private key from the password
    private_key = hashlib.scrypt(
        password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)

    # create cipher config
    cipher_config = AES.new(private_key, AES.MODE_GCM)

    # return a dictionary with the encrypted text
    cipher_text, tag = cipher_config.encrypt_and_digest(bytes(plain_text, 'utf-8'))
    return {
        'cipher_text': b64encode(cipher_text).decode('utf-8'),
        'salt': b64encode(salt).decode('utf-8'),
        'nonce': b64encode(cipher_config.nonce).decode('utf-8'),
        'tag': b64encode(tag).decode('utf-8')
    }

def decrypt(enc_dict, password):
    # decode the dictionary entries from base64
    salt = b64decode(enc_dict['salt'])
    cipher_text = b64decode(enc_dict['cipher_text'])
    nonce = b64decode(enc_dict['nonce'])
    tag = b64decode(enc_dict['tag'])
    

    # generate the private key from the password and salt
    private_key = hashlib.scrypt(
        password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)

    # create the cipher config
    cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)

    # decrypt the cipher text
    decrypted = cipher.decrypt_and_verify(cipher_text, tag)

    return decrypted

def encrypt_file(filename, content, password):
    crypted_content = json.dumps(encrypt(content, password))
    f = open(filename, 'w')
    f.write(crypted_content)
    f.close()

def decrypt_file(filename, password):
    f = open(filename, 'r')
    crypted_content = json.loads(f.read())
    f.close()
    return decrypt(crypted_content, password)

def is_valid_image_file(url:QUrl):
    filename = url.toLocalFile()
    if imghdr.what(filename) is not None:
        return True

def mime_data_valid(mime_data:QMimeData):
    #It accepts only URLS data referring to image files or otpauth url
    if mime_data.hasUrls():
        for url in mime_data.urls():
            if url.isLocalFile():
                return is_valid_image_file(url)
            elif url.scheme() == 'otpauth':
                return True
    elif mime_data.hasText():
        url = QUrl(mime_data.text())
        if url.isValid() and url.scheme() == 'otpauth':
            return True

def get_account_from_image(filename:Union[QUrl, str]):
    #TODO: To be implemented
    return None

def get_account_from_mime_data(mime:QMimeData) -> List[BTAccount]:
    if not mime_data_valid(mime):
        return False
    
    accounts = []
    if mime.hasUrls():
        urls = mime.urls()
    elif mime.hasText():
        urls = [QUrl(mime.text().strip())]

    for url in urls:
        if url.isLocalFile():
            return get_account_from_image(url.toLocalFile())
        elif url.scheme() == 'otpauth':
            try:
                account = BTAccount.fromURI(url.toString())
                n = account.now()
                accounts.append(account)
            except:
                pass
    return accounts

def validate_password(password : str):
    bt_password_validator = PasswordValidator()
    bt_password_validator\
                    .min(6)\
                    .max(100)\
                    .has().lowercase()\
                    .has().digits()\
                    .has().no().spaces()\
                    #.has().symbols()
                    #.has().uppercase()\
    return bt_password_validator.validate(password)

digest_table = {
    "SHA-1" : hashlib.sha1,
    "SHA-256": hashlib.sha256,
    "SHA-512": hashlib.sha512,
    "MD5" : hashlib.md5
}
                

lookup_table = {"0": "QEvent::None",
                "114": "QEvent::ActionAdded",
                "113": "QEvent::ActionChanged",
                "115": "QEvent::ActionRemoved",
                "99": "QEvent::ActivationChange",
                "121": "QEvent::ApplicationActivate",
                "122": "QEvent::ApplicationDeactivate",
                "36": "QEvent::ApplicationFontChange",
                "37": "QEvent::ApplicationLayoutDirectionChange",
                "38": "QEvent::ApplicationPaletteChange",
                "214": "QEvent::ApplicationStateChange",
                "35": "QEvent::ApplicationWindowIconChange",
                "68": "QEvent::ChildAdded",
                "69": "QEvent::ChildPolished",
                "71": "QEvent::ChildRemoved",
                "40": "QEvent::Clipboard",
                "19": "QEvent::Close",
                "200": "QEvent::CloseSoftwareInputPanel",
                "178": "QEvent::ContentsRectChange",
                "82": "QEvent::ContextMenu",
                "183": "QEvent::CursorChange",
                "52": "QEvent::DeferredDelete",
                "60": "QEvent::DragEnter",
                "62": "QEvent::DragLeave",
                "61": "QEvent::DragMove",
                "63": "QEvent::Drop",
                "170": "QEvent::DynamicPropertyChange",
                "98": "QEvent::EnabledChange",
                "10": "QEvent::Enter",
                "150": "QEvent::EnterEditFocus",
                "124": "QEvent::EnterWhatsThisMode",
                "206": "QEvent::Expose",
                "116": "QEvent::FileOpen",
                "8": "QEvent::FocusIn",
                "9": "QEvent::FocusOut",
                "23": "QEvent::FocusAboutToChange",
                "97": "QEvent::FontChange",
                "198": "QEvent::Gesture",
                "202": "QEvent::GestureOverride",
                "188": "QEvent::GrabKeyboard",
                "186": "QEvent::GrabMouse",
                "159": "QEvent::GraphicsSceneContextMenu",
                "164": "QEvent::GraphicsSceneDragEnter",
                "166": "QEvent::GraphicsSceneDragLeave",
                "165": "QEvent::GraphicsSceneDragMove",
                "167": "QEvent::GraphicsSceneDrop",
                "163": "QEvent::GraphicsSceneHelp",
                "160": "QEvent::GraphicsSceneHoverEnter",
                "162": "QEvent::GraphicsSceneHoverLeave",
                "161": "QEvent::GraphicsSceneHoverMove",
                "158": "QEvent::GraphicsSceneMouseDoubleClick",
                "155": "QEvent::GraphicsSceneMouseMove",
                "156": "QEvent::GraphicsSceneMousePress",
                "157": "QEvent::GraphicsSceneMouseRelease",
                "182": "QEvent::GraphicsSceneMove",
                "181": "QEvent::GraphicsSceneResize",
                "168": "QEvent::GraphicsSceneWheel",
                "18": "QEvent::Hide",
                "27": "QEvent::HideToParent",
                "127": "QEvent::HoverEnter",
                "128": "QEvent::HoverLeave",
                "129": "QEvent::HoverMove",
                "96": "QEvent::IconDrag",
                "101": "QEvent::IconTextChange",
                "83": "QEvent::InputMethod",
                "207": "QEvent::InputMethodQuery",
                "169": "QEvent::KeyboardLayoutChange",
                "6": "QEvent::KeyPress",
                "7": "QEvent::KeyRelease",
                "89": "QEvent::LanguageChange",
                "90": "QEvent::LayoutDirectionChange",
                "76": "QEvent::LayoutRequest",
                "11": "QEvent::Leave",
                "151": "QEvent::LeaveEditFocus",
                "125": "QEvent::LeaveWhatsThisMode",
                "88": "QEvent::LocaleChange",
                "176": "QEvent::NonClientAreaMouseButtonDblClick",
                "174": "QEvent::NonClientAreaMouseButtonPress",
                "175": "QEvent::NonClientAreaMouseButtonRelease",
                "173": "QEvent::NonClientAreaMouseMove",
                "177": "QEvent::MacSizeChange",
                "43": "QEvent::MetaCall",
                "102": "QEvent::ModifiedChange",
                "4": "QEvent::MouseButtonDblClick",
                "2": "QEvent::MouseButtonPress",
                "3": "QEvent::MouseButtonRelease",
                "5": "QEvent::MouseMove",
                "109": "QEvent::MouseTrackingChange",
                "13": "QEvent::Move",
                "197": "QEvent::NativeGesture",
                "208": "QEvent::OrientationChange",
                "12": "QEvent::Paint",
                "39": "QEvent::PaletteChange",
                "131": "QEvent::ParentAboutToChange",
                "21": "QEvent::ParentChange",
                "212": "QEvent::PlatformPanel",
                "217": "QEvent::PlatformSurface",
                "75": "QEvent::Polish",
                "74": "QEvent::PolishRequest",
                "123": "QEvent::QueryWhatsThis",
                "106": "QEvent::ReadOnlyChange",
                "199": "QEvent::RequestSoftwareInputPanel",
                "14": "QEvent::Resize",
                "204": "QEvent::ScrollPrepare",
                "205": "QEvent::Scroll",
                "117": "QEvent::Shortcut",
                "51": "QEvent::ShortcutOverride",
                "17": "QEvent::Show",
                "26": "QEvent::ShowToParent",
                "50": "QEvent::SockAct",
                "192": "QEvent::StateMachineSignal",
                "193": "QEvent::StateMachineWrapped",
                "112": "QEvent::StatusTip",
                "100": "QEvent::StyleChange",
                "87": "QEvent::TabletMove",
                "92": "QEvent::TabletPress",
                "93": "QEvent::TabletRelease",
                "171": "QEvent::TabletEnterProximity",
                "172": "QEvent::TabletLeaveProximity",
                "219": "QEvent::TabletTrackingChange",
                "22": "QEvent::ThreadChange",
                "1": "QEvent::Timer",
                "120": "QEvent::ToolBarChange",
                "110": "QEvent::ToolTip",
                "184": "QEvent::ToolTipChange",
                "194": "QEvent::TouchBegin",
                "209": "QEvent::TouchCancel",
                "196": "QEvent::TouchEnd",
                "195": "QEvent::TouchUpdate",
                "189": "QEvent::UngrabKeyboard",
                "187": "QEvent::UngrabMouse",
                "78": "QEvent::UpdateLater",
                "77": "QEvent::UpdateRequest",
                "111": "QEvent::WhatsThis",
                "118": "QEvent::WhatsThisClicked",
                "31": "QEvent::Wheel",
                "132": "QEvent::WinEventAct",
                "24": "QEvent::WindowActivate",
                "103": "QEvent::WindowBlocked",
                "25": "QEvent::WindowDeactivate",
                "34": "QEvent::WindowIconChange",
                "105": "QEvent::WindowStateChange",
                "33": "QEvent::WindowTitleChange",
                "104": "QEvent::WindowUnblocked",
                "203": "QEvent::WinIdChange",
                "126": "QEvent::ZOrderChange", }

def QEventLookup(event:QEvent):
    return lookup_table[str(event.type())]