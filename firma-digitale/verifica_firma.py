import hashlib  
import rsa  
import json
import os
import termcolor
import sys

# Increase the limit for integer string conversion
sys.set_int_max_str_digits(100000)  # Set limit to 100,000 digits

def get_absolute_path(filename):
    # Ottiene il percorso della directory corrente dello script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, filename)

def main():
    # Carica la chiave pubblica dal file
    with open(get_absolute_path('public_key.txt'), 'r') as f:
        pub_e, pub_n = f.read().strip().split('\n')
        public_e = int(pub_e)
        public_n = int(pub_n)

    # Carica la firma digitale dal file
    with open(get_absolute_path('document.txt'), 'r') as f:
        signature = f.read().strip()  # Remove any whitespace

    # Carica la stringa originale dal file
    with open(get_absolute_path('text.txt'), 'r') as f:
        input_string = f.read()
    
    encoded_string = input_string.encode('utf-8')
    input_hash = hashlib.sha256(encoded_string).hexdigest()

    print("\nDEBUG INFO:")
    print(termcolor.colored("1. Signature verification:", "cyan"))
    print(f"Signature from file: {signature}")
    
    print(termcolor.colored("\n2. Hash details:", "cyan"))
    print(f"Original text: {input_string}")
    print(f"Calculated hash: {input_hash}")
    
    try:
        # Convert signature to integer
        signature_int = int(signature)
        
        # Decrypt signature using public key values directly
        decrypted_sig = rsa.decrypt(signature_int, public_e, public_n)
        decrypted_sig_str = str(decrypted_sig)
        
        # Convert decrypted signature back to hex format
        try:
            decrypted_hex = format(int(decrypted_sig_str), 'x')
        except ValueError:
            # If direct conversion fails, try cleaning the string
            clean_sig = ''.join(c for c in decrypted_sig_str if c.isdigit())
            decrypted_hex = format(int(clean_sig), 'x')
            
        # Ensure the hex string has the correct length (64 characters for SHA256)
        decrypted_hex = decrypted_hex.zfill(64)
        
        print(termcolor.colored("\n3. Decryption result:", "cyan"))
        print(f"Decrypted signature (hex): {decrypted_hex}")
        print(f"Original hash          : {input_hash}")
        
        # Compare the decrypted signature with the original hash
        if decrypted_hex == input_hash:
            print(termcolor.colored("\nLa firma è valida! Il messaggio è autentico.", "green"))
        else:
            print(termcolor.colored("\nLa firma non è valida! Il messaggio potrebbe essere stato alterato.", "red"))
            
    except Exception as e:
        print(termcolor.colored(f"\nErrore nella verifica: {e}", "red"))
        print(termcolor.colored("Stack trace:", "red"))
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
