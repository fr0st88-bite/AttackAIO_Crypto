#!/usr/bin/env python3
"""
Persistence and Centralization Verification Report
==================================================

This script verifies that all cryptocurrency scanning scripts have been
updated with persistence tracking and centralized findings output.
"""

import os
import re

BITCOINS = [
    'bitcoin-p2pkh.py',
    'bitcoin-p2sh.py', 
    'bitcoin-p2wpkh.py',
    'bitcoin-p2wpkh1.py',
    'bitcoin-p2wsh.py',
    'bitcoin-p2wsh2.py',
]

ALTCOINS = [
    'bitcoincash.py',
    'litecoin.py',
    'zcash.py',
    'qtum.py',
    'tron.py',
    'digibyte.py',
]

BASE64_DECODED = [
    'dash.py',
    'ethereum.py',
    'bitcoingold.py',
    'doge.py',
    'bitcoin.py',
]

def check_persistence(filepath):
    """Check if file has persistence integration"""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    checks = {
        'has_imports': 'import os' in content,
        'has_functions': 'def load_used_passphrases' in content and 'def add_to_used' in content and 'def save_found' in content,
        'has_persistence_check': 'if passphrase in used_passphrases:' in content,
        'has_save_found_calls': 'save_found(' in content,
        'has_add_to_used_calls': 'add_to_used(' in content,
        'has_global_declaration': 'global used_passphrases' in content,
    }
    
    return all(checks.values()), checks

def verify_all():
    """Verify all files"""
    print("=" * 70)
    print("PERSISTENCE AND CENTRALIZATION VERIFICATION REPORT")
    print("=" * 70)
    print()
    
    all_good = True
    
    for category, files in [("Bitcoin Variants", BITCOINS), ("Altcoins", ALTCOINS), ("Base64-Decoded", BASE64_DECODED)]:
        print(f"\n{category}:")
        print("-" * 70)
        
        for fname in files:
            if os.path.exists(fname):
                is_good, checks = check_persistence(fname)
                status_symbol = "✓" if is_good else "✗"
                print(f"  {status_symbol} {fname:<25}", end="")
                
                if not is_good:
                    all_good = False
                    failed = [k for k, v in checks.items() if not v]
                    print(f"  — Missing: {', '.join(failed)}")
                else:
                    print()
            else:
                print(f"  ✗ {fname:<25} — FILE NOT FOUND")
                all_good = False
    
    print()
    print("=" * 70)
    
    if all_good:
        print("✓ SUCCESS: All files properly updated with persistence!")
        print()
        print("Summary:")
        print("  • Persistence tracking enabled (used_passphrases.txt)")
        print("  • Centralized findings (found.txt)")
        print("  • Format: Blockchain, Address, Balance, Passphrase, Private Key")
        print("  • Duplicate passphrases skipped automatically")
        return 0
    else:
        print("✗ FAILURE: Some files missing persistence code")
        return 1

if __name__ == "__main__":
    exit(verify_all())
