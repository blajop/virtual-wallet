import base64
import os

key = os.urandom(32)
iv = os.urandom(16)

# print(base64.b64encode(key).decode())
# print(base64.b64encode(iv).decode())
