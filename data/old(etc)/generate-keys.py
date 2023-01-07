from cryptography.fernet import Fernet
import hashlib
from info import *
import base64
import json

if os.path.exists(f'.{subDirectory}settings.json'):
    key = base64.urlsafe_b64encode(hashlib.md5(b"Will Hellinger").hexdigest().encode())
    f = Fernet(key)

    encrypted = False
    with open('keys.key', 'rb') as file:
        original = file.read()
        if original.decode('utf-8')[0] != '{':
            decrypted = f.decrypt(original)
        else:
            decrypted = original
            encrypted = f.encrypt(original)

    if encrypted != False:
        with open('keys.key', 'wb') as file:
            file.write(encrypted)

unlock_noun_adj = json.loads(decrypted)['unlock_noun-adj']
print(unlock_noun_adj)