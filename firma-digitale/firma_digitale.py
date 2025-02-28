#=====================================================================#
# Import libraries
import os
import termcolor
from hashlib import sha256
from rsa_python import rsa
import time
import sys
import json

# Define the folder for key and document files
key_folder = "firma-digitale"
os.makedirs(key_folder, exist_ok=True)

# File paths
pub_key_path = os.path.join(key_folder, "public_key.json")
priv_key_path = os.path.join(key_folder, "private_key.json")
document_path = os.path.join(key_folder, "document.txt")

#=====================================================================#
# Variable declaration
plain_text = str(input("Enter the text to sign: "))

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
# Check if key files exist

print("")
print(termcolor.colored("Verify keys, please wait", "magenta"), end="")
for _ in range(3):
    sys.stdout.write(".")
    sys.stdout.flush()
    time.sleep(1)
print("")

if os.path.exists(pub_key_path) and os.path.exists(priv_key_path):
    with open(pub_key_path, "r") as pub_file:
        pub_data = json.load(pub_file)
    with open(priv_key_path, "r") as priv_file:
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
    with open(pub_key_path, "w") as pub_file:
        json.dump({
            "public": key_pair["public"],
            "modulus": key_pair["modulus"]
        }, pub_file)

    # Save private key
    with open(priv_key_path, "w") as priv_file:
        json.dump({
            "private": key_pair["private"],
            "modulus": key_pair["modulus"]
        }, priv_file)
    print("")
    print(termcolor.colored("Keys generated and saved in files.", "yellow"))

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
# Document signature

print("")
print(termcolor.colored("Creating text file, please wait", "magenta"), end="")
for _ in range(3):
    sys.stdout.write(".")
    sys.stdout.flush()
    time.sleep(1)
print("")

with open(document_path, "w") as doc_file:
    doc_file.write(decrypted_message)

print("")
print(termcolor.colored("Document created and saved.", "green"))