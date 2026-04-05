import os
import re

def update_altcoin_mmdrza(filepath, blockchain_name):
    """Update altcoin MmDrza functions with persistence"""
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Check if already has persistence code integrated
    if 'if passphrase in used_passphrases:' in content:
        print(f"  → {filepath} already updated, skipping")
        return False
    
    # Add global declaration at start of MmDrza
    updated = re.sub(
        r'(def MmDrza\(\):)\n(\t)(\w+ = 0)',
        r'\1\n\2global used_passphrases\n\2\3',
        content
    )
    
    # Add persistence check right after passphrase assignment
    updated = re.sub(
        r'(\n\t+passphrase = mylist\[i\])\n(\t+)(wallet = )',
        r'\1\n\2if passphrase in used_passphrases:\n\2\tcontinue\n\2\n\2\3',
        updated,
        count=1
    )
    
    # Replace the fx.write() block with save_found call
    updated = re.sub(
        r'if bal != if[xX]\w+:.*?fx\.close\(\)',
        f'if bal != ifx' + blockchain_name + ':\n\t\t\tsave_found("' + blockchain_name + '", addr, bal, passphrase, private_key)\n\t\t\tadd_to_used(passphrase)\n\t\t\tused_passphrases.add(passphrase)\n\t\t\tw += 1',
        updated,
        flags=re.DOTALL,
        count=1
    )
    
    # Fix the ifxBCH/ifxETH variable check if needed
    if 'ifxBCH' in updated and 'if bal != ifxBCH' in updated:
        updated = re.sub(
            r"ifxBCH = '[0-9 A-Z]+'",
            f"ifx{blockchain_name} = '0 {blockchain_name[:3]}'",
            updated
        )
        updated = updated.replace('if bal != ifxBCH:', 'if bal != ifx' + blockchain_name + ':')
    
    if updated != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(updated)
        print(f"  ✓ Updated {os.path.basename(filepath)}")
        return True
    else:
        print(f"  ? No changes made to {os.path.basename(filepath)}")
        return False

# Altcoin files to update
altcoin_files = [
    ('bitcoincash.py', 'BCH'),
    ('litecoin.py', 'LTC'),
    ('zcash.py', 'ZEC'),
    ('qtum.py', 'QTUM'),
    ('tron.py', 'TRX'),
    ('digibyte.py', 'DGB'),
]

print("Updating altcoin scripts with persistence...\n")
for fname, symbol in altcoin_files:
    if os.path.exists(fname):
        update_altcoin_mmdrza(fname, symbol)
    else:
        print(f"  ✗ {fname} not found")

print("\nDone!")
