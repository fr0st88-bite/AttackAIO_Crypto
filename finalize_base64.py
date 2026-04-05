import base64
import os
import re

def extract_base64(filepath):
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

# Mapping of files
files_config = {
    'dash.py': ('DASH', 'Dash'),
    'ethereum.py': ('ETH', 'Ethereum'),
    'bitcoingold.py': ('BTG', 'Bitcoin Gold'),
    'doge.py': ('DOGE', 'Dogecoin'),
    'bitcoin.py': ('BTC', 'Bitcoin P2PKH'),
}

persistence_imports = '''import os

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

used_passphrases = load_used_passphrases()'''

for fname, (symbol, blockchain_name) in files_config.items():
    if os.path.exists(fname):
        print(f"\\nUpdating {fname}...")
        decoded = extract_base64(fname)
        if decoded:
            # Add import os if not already there
            if 'import os' not in decoded:
                decoded = decoded.replace('import threading', f'import threading\n{persistence_imports}')
            
            # Now modify the MmDrza() function to use persistence
            # Find the MmDrza function and add persistence checks
            decoded = re.sub(
                r'def MmDrza\(\):\s*w = 0\s*count = 0\s*for i in range\(0, len\(mylist\)\):\s*count \+= 1\s*passphrase = mylist\[i\]',
                f'''def MmDrza():
    global used_passphrases
    w = 0
    count = 0

    for i in range(0, len(mylist)):
        passphrase = mylist[i]
        
        # Skip if already processed
        if passphrase in used_passphrases:
            continue
        
        count += 1''',
                decoded,
                flags=re.DOTALL
            )
            
            # Replace old file write patterns with save_found call
            decoded = re.sub(
                r'fx = open\([^)]+\\\"_MMDRZA\.txt[^)]*\).*?fx\.close\(\)',
                f'save_found("{blockchain_name}", addr, bal, passphrase, private_key)',
                decoded,
                flags=re.DOTALL,
                count=1
            )
            
            # Add mark-as-used at end of loop iteration
            decoded = re.sub(
                r'(else:\s+print\(f[^)]+\)\s+continue)',
                r'\1\n        \n        # Mark as processed\n        add_to_used(passphrase)\n        used_passphrases.add(passphrase)',
                decoded
            )
            
            # Write the modified script
            with open(fname, 'w', encoding='utf-8') as f:
                f.write(decoded)
            
            print(f"  ✓ Updated {fname} ({len(decoded)} bytes)")
        else:
            print(f"  ✗ Failed to decode {fname}")

print("\\n✓ All base64 files updated!")
