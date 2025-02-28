#=====================================================================#
# Import libraries
import os
import termcolor
from hashlib import sha256
from rsa_python import rsa
import time
import sys
import json

#=====================================================================#

#=====================================================================#
# Variable declaration
plain_text = str(input("Enter a text: "))

print(termcolor.colored("#=====================================================================#", "cyan"))
print(termcolor.colored("Plain text:", "cyan"))
print("")
print(termcolor.colored(plain_text, "green"))
print("")
print(termcolor.colored("#=====================================================================#", "cyan"))

hash_value = sha256(plain_text.encode()).hexdigest()

print("")
print(termcolor.colored("#=====================================================================#", "cyan"))
print(termcolor.colored("Hash text:", "cyan"))
print("")
print(termcolor.colored(hash_value, "red"))
print("")
print(termcolor.colored("#=====================================================================#", "cyan"))

#=====================================================================#

#=====================================================================#
# Check if key files exist

print("")

print(termcolor.colored("Verify keys, please wait", "magenta"), end="")
for _ in range(3):
    sys.stdout.write(".")
    sys.stdout.flush()
    time.sleep(1)
print("")

if os.path.exists("public_key.json") and os.path.exists("private_key.json"):
    with open("public_key.json", "r") as pub_file:
        pub_data = json.load(pub_file)
    with open("private_key.json", "r") as priv_file:
        priv_data = json.load(priv_file)
    key_pair = {
        "public": pub_data["public"],
        "private": priv_data["private"],
        "modulus": pub_data["modulus"]
    }
    print("")
    print(termcolor.colored("Keys found and loaded from files.", "green"))
else:
    # Generate keys if they do not exist
    key_pair = rsa.generate_key_pair(1024)

    # Save public key
    with open("public_key.json", "w") as pub_file:
        json.dump({
            "public": key_pair["public"],
            "modulus": key_pair["modulus"]
        }, pub_file)

    # Save private key
    with open("private_key.json", "w") as priv_file:
        json.dump({
            "private": key_pair["private"],
            "modulus": key_pair["modulus"]
        }, priv_file)
    print(termcolor.colored("Keys generated and saved in files.", "yellow"))

#=====================================================================#

#=====================================================================#
# Encrypt and decrypt message
cipher = rsa.encrypt(hash_value, key_pair["private"], key_pair["modulus"])
decrypted_message = rsa.decrypt(cipher, key_pair["public"], key_pair["modulus"])

print("")

print(termcolor.colored("Decrypting message, please wait", "magenta"), end="")
for _ in range(5):
    sys.stdout.write(".")
    sys.stdout.flush()
    time.sleep(1)
print("")

print("")
print(termcolor.colored("#=====================================================================#", "cyan"))
print("")
print(termcolor.colored(decrypted_message, "yellow"))
print("")
print(termcolor.colored("#=====================================================================#", "cyan"))

#=====================================================================#