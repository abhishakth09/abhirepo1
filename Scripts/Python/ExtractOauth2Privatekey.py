import base64
import json
import re
from cryptography.hazmat.primitives import serialization

def extract_modulus():
    # 1. Read the file content
    with open("private_key.pem", "r", encoding="utf-8") as key_file:
        raw_content = key_file.read().strip()

    # Try Option A: If the file is actually a JSON / JWK structure
    try:
        json_data = json.loads(raw_content)
        # Check if it has a 'd' parameter (private key components in JWK)
        if "n" in json_data:
            print("\n" + "="*50)
            print("SUCCESS: Detected a JWK/JSON file structure.")
            print("="*50)
            print(f"Your Key Modulus ('n' value):\n\n{json_data['n']}")
            print("="*50 + "\n")
            return
    except json.JSONDecodeError:
        pass # Not a JSON file, proceed to PEM cleanup

    # Try Option B: Force-clean the PEM framing
    # Strip any existing header/footer frames and spaces to find the pure base64 payload
    pure_b64 = re.sub(r'-----(BEGIN|END)[^-]*-----', '', raw_content)
    pure_b64 = "".join(pure_b64.split()) # Remove all newlines and spaces

    # Re-apply perfectly formatted standard PKCS#8 framing
    formatted_pem = f"-----BEGIN PRIVATE KEY-----\n"
    # Chunk base64 into standard 64-character lines
    for i in range(0, len(pure_b64), 64):
        formatted_pem += pure_b64[i:i+64] + "\n"
    formatted_pem += "-----END PRIVATE KEY-----"

    try:
        private_key = serialization.load_pem_private_key(formatted_pem.encode('utf-8'), password=None)
        n = private_key.private_numbers().public_numbers.n
        
        bit_length = n.bit_length()
        byte_length = (bit_length + 7) // 8
        n_bytes = n.to_bytes(byte_length, byteorder="big")
        okta_n_format = base64.urlsafe_b64encode(n_bytes).decode("utf-8").rstrip("=")
        
        print("\n" + "="*50)
        print("SUCCESS: Standardized PEM framing and loaded key.")
        print("="*50)
        print(f"Your Key Modulus ('n' value for Okta matching):\n\n{okta_n_format}")
        print("="*50 + "\n")
        
    except Exception as e:
        print(f"\nCRITICAL ERROR: Could not parse key data. Details: {e}")
        print("Please open 'private_key.pem' in text editor and check if it starts with '{' or 'MII'.")

if __name__ == "__main__":
    extract_modulus()