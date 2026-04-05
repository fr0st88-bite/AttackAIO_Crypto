#!/usr/bin/env python3
"""Fix filename handling in cryptocurrency scripts"""

import os
import re

def fix_filename_handling(filepath):
    """Fix filename handling to support both files.txt and files input"""
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    original = content
    
    # Pattern 1: filer + ".txt"
    content = re.sub(
        r'filer = input\((.*?)\)\s+filename = str\(filer \+ "\.txt"\)',
        r'filer = input(\1)\nif not filer.endswith(".txt"):\n    filename = filer + ".txt"\nelse:\n    filename = filer',
        content,
        flags=re.DOTALL
    )
    
    # Pattern 2: filexname + ".txt"  
    content = re.sub(
        r'filexname = input\((.*?)\)\s+mylist = \[\]\s+filename = str\(filexname \+ "\.txt"\)',
        r'filexname = input(\1)\n\nmylist = []\n\nif not filexname.endswith(".txt"):\n    filename = filexname + ".txt"\nelse:\n    filename = filexname',
        content,
        flags=re.DOTALL
    )
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Fixed {os.path.basename(filepath)}")
        return True
    else:
        return False

# Main directory files to fix
files_to_fix = [
    'bitcoin-p2pkh.py',
    'bitcoin-p2sh.py',
    'bitcoin-p2wpkh.py',
    'bitcoin-p2wpkh1.py',
    'bitcoin-p2wsh.py',
    'bitcoin-p2wsh2.py',
    'bitcoincash.py',
    'litecoin.py',
    'zcash.py',
    'qtum.py',
    'tron.py',
    'digibyte.py',
    'dash.py',
    'ethereum.py',
    'bitcoingold.py',
    'doge.py',
    'bitcoin.py',
]

print("Fixing filename handling in cryptocurrency scripts...\n")

for fname in files_to_fix:
    if os.path.exists(fname):
        fix_filename_handling(fname)
    else:
        print(f"✗ {fname} not found")

print("\nDone!")
