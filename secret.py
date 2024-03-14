from cryptography.fernet import Fernet

class SecretUtils:
    def __init__(self,key:str):
        key_bytes = bytes.fromhex(key)
        self.cipher_suite = Fernet(key_bytes)

    def encrypt_with_key(self,input_str):
        # Encrypt the secrets
        encrypted_secret = self.cipher_suite.encrypt(input_str.encode())
        encrypted_secret_hex = encrypted_secret.hex()
        return encrypted_secret_hex

    def decrypt_with_key(self,encrypted_secret_hex):
        # Decrypt the secrets 
        encrypted_secret_bytes = bytes.fromhex(encrypted_secret_hex)
        decrypted_secret = self.cipher_suite.decrypt(encrypted_secret_bytes).decode()
        return decrypted_secret
    
        
