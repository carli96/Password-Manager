import bcrypt
from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
from Crypto import Random
from unicodedata import normalize

encryptedPass, hashPass, endMsg = "", "", ""

# function to encrypt the passwords


def encryptPass(password):
    outputFinal, outputDB = [], []  # E(password)   IV,Hash,Key
    while True:
        try:
            key = DES3.adjust_key_parity(get_random_bytes(16))
            break
        except ValueError:
            pass

    # DES3.MODE_OFB
    padding = len(password) % 8
    password += (8-padding)*" "

    iv = Random.new().read(DES3.block_size)
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    encryptedPass = cipher.encrypt(password.encode())
    hashPass = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    outputDB.append(iv)
    outputDB.append(hashPass)
    outputDB.append(key)

    outputFinal.append(encryptedPass)
    outputFinal.append(outputDB)
    return outputFinal

# function to decrypt the password


def decryptPass(endMsg, outputDB):
    iv, hash, key = outputDB[0], outputDB[1], outputDB[2]

    cipher_decrypt = DES3.new(key, DES3.MODE_CBC, iv)
    dec = cipher_decrypt.decrypt(endMsg)
    if bcrypt.hashpw(dec, bcrypt.gensalt()) == hash:
        return dec
    else:
        print("You have been hacked!!")
    print("Decrpted message: " + dec.decode())
    var = endMsg.partition(hash.decode())


if __name__ == '__main__':
    encryptPass("luisqqqqluisqqqqluisqqqqluisqqqqq")
