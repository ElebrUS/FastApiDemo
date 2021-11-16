import binascii
import hashlib
import os


def hash_password(password: str) -> str:
    """Зашифровать полученный пароль"""
    salt = hashlib.sha256(os.urandom(30)).hexdigest().encode('ascii')
    pwd_hash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                   salt, 1000)
    pwd_hash = binascii.hexlify(pwd_hash)
    return (salt + pwd_hash).decode('ascii')


async def verify_password(stored_password: str, provided_password: str) -> bool:
    """Проверить полученный пароль с зашифрованным
        :param stored_password - зашифрованный пароль
        :param provided_password - полученный не зашифрованный пароль
    """
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwd_hash = hashlib.pbkdf2_hmac('sha512',
                                   provided_password.encode('utf-8'),
                                   salt.encode('ascii'),
                                   1000)
    pwd_hash = binascii.hexlify(pwd_hash).decode('ascii')
    return pwd_hash == stored_password


class CustomFail(Exception):
    def __init__(self, m):
        self.message = m

    def __str__(self):
        return self.message
