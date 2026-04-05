#!/usr/bin/env python3
"""Fix HDWallet API calls across all cryptocurrency scripts."""

import os
import re

# Define cryptocurrency mappings
CRYPTO_MAPPINGS = {
    'bitcoin-p2wpkh.py': ('BitcoinMainnet', 'BTC'),
    'bitcoin-p2wpkh1.py': ('BitcoinMainnet', 'BTC'),
    'bitcoin-p2wsh.py': ('BitcoinMainnet', 'BTC'),
    'bitcoin-p2wsh2.py': ('BitcoinMainnet', 'BTC'),
    'bitcoincash.py': ('BitcoinCashMainnet', 'BCH'),
    'litecoin.py': ('LitecoinMainnet', 'LTC'),
    'zcash.py': ('ZcashMainnet', 'ZEC'),
    'qtum.py': ('QtumMainnet', 'QTUM'),
    'bitcoin.py': ('BitcoinMainnet', 'BTC'),
    'dash.py': ('DashMainnet', 'DASH'),
    'ethereum.py': ('EthereumMainnet', 'ETH'),
    'bitcoingold.py': ('BitcoinGoldMainnet', 'BTG'),
    'doge.py': ('DogecoinMainnet', 'DOGE'),
    'digibyte.py': ('DigiByteMainnet', 'DGB'),
}

def fix_file(filepath, crypto_class, symbol_short):
    """Fix a single Python script file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Fix import
    symbol_import = f"from hdwallet.symbols import {symbol_short} as SYMBOL"
    if symbol_import in content and f"from hdwallet.cryptocurrencies import {crypto_class}" not in content:
        content = content.replace(
            symbol_import,
            f"{symbol_import}\nfrom hdwallet.cryptocurrencies import {crypto_class}"
        )
    
    # Fix HDWallet instantiation
    content = re.sub(
        r'HDWallet\(symbol=SYMBOL\)',
        f'HDWallet(cryptocurrency={crypto_class}, symbol=SYMBOL)',
        content
    )
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# Fix all scripts
os.chdir('C:\\Users\\Nrobb\\AttackAIO_Crypto')
fixed_count = 0

for filename, (crypto_class, symbol) in CRYPTO_MAPPINGS.items():
    if os.path.exists(filename):
        if fix_file(filename, crypto_class, symbol):
            print(f"✓ Fixed: {filename}")
            fixed_count += 1
        else:
            print(f"- Already fixed or not needed: {filename}")
    else:
        print(f"✗ Not found: {filename}")

print(f"\n✓ Total files fixed: {fixed_count}")
