import base64
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# Function to generate a random 256-bit key and a 128-bit IV
def generate_key_iv():
    key = get_random_bytes(32)  # AES-256 key
    iv = get_random_bytes(16)   # AES block size for CBC mode
    return key, iv

# Function to encrypt data using AES in CBC mode
def encrypt_data(data, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = pad(data.encode(), AES.block_size)
    encrypted = cipher.encrypt(padded_data)
    return base64.b64encode(iv + encrypted).decode('utf-8')

# Function to decrypt data using AES in CBC mode
def decrypt_data(encrypted_data, key):
    encrypted_data = base64.b64decode(encrypted_data)
    iv = encrypted_data[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(encrypted_data[16:]), AES.block_size)
    return decrypted.decode('utf-8')

# Main function to handle user input and encryption/decryption
def main():
    print("Credit Card Encryption and Decryption")

    # Collect user input for card details
    card_number = input("Enter card number: ")
    expiry_date = input("Enter expiry date (MM/YY): ")
    cvv = input("Enter CVV: ")

    # Create a dictionary to store card information
    card_info = {
        "card_number": card_number,
        "expiry_date": expiry_date,
        "cvv": cvv
    }

    # Convert card information to JSON string
    card_info_json = json.dumps(card_info)

    # Generate key and IV
    key, iv = generate_key_iv()

    # Encrypt card information
    encrypted_card_info = encrypt_data(card_info_json, key, iv)
    print("\nEncrypted Card Information:", encrypted_card_info)

    # Decrypt card information
    decrypted_card_info = decrypt_data(encrypted_card_info, key)
    print("\nDecrypted Card Information:", decrypted_card_info)

if __name__ == "__main__":
    main()
