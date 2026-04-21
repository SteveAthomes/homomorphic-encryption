<<<<<<< HEAD
from phe import paillier
import os
import pickle

KEY_FILE = "paillier_keys.pkl"

# Load or create keys
if os.path.exists(KEY_FILE):
    with open(KEY_FILE, "rb") as f:
        public_key, private_key = pickle.load(f)
else:
    public_key, private_key = paillier.generate_paillier_keypair()
    with open(KEY_FILE, "wb") as f:
        pickle.dump((public_key, private_key), f)


def encrypt_number(value):
    return public_key.encrypt(value)


def decrypt_number(encrypted_number):
    return private_key.decrypt(encrypted_number)


def get_keys():
=======
from phe import paillier
import os
import pickle

KEY_FILE = "paillier_keys.pkl"

# Load or create keys
if os.path.exists(KEY_FILE):
    with open(KEY_FILE, "rb") as f:
        public_key, private_key = pickle.load(f)
else:
    public_key, private_key = paillier.generate_paillier_keypair()
    with open(KEY_FILE, "wb") as f:
        pickle.dump((public_key, private_key), f)


def encrypt_number(value):
    return public_key.encrypt(value)


def decrypt_number(encrypted_number):
    return private_key.decrypt(encrypted_number)


def get_keys():
>>>>>>> a4f7494f5e69b82888191170890e42a645601681
    return public_key, private_key