# Secure Vault

A Python application for securely managing files with encryption, secure deletion, and dynamic theme support. Built with PyQt6, it provides a user-friendly interface and integrates with system themes using `darkdetect`.

## Features
- **File Encryption/Decryption**: Encrypt and decrypt files or directories using a password-derived key with Fernet (symmetric encryption).
- **Secure Deletion**: Overwrite files with random data before deletion to prevent recovery.
- **Access Logging**: Log actions in an encrypted file for audit purposes.
- **Locked Items Management**: Store and manage a list of locked items in an encrypted JSON file.
- **Dynamic Theme Support**: Automatically adjust the UI theme (dark/light) based on the system theme using `darkdetect`.
- **Cross-Platform**: Primarily designed for Windows, with potential for broader compatibility.

## Requirements
- Python 3.11.0
- PyQt6
- cryptography
- darkdetect

Install dependencies via pip:

```bash
pip install PyQt6 cryptography darkdetect
```
```bash
secure-file-manager/
│
├── files/
│   ├── app/
│   │   ├── config.py       # Configuration settings (MASTER_KEY_FILE, SECURE_DIR, etc.)

│   │   └── data/          # Directory for storing encrypted files and logs
│   └── main.py            # Main application logic
│
└── README.md              # This file
```
![image](https://github.com/user-attachments/assets/edadb7bb-d86d-4cd3-84c7-8544785e1093)

