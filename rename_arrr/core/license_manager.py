"""
Simple license management system
"""
import hashlib
import json
import os
from datetime import datetime, timedelta
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

class LicenseManager:
    def __init__(self, license_file='.license'):
        self.license_file = license_file
        self.key = get_random_bytes(32)  # AES-256 key
        
    def generate_license(self, email, expiry_days=365):
        """Generate a new license for the user"""
        expiry_date = datetime.now() + timedelta(days=expiry_days)
        license_data = {
            'email': email,
            'expiry_date': expiry_date.isoformat(),
            'hash': hashlib.sha256(email.encode()).hexdigest()
        }
        
        # Encrypt license data
        cipher = AES.new(self.key, AES.MODE_EAX)
        nonce = cipher.nonce
        
        data = json.dumps(license_data).encode()
        ciphertext, tag = cipher.encrypt_and_digest(data)
        
        # Save to file
        with open(self.license_file, 'wb') as f:
            [f.write(x) for x in (nonce, tag, ciphertext)]
            
        return True
        
    def verify_license(self):
        """Verify if license is valid"""
        if not os.path.exists(self.license_file):
            return False
            
        try:
            # Read the license file
            with open(self.license_file, 'rb') as f:
                nonce = f.read(16)
                tag = f.read(16)
                ciphertext = f.read()
                
            # Decrypt
            cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)
            data = cipher.decrypt_and_verify(ciphertext, tag)
            
            # Parse and verify
            license_data = json.loads(data.decode())
            expiry_date = datetime.fromisoformat(license_data['expiry_date'])
            
            # Check if license has expired
            if datetime.now() > expiry_date:
                return False
                
            # Verify hash
            if hashlib.sha256(license_data['email'].encode()).hexdigest() != license_data['hash']:
                return False
                
            return True
            
        except Exception as e:
            return False
            
    def get_license_info(self):
        """Get information about the current license"""
        if not os.path.exists(self.license_file):
            return None
            
        try:
            with open(self.license_file, 'rb') as f:
                nonce = f.read(16)
                tag = f.read(16)
                ciphertext = f.read()
                
            cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)
            data = cipher.decrypt_and_verify(ciphertext, tag)
            
            license_data = json.loads(data.decode())
            expiry_date = datetime.fromisoformat(license_data['expiry_date'])
            
            return {
                'email': license_data['email'],
                'expiry_date': expiry_date.strftime('%Y-%m-%d'),
                'days_remaining': (expiry_date - datetime.now()).days
            }
            
        except Exception as e:
            return None
