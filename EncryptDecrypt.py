import bcrypt
import os
import argon2
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
    password += (8-padding)*" " #add padding to fit the 3DES OFB requiremets (multiple of 8)

    # generate all the required parts to encrypt the password   
    iv = Random.new().read(DES3.block_size)
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    encryptedPass = cipher.encrypt(password.encode())
    hasher = argon2.PasswordHasher(time_cost=16, memory_cost=2**16, parallelism=2, hash_len=32)
    hashPass = hasher.hash(password)

    # parts to store in the DB server
    outputDB.append(iv)
    outputDB.append(hashPass)
    outputDB.append(key)

    # parts to return
    outputFinal.append(encryptedPass)
    outputFinal.append(outputDB)
    return outputFinal

# function to decrypt the password
def decryptPass(encryptedPass, iv, hash, key):
    # decrypt the password
    cipher_decrypt = DES3.new(key, DES3.MODE_CBC, iv)
    dec = cipher_decrypt.decrypt(encryptedPass).decode("utf-8")
    
    #hash it again
    hasher = argon2.PasswordHasher(time_cost=16, memory_cost=2**16, parallelism=2, hash_len=32)

    # Verify if the hash just created and the old one(with the salt) are equivalent
    if hasher.verify(hash,dec):
        return dec
    else:
        print("You have been hacked :(")