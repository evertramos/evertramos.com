#!/usr/bin/env python3
"""
Generate secure API key for Ezyba production
Usage: python scripts/generate-api-key.py
"""

import secrets
import string
import bcrypt
from datetime import datetime

def generate_secure_api_key(length: int = 64) -> str:
    """Generate cryptographically secure API key"""
    alphabet = string.ascii_letters + string.digits + "-_"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_api_key_hash(api_key: str) -> str:
    """Generate bcrypt hash of API key for verification"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(api_key.encode('utf-8'), salt).decode('utf-8')

def main():
    print("🔐 Ezyba API Key Generator")
    print("=" * 50)
    
    # Generate secure API key
    api_key = f"ezyba-{generate_secure_api_key(48)}"
    api_hash = generate_api_key_hash(api_key)
    
    print(f"Generated at: {datetime.now().isoformat()}")
    print(f"\n🔑 API Key (add to .env):")
    print(f"API_KEY={api_key}")
    
    print(f"\n🔒 API Key Hash (for verification):")
    print(f"{api_hash}")
    
    print(f"\n📝 Frontend Environment Variable:")
    print(f"PUBLIC_API_KEY={api_key}")
    
    print(f"\n⚠️  SECURITY NOTES:")
    print("- Store API key securely in environment variables")
    print("- Never commit API key to version control")
    print("- Rotate API key regularly (monthly recommended)")
    print("- Use different keys for development/production")
    
    # Save to file for backup
    with open("api-key-backup.txt", "w") as f:
        f.write(f"Generated: {datetime.now().isoformat()}\n")
        f.write(f"API_KEY={api_key}\n")
        f.write(f"Hash: {api_hash}\n")
    
    print(f"\n💾 Backup saved to: api-key-backup.txt")
    print("🚨 Remember to delete this file after copying the key!")

if __name__ == "__main__":
    main()