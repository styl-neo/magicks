import json
import base64

from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Padding import pad, unpad

def doEncrypt(payload, password):
    # Key derivation
    pw = bytes(password, 'UTF-8')
    hash = SHA256.new()
    hash.update(pw)
    hashed = hash.digest()
    # Encryption
    cipher = AES.new(hashed[:16], AES.MODE_CBC, hashed[16:])
    data = cipher.encrypt(pad(payload, AES.block_size, 'pkcs7'))
    return data

def doDecrypt(payload, password):
    # Key derivation
    pw = bytes(password, 'UTF-8')
    hash = SHA256.new()
    hash.update(pw)
    hashed = hash.digest()
     # Decryption
    cipher = AES.new(hashed[:16], AES.MODE_CBC, hashed[16:])
    data = cipher.decrypt(payload)
    return unpad(data, AES.block_size, 'pkcs7')


def encryptObject(obj, pw):
	jobj = json.dumps(obj)
	encData = doEncrypt(bytes(jobj, 'UTF-8'), pw)
	return base64.b64encode(encData)

def decryptObject(b64data, pw):
	encData = base64.b64decode(b64data)
	ptData = doDecrypt(encData, pw)
	return json.loads(ptData)