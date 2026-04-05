import base64
import os
import re

def extract_and_decode(filepath):
    """Extract and decode base64 from Python file"""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    match = re.search(r"e = b'([a-zA-Z0-9+/=\n]+)'", content, re.DOTALL)
    if match:
        b64_string = match.group(1).replace('\n', '')
        try:
            return base64.b64decode(b64_string).decode('utf-8')
        except Exception as e:
            print(f"  Error decoding: {e}")
            return None
    return None

def add_persistence_header(code, symbol, blockchain_name):
    """Add persistence code to decoded script"""
    persistence = f'''import os

# Persistence tracking
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
        f.write(passphrase + '\\n')

def save_found(blockchain, address, balance, passphrase, private_key):
    """Save to centralized found.txt"""
    with open(FOUND_FILE, 'a', encoding='utf-8', errors='ignore') as f:
        f.write(f"Blockchain: {{blockchain}}\\n")
        f.write(f"Address: {{address}}\\n")
        f.write(f"Balance: {{balance}}\\n")
        f.write(f"Passphrase: {{passphrase}}\\n")
        f.write(f"Private Key: {{private_key}}\\n")
        f.write("-" * 80 + "\\n\\n")

used_passphrases = load_used_passphrases()'''
    
    # Add of import after threading
    code = code.replace('import threading', f'import threading\n{persistence}')
    
    # Now modify the MmDrza function
    # Find  where count += 1 and passphrase = mylist[i] are, add persistence check
    code = re.sub(
        r'(for i in range\(0, len\(mylist\)\):\s*)\n(\s*count \+=)',
        r'''\1
        passphrase = mylist[i]
        
        if passphrase in used_passphrases:
            continue
        
        \2''',
        code,
        count=1
    )
    
    # Remove the duplicate passphrase = mylist[i] that comes after count += 1
    code = re.sub(
        r'(\n\s*passphrase = mylist\[i\]\s*\n\s*if passphrase in used_passphrases.*?continue\s*)\s*\n(\s*count.*?\n\s*passphrase = mylist\[i\])',
        r'\1',
        code,
        flags=re.DOTALL,
        count=1
    )
    
    # Replace file write with save_found
    code = re.sub(
        r'''fx = open\(u?"BitcoinWinner[^"]*_MMDRZA\.txt", "a"\).*?fx\.close\(\)''',
        f'save_found("{blockchain_name}", addr, bal, passphrase, private_key)',
        code,
        flags=re.DOTALL,
        count=1
    )
    
    # Add persistence mark at end of continue
    #code = code + \n    add_to_used(passphrase)\n    used_passphrases.add(passphrase)
    code = re.sub(
        r'(else:\s+print\(f"[^"]+"\)\s+continue)',
        r'\1\n        \n        add_to_used(passphrase)\n        used_passphrases.add(passphrase)',
        code,
        count=1
    )
    
    return code

# Process base64 files
files_config = {
    'dash.py': ('DASH', 'Dash'),
    'ethereum.py': ('ETH', 'Ethereum'),
    'bitcoingold.py': ('BTG', 'Bitcoin Gold'),
    'doge.py': ('DOGE', 'Dogecoin'),
    'bitcoin.py': ('BTC', 'Bitcoin'),
}

for fname, (symbol, blockchain_name) in files_config.items():
    if os.path.exists(fname):
        print(f"Processing {fname}...")
        decoded = extract_and_decode(fname)
        if decoded:
            modified = add_persistence_header(decoded, symbol, blockchain_name)
            
            # Backup and write
            os.rename(fname, f"_{fname}.bak")
            with open(fname, 'w', encoding='utf-8') as f:
                f.write(modified)
            
            print(f"  ✓ Updated {fname}")
        else:
            print(f"  ✗ Failed to decode {fname}")
