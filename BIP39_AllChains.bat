@Echo off
title BIP39 Seed Phrase Scanner - All Blockchains [MMDRZA.CoM]
Pushd "%~dp0"
color 0a

echo.
echo ============================================
echo  BIP39 Seed Phrase Scanner - ALL BLOCKCHAINS
echo  Generates 12/18/24 word phrases for every supported chain
echo  Checks addresses against the corresponding target file
echo  Saves matches to FOUND.txt
echo ============================================
echo.

echo [*] Running Bitcoin...
python bip39_scanner.py bitcoin

echo [*] Running Bitcoin Cash...
python bip39_scanner.py bitcoincash

echo [*] Running Bitcoin Gold...
python bip39_scanner.py bitcoingold

echo [*] Running Dash...
python bip39_scanner.py dash

echo [*] Running DigiByte...
python bip39_scanner.py digibyte

echo [*] Running Dogecoin...
python bip39_scanner.py doge

echo [*] Running Ethereum...
python bip39_scanner.py ethereum

echo [*] Running Litecoin...
python bip39_scanner.py litecoin

echo [*] Running Qtum...
python bip39_scanner.py qtum

echo [*] Running Tron...
python bip39_scanner.py tron

echo [*] Running Zcash...
python bip39_scanner.py zcash

echo.
echo ============================================
echo  ALL-CHAIN SCAN COMPLETE
echo  Check FOUND.txt for any matches
echo ============================================
echo.

if exist FOUND.txt (
    echo [+] Found Results:
    echo.
    type FOUND.txt
) else (
    echo [-] No matches found yet
)

echo.
pause
