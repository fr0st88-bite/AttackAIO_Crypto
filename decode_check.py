import base64
import os
import re

# Function to decode and extract base64 code
def decode_base64_script(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Find the base64 string
    match = re.search(r"e = b'([a-zA-Z0-9+/=\n]+)'", content)
    if match:
        b64_string = match.group(1).replace('\n', '')
        decoded = base64.b64decode(b64_string).decode('utf-8')
        return decoded
    return None

# List of base64-encoded files to check
base64_files = ['dash.py', 'ethereum.py', 'bitcoingold.py', 'doge.py', 'bitcoin.py']

for fname in base64_files:
    if os.path.exists(fname):
        decoded = decode_base64_script(fname)
        if decoded:
            print(f"\n{'='*60}")
            print(f"File: {fname}")
            print(f"{'='*60}")
            print(decoded[:500] + "..." if len(decoded) > 500 else decoded)
