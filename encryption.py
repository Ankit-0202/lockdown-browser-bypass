#!/usr/bin/env python3

import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import json


class SecureCommunication:
    def __init__(self):
        # Generate a random salt for key derivation
        self.salt = os.urandom(16)
        # Generate a random key for encryption
        self.key = self._derive_key()
        self.cipher = Fernet(self.key)

    def _derive_key(self):
        """Derive a secure key using PBKDF2"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        # Use a random password for key derivation
        password = os.urandom(32)
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return key

    def encrypt_message(self, message):
        """Encrypt a message and return it in a format that looks like normal web traffic"""
        # Convert message to bytes if it's a string
        if isinstance(message, str):
            message = message.encode()

        # Encrypt the message
        encrypted = self.cipher.encrypt(message)

        # Create a payload that looks like normal web traffic
        payload = {
            "type": "application/json",
            "data": base64.b64encode(encrypted).decode(),
            "timestamp": str(int(time.time() * 1000)),
            "content_type": "text/plain",
            "encoding": "gzip",
            "cache_control": "no-cache",
        }

        # Convert to a format that looks like a normal HTTP request
        return json.dumps(payload)

    def decrypt_message(self, encrypted_payload):
        """Decrypt a message from its web traffic format"""
        try:
            # Parse the payload
            payload = json.loads(encrypted_payload)

            # Extract and decode the encrypted data
            encrypted_data = base64.b64decode(payload["data"])

            # Decrypt the message
            decrypted = self.cipher.decrypt(encrypted_data)

            # Convert back to string if it was originally a string
            try:
                return decrypted.decode()
            except:
                return decrypted

        except Exception as e:
            raise ValueError(f"Failed to decrypt message: {str(e)}")

    def generate_stealth_headers(self):
        """Generate headers that make the traffic look like normal browser activity"""
        return {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
        }
