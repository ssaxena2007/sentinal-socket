import os
from cryptography.fernet import Fernet
from src.config import LOG_DIR
import time
from src.config import MAX_LOG_SIZE


# The key should be kept very safe. For now, we store it in our log dir.
KEY_FILE = os.path.join(LOG_DIR, "secret.key")

def load_or_generate_key():
    """Retrieves the existing key or creates a new one if it doesn't exist."""
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        return key

def rotate_logs():
    """Checks log size and renames it if it exceeds the limit."""
    log_path = os.path.join(LOG_DIR, "threats.log")
    if os.path.exists(log_path) and os.path.getsize(log_path) > MAX_LOG_SIZE:
        timestamp = int(time.time())
        archive_path = os.path.join(LOG_DIR, f"threats_{timestamp}.log.archive")
        os.rename(log_path, archive_path)
        print(f"Log rotated: Old log archived as {archive_path}")


def log_event_encrypted(data_string):
    """Encrypts a string and appends it to the log file."""
    rotate_logs()  
    key = load_or_generate_key()
    cipher_suite = Fernet(key)
    
    # Encrypt the data (Fernet requires bytes, so we .encode() the string)
    encrypted_text = cipher_suite.encrypt(data_string.encode())
    
    log_path = os.path.join(LOG_DIR, "threats.log")
    with open(log_path, "ab") as log_file:
        log_file.write(encrypted_text + b"\n")
        

def read_encrypted_logs():
    """Decrypts and prints the log file for forensic review."""
    key = load_or_generate_key()
    cipher_suite = Fernet(key)
    log_path = os.path.join(LOG_DIR, "threats.log")
    
    if not os.path.exists(log_path):
        print("No log file found.")
        return

    print("--- Decrypted Forensic Logs ---")
    with open(log_path, "rb") as log_file:
        for line in log_file:
            if line.strip():
                decrypted_text = cipher_suite.decrypt(line).decode()
                print(decrypted_text)