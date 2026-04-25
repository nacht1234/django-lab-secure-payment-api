from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher = Fernet(key)

def encrypt_data(data: str) -> bytes:
    return cipher.encrypt(data.encode())

def decrypt_data(token: bytes) -> str:
    return cipher.decrypt(token).decode()