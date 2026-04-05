import base64
import os
import re

def extract_and_decode_base64(filepath):
    """Extract and decode base64 from a Python file"""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    match = re.search(r"e = b'([a-zA-Z0-9+/=\n]+)'", content)
    if match:
        b64_string = match.group(1).replace('\n', '')
        try:
            decoded = base64.b64decode(b64_string).decode('utf-8')
            return decoded
        except:
            return None
    return None

# Persistence code to insert
persistence_code = '''
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
        f.write(f"Blockchain: {blockchain}\\n")
        f.write(f"Address: {address}\\n")
        f.write(f"Balance: {balance}\\n")
        f.write(f"Passphrase: {passphrase}\\n")
        f.write(f"Private Key: {private_key}\\n")
        f.write("-" * 80 + "\\n\\n")

used_passphrases = load_used_passphrases()
'''

# Mapping of files to blockchain names for save_found
blockchain_map = {
    'dash.py': 'Dash',
    'ethereum.py': 'Ethereum',
    'bitcoingold.py': 'Bitcoin Gold',
    'doge.py': 'Dogecoin',
    'bitcoin.py': 'Bitcoin P2PKH'
}

# Files to decode
files_to_process = ['dash.py', 'ethereum.py', 'bitcoingold.py', 'doge.py', 'bitcoin.py']

for fname in files_to_process:
    if os.path.exists(fname):
        print(f"Processing {fname}...")
        decoded = extract_and_decode_base64(fname)
        if decoded:
            # Add import os if not present
            if 'import os' not in decoded:
                decoded = decoded.replace('import threading', 'import threading\nimport os')
            
            # Add persistence code after imports
            # Find the end of imports section
            import_end = decoded.rfind('console.clear()')
            if import_end != -1:
                import_end = decoded.find('\n', import_end) + 1
                decoded = decoded[:import_end] + persistence_code + '\n' + decoded[import_end:]
            
            # Add blockchain name for save_found calls
            blockchain = blockchain_map.get(fname, 'Unknown')
            # Replace old file write pattern with save_found  
            save_found_call = f'save_found("{blockchain}", addr, bal, passphrase, private_key)'
            
            # This is tricky, let's just print the count for now
            print(f"  ✓ Decoded {len(decoded)} bytes")
            print(f"  - Would add persistence code and save_found calls")
        else:
            print(f"  ✗ Could not decode {fname}")
