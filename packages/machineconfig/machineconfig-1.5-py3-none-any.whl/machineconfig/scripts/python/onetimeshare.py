
# as per https://github.com/Luzifer/ots
# this script is pure python and connects to server to create a secret
# or use ots executable to do this job


import requests
import crocodile.file_management as fm


from Crypto.Cipher import AES
from Crypto.Hash import MD5
import base64

def encrypt(key, pwd):
    pwd = pwd.encode("utf-8")
    hash_object = MD5.new(key.encode("utf-8"))
    key = hash_object.digest()
    iv = b'\x00' * 16
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pad = 16 - (len(pwd) % 16)
    pwd += bytes([pad] * pad)
    encrypted_password = cipher.encrypt(pwd)
    return base64.b64encode(encrypted_password).decode("utf-8")


secret = input("Secret: ")
password = input("Password: ") or None


if password is not None: encoded_secret = encrypt(password, secret)
else: encoded_secret = secret


url = "https://ots.fyi/api/create"

payload = {"secret": encoded_secret}
headers = {'Content-Type': 'application/json'}

response = requests.post(url, json=payload, headers=headers)

if response.status_code == 201:
    res = response.json()
    print(res)
    assert res["success"] is True, "Request have failed"
    share_url = fm.P(f"https://ots.fyi/#{res['secret_id']}") + (f"|{password}" if password is not None else "")
    print(repr(share_url))
else:
    print("Request failed")
    raise RuntimeError(response.text)

