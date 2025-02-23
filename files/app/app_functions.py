import os
import json
import base64
import hashlib
import uuid
import shutil
from datetime import datetime
from PyQt6.QtWidgets import QMessageBox
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
# In your other file (e.g., main.py)
import files.app.config as config

# Access the variables using dot notation
key_file = os.path.join(config.SECURE_DIR, "master_key.bin")
locked_file = os.path.join(config.SECURE_DIR, "locked_items.json")
access_log = os.path.join(config.SECURE_DIR, "access_log.txt")
secure_dir = config.SECURE_DIR
theme_dark = config.STYLE_CONFIG_DARK
theme_light = config.STYLE_CONFIG_LIGHT

# Ensure the secure directory exists
if not os.path.exists(secure_dir):
    os.makedirs(secure_dir)

# Load or set master key
if not os.path.exists(key_file):
    MASTER_PASSWORD = "default_master"  # Replace with user input on first run
    MASTER_KEY = base64.urlsafe_b64encode(hashlib.sha256(MASTER_PASSWORD.encode()).digest())
    with open(key_file, "wb") as f:
        f.write(MASTER_KEY)
else:
    with open(key_file, "rb") as f:
        MASTER_KEY = f.read()

MASTER_FERNET = Fernet(MASTER_KEY)

class AppFunctions:
    @staticmethod
    def show_message(parent, message, title, theme=theme_dark):
        msg_box = QMessageBox(parent)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        stylesheet = f"""
            QMessageBox {{
                background-color: {theme['bg_color']};
                color: {theme['text_color']};
                font: {theme['font_size_large']} "{theme['font_family']}";
                border-radius: 10px;
                padding: 20px;
            }}
            QMessageBox QPushButton {{
                background-color: {theme['accent_color']};
                color: {theme['selected_text_color']};
                padding: 10px 20px;
                font: {theme['font_size_medium']} "{theme['font_family']}";
                border-radius: 5px;
                min-width: 100px;
            }}
            QMessageBox QPushButton:hover {{
                background-color: {theme['accent_hover']};
            }}
            QMessageBox QPushButton:pressed {{
                background-color: {theme['accent_pressed']};
            }}
        """
        msg_box.setStyleSheet(stylesheet)
        msg_box.exec()

    @staticmethod
    def derive_key(password, salt=None):
        if salt is None:
            salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt

    @staticmethod
    def encrypt_file(file_path, password):
        key, salt = AppFunctions.derive_key(password)
        fernet = Fernet(key)
        with open(file_path, "rb") as f:
            data = f.read()
        encrypted_data = fernet.encrypt(data)
        with open(file_path, "wb") as f:
            f.write(encrypted_data)
        return salt

    @staticmethod
    def decrypt_file(file_path, password, salt):
        key, _ = AppFunctions.derive_key(password, salt)
        fernet = Fernet(key)
        with open(file_path, "rb") as f:
            encrypted_data = f.read()
        decrypted_data = fernet.decrypt(encrypted_data)
        with open(file_path, "wb") as f:
            f.write(decrypted_data)

    @staticmethod
    def encrypt_items(item_path, password):
        salt = None
        if os.path.isfile(item_path):
            salt = AppFunctions.encrypt_file(item_path, password)
        elif os.path.isdir(item_path):
            for root, _, files in os.walk(item_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    salt = AppFunctions.encrypt_file(file_path, password)
        return salt

    @staticmethod
    def decrypt_items(item_path, password, salt):
        if os.path.isfile(item_path):
            AppFunctions.decrypt_file(item_path, password, salt)
        elif os.path.isdir(item_path):
            for root, _, files in os.walk(item_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    AppFunctions.decrypt_file(file_path, password, salt)

    @staticmethod
    def secure_delete(file_path):
        if os.path.isfile(file_path):
            with open(file_path, "wb") as f:
                f.write(os.urandom(os.path.getsize(file_path)))
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path, ignore_errors=True)

    @staticmethod
    def log_action(action):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {action}"
        encrypted_entry = MASTER_FERNET.encrypt(log_entry.encode())
        with open(access_log, "ab") as f:
            f.write(encrypted_entry + b"\n")

    @staticmethod
    def load_locked_items():
        if not os.path.exists(locked_file):
            return {}
        with open(locked_file, "rb") as f:
            encrypted_data = f.read()
        if not encrypted_data:
            return {}
        try:
            decrypted_data = MASTER_FERNET.decrypt(encrypted_data)
            return json.loads(decrypted_data.decode())
        except Exception:
            return {}

    @staticmethod
    def save_locked_items(items):
        encrypted_data = MASTER_FERNET.encrypt(json.dumps(items).encode())
        with open(locked_file, "wb") as f:
            f.write(encrypted_data)