#!/usr/bin/env python3
import base64
import hashlib

user_id = input("User id: ")
passphrase = input("Passphrase: ").encode('utf-8')
user_bytes = int(user_id).to_bytes(8, "big")

key = b"".join([user_bytes, passphrase])
key_hash = hashlib.sha224(key).digest()

b64 = base64.standard_b64encode(key_hash)
print(b64.decode('utf-8'))
