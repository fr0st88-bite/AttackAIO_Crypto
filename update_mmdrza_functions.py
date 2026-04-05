import os
import re

def update_mmdrza_function(filepath, blockchain_name):
    """Update MmDrza function in readable Python files for persistence"""
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Check if already has persistence code
    if 'if passphrase in used_passphrases:' in content:
        print(f"  → {filepath} already updated, skipping")
        return False
    
    # Pattern 1: Add persistence check at start of passphrase loop
    # Look for: for i in range(...): followed by passphrase = mylist[i]
    updated = re.sub(
        r'(for i in range\([^)]+\):\s*\n)(\s*)(passphrase = mylist)',
        r'\1\2global used_passphrases\n\2passphrase = \3',
        content
    )
    
    if updated == content:
        # Try without global if it's not there
        updated = re.sub(
            r'(for i in range\([^)]+\):\s*\n)(\s*)(passphrase = mylist)',
            r'\1\2passphrase = \3',
            content
        )
    
    # Add the skip check right after passphrase assignment
    updated = re.sub(
        r'(passphrase = mylist\[i\])\n(\s*)(.*?)(\n\s*try:|try:)',
        r'\1\n\2if passphrase in used_passphrases:\n\2    continue\n\n\4',
        updated
    )
    
    # Replace fx.write(...) or similar file writes with save_found call
    # Look for patterns like:  fx.write(...) or similar
    updated = re.sub(
        r'fx\s*=\s*open\(["\']([^"\']*)["\'],\s*["\']a["\']\).*?fx\.close\(\)',
        f'save_found("{blockchain_name}", addr, bal, passphrase, private_key)',
        updated,
        flags=re.DOTALL
    )
    
    # Also handle catch where balance is found - replace with save_found
    updated = re.sub(
        r'with\s+open\(["\']([^"\']*)["\'],\s*["\']a["\']\)\s+as\s+\w+:\s+\w+\.write\([^)]+\)',
        f'save_found("{blockchain_name}", addr, bal, passphrase, private_key)',
        updated,
        flags=re.DOTALL
    )
    
    # Add persistence mark at appropriate location (after continue in except, or end of loop)
    # Look for print statements that might come before continue
    updated = re.sub(
        r'(print\(f"[^"]*Found[^"]*"\))(\s*continue)',
        r'\1\n        add_to_used(passphrase)\n        used_passphrases.add(passphrase)\2',
        updated
    )
    
    if updated != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(updated)
        print(f"  ✓ Updated {os.path.basename(filepath)}")
        return True
    else:
        print(f"  ? No changes made to {os.path.basename(filepath)} (pattern not found)")
        return False

# List of files to update
files_to_update = [
    ('bitcoincash.py', 'Bitcoin Cash'),
    ('litecoin.py', 'Litecoin'),
    ('zcash.py', 'Z-Cash'),
    ('qtum.py', 'Qtum'),
    ('tron.py', 'Tron'),
    ('digibyte.py', 'Digibyte'),
    ('bitcoin-p2wpkh1.py', 'Bitcoin P2WPKH-nested-P2SH'),
    ('bitcoin-p2wsh.py', 'Bitcoin P2WSH'),
    ('bitcoin-p2wsh2.py', 'Bitcoin P2WSH-nested-P2SH'),
]

print("Updating MmDrza() functions with persistence...\n")
for fname, blockchain_name in files_to_update:
    if os.path.exists(fname):
        update_mmdrza_function(fname, blockchain_name)
    else:
        print(f"  ✗ {fname} not found")

print("\nDone!")
