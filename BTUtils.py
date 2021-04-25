# AES 256 encryption/decryption using pycryptodome library
import json
from typing import List, Union

import pyotp
from models.BTAccount import BTAccount
import os
import hashlib
from base64 import b64encode, b64decode
from password_validator import PasswordValidator

from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes

from PyQt5.QtCore import QMimeData, QUrl
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
                
        