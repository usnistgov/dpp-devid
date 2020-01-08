import binascii
keyname = "IDevID50.pubkey.der"
#keyname = "ecpubkey.der"
with open(keyname, mode="rb") as file:
    fileContent = file.read()

hex_str = binascii.b2a_hex(fileContent)
print(hex_str)
import base64
print(base64.b64encode(fileContent))

