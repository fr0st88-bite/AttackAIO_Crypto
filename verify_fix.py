#!/usr/bin/env python3
"""Verify filename handling fix in all cryptocurrency scripts"""

import os
import re

scripts = [
    'bitcoin-p2pkh.py', 'bitcoin-p2sh.py', 'bitcoin-p2wpkh.py', 'bitcoin-p2wpkh1.py',
    'bitcoin-p2wsh.py', 'bitcoin-p2wsh2.py', 'bitcoincash.py', 'litecoin.py',
    'zcash.py', 'qtum.py', 'tron.py', 'digibyte.py', 'dash.py', 'ethereum.py',
    'bitcoingold.py', 'doge.py', 'bitcoin.py'
]

print("Verifying filename handling fix...\n")

all_good = True
for script in scripts:
    if os.path.exists(script):
        with open(script, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Check for the fix: if not filer.endswith('.txt') or if not filexname.endswith('.txt')
        has_fix = "if not filer.endswith('.txt')" in content or "if not filexname.endswith('.txt')" in content
        
        # Make sure old code is NOT there
        has_old_code = 'filename = str(filer + ".txt")' in content or 'filename = str(filexname + ".txt")' in content
        
        if has_fix and not has_old_code:
            print(f"  ✓ {script:<25} FIXED")
        elif has_old_code:
            print(f"  ✗ {script:<25} NEEDS FIX - still has old code")
            all_good = False
        else:
            print(f"  ? {script:<25} UNCLEAR")
            all_good = False
    else:
        print(f"  ✗ {script:<25} FILE NOT FOUND")
        all_good = False

print()
if all_good:
    print("✓ SUCCESS: All scripts have the filename handling fix!")
    print("\nYou can now enter filenames as either:")
    print("  • files (without extension)")
    print("  • files.txt (with extension)")
    print("\nBoth will work correctly.")
else:
    print("✗ Some scripts need attention")
