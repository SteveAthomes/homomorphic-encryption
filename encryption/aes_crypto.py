<<<<<<< HEAD
import os
from cryptography.fernet import Fernet, InvalidToken

key = os.environ.get("2SUvw6wSdeczSC4Dsk70r03pLaUeBWklfyAs9C_TLJE=")

cipher = Fernet(key.encode())

def encrypt_text(text):
    return cipher.encrypt(text.encode()).decode()

def decrypt_text(enc_text):
    try:
        return cipher.decrypt(enc_text.encode()).decode()
    except InvalidToken:
=======
import os
from cryptography.fernet import Fernet, InvalidToken

key = os.environ.get("2SUvw6wSdeczSC4Dsk70r03pLaUeBWklfyAs9C_TLJE=")

cipher = Fernet(key.encode())

def encrypt_text(text):
    return cipher.encrypt(text.encode()).decode()

def decrypt_text(enc_text):
    try:
        return cipher.decrypt(enc_text.encode()).decode()
    except InvalidToken:
>>>>>>> a4f7494f5e69b82888191170890e42a645601681
        return enc_text