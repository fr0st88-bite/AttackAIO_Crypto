"""Persistence tracking module for blockchain address scanning"""
import os

USED_FILE = "used_passphrases.txt"
FOUND_FILE = "found.txt"

def load_used_passphrases():
    """Load already processed passphrases"""
    if os.path.exists(USED_FILE):
        with open(USED_FILE, 'r', encoding='utf-8') as f:
            return set(line.strip() for line in f if line.strip())
    return set()

def add_to_used(passphrase):
    """Mark passphrase as processed"""
    with open(USED_FILE, 'a', encoding='utf-8') as f:
        f.write(passphrase + '\n')

def save_found(blockchain, address, balance, passphrase, private_key):
    """Save to centralized found.txt"""
    with open(FOUND_FILE, 'a', encoding='utf-8', errors='ignore') as f:
        f.write(f"Blockchain: {blockchain}\n")
        f.write(f"Address: {address}\n")
        f.write(f"Balance: {balance}\n")
        f.write(f"Passphrase: {passphrase}\n")
        f.write(f"Private Key: {private_key}\n")
        f.write("-" * 80 + "\n\n")
