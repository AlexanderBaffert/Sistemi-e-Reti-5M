#=====================================================================#
# Importazione delle librerie
import termcolor
from hashlib import sha256
from rsa_python import rsa
import time
import sys


#=====================================================================#

#=====================================================================#
# Dichiarazione delle variabili
testo_in_chiaro = str(input("Inserisci il testo da firmare: "))

print(termcolor.colored("#=====================================================================#", "cyan"))
print(termcolor.colored("Testo in chiaro:", "cyan"))
print("")
print(termcolor.colored(testo_in_chiaro, "green"))
print("")
print(termcolor.colored("#=====================================================================#", "cyan"))

hash = sha256(testo_in_chiaro.encode()).hexdigest()

print("")
print(termcolor.colored("#=====================================================================#", "cyan"))
print(termcolor.colored("Testo in hash:", "cyan"))
print("")
print(termcolor.colored(hash, "red"))
print("")
print(termcolor.colored("#=====================================================================#", "cyan"))

#=====================================================================#

#=====================================================================#
# Generazione delle chiavi
key_pair = rsa.generate_key_pair(1024)

cipher = rsa.encrypt(testo_in_chiaro, key_pair["public"], key_pair["modulus"])
decrypted_message = rsa.decrypt(cipher, key_pair["private"], key_pair["modulus"])

print("")

print(termcolor.colored("Decrypting message, please wait", "magenta"), end="")
for _ in range(5):
    sys.stdout.write(".")
    sys.stdout.flush()
    time.sleep(1)
print("")

print("")
print(termcolor.colored("#=====================================================================#", "cyan"))
print(termcolor.colored(decrypted_message, "yellow"))
print("")
print(termcolor.colored("#=====================================================================#", "cyan"))

#=====================================================================#