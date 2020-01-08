import binascii
with open("IDevID50.key.der", mode="rb") as file:
    fileContent = file.read()

hex_str = binascii.b2a_hex(fileContent)
print(hex_str)

