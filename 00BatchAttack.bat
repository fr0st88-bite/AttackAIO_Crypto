@Echo off
title AiO Batch Crypto Attack - All Results to found.txt [MMDRZA.CoM]
Pushd "%~dp0"
color 0a

echo.
echo ============================================
echo  AiO Batch Crypto Scanner
echo  All results accumulate in: found.txt
echo ============================================
echo.
echo Choose scanner type:
echo [1] Brain Wallet Scanner (original)
echo [2] BIP39 Seed Phrase Scanner (new)
echo [3] BIP39 All Chains

echo.
set /p choice="Enter choice (1, 2, or 3): "

if "%choice%"=="1" goto brainwallet
if "%choice%"=="2" goto bip39
if "%choice%"=="3" goto bip39_all
goto end

:brainwallet
REM Bitcoin Variants
echo [*] Running Bitcoin P2PKH Scanner...
python bitcoin-p2pkh.py

echo [*] Running Bitcoin P2SH Scanner...
python bitcoin-p2sh.py

echo [*] Running Bitcoin P2WPKH Scanner...
python bitcoin-p2wpkh.py

echo [*] Running Bitcoin P2WPKH-nested-P2SH Scanner...
python bitcoin-p2wpkh1.py

echo [*] Running Bitcoin P2WSH Scanner...
python bitcoin-p2wsh.py

echo [*] Running Bitcoin P2WSH-nested-P2SH Scanner...
python bitcoin-p2wsh2.py

REM Altcoins
echo [*] Running Bitcoin Cash Scanner...
python bitcoincash.py

echo [*] Running Litecoin Scanner...
python litecoin.py

echo [*] Running Z-Cash Scanner...
python zcash.py

echo [*] Running Qtum Scanner...
python qtum.py

echo [*] Running Tron Scanner...
if exist tron.py (
    python tron.py
) else if exist trx.py (
    python trx.py
) else (
    echo [-] Tron scanner not found
)

echo [*] Running Digibyte Scanner...
python digibyte.py

echo [*] Running Dash Scanner...
python dash.py

echo [*] Running Ethereum Scanner...
python ethereum.py

echo [*] Running Bitcoin Gold Scanner...
python bitcoingold.py

echo [*] Running Dogecoin Scanner...
python doge.py

echo [*] Running Bitcoin (All Types) Scanner...
python bitcoin.py

goto complete

:bip39
echo.
echo ============================================
echo  BIP39 Seed Phrase Scanner Menu
echo ============================================
echo [1] Bitcoin
echo [2] Bitcoin Cash
echo [3] Bitcoin Gold
echo [4] Dash
echo [5] DigiByte
echo [6] Dogecoin
echo [7] Ethereum
echo [8] Litecoin
echo [9] Qtum
echo [10] Tron
echo [11] Zcash
echo [A] All chains

echo.
set /p bip39choice="Enter choice: "

if /I "%bip39choice%"=="1" python bip39_scanner.py bitcoin & goto complete
if /I "%bip39choice%"=="2" python bip39_scanner.py bitcoincash & goto complete
if /I "%bip39choice%"=="3" python bip39_scanner.py bitcoingold & goto complete
if /I "%bip39choice%"=="4" python bip39_scanner.py dash & goto complete
if /I "%bip39choice%"=="5" python bip39_scanner.py digibyte & goto complete
if /I "%bip39choice%"=="6" python bip39_scanner.py doge & goto complete
if /I "%bip39choice%"=="7" python bip39_scanner.py ethereum & goto complete
if /I "%bip39choice%"=="8" python bip39_scanner.py litecoin & goto complete
if /I "%bip39choice%"=="9" python bip39_scanner.py qtum & goto complete
if /I "%bip39choice%"=="10" python bip39_scanner.py tron & goto complete
if /I "%bip39choice%"=="11" python bip39_scanner.py zcash & goto complete
if /I "%bip39choice%"=="A" (
    python bip39_scanner.py bitcoin
    python bip39_scanner.py bitcoincash
    python bip39_scanner.py bitcoingold
    python bip39_scanner.py dash
    python bip39_scanner.py digibyte
    python bip39_scanner.py doge
    python bip39_scanner.py ethereum
    python bip39_scanner.py litecoin
    python bip39_scanner.py qtum
    python bip39_scanner.py tron
    python bip39_scanner.py zcash
    goto complete
)

echo Invalid selection.
goto end

:bip39_all
call BIP39_AllChains.bat
goto complete

:complete
echo.
echo ============================================
echo  SCAN COMPLETE
echo  Results saved to: found.txt / FOUND.txt
echo ============================================
echo.

if exist found.txt (
    echo [+] Brain wallet results:
    echo.
    type found.txt
)

if exist FOUND.txt (
    echo [+] BIP39 seed phrase results:
    echo.
    type FOUND.txt
)

if not exist found.txt if not exist FOUND.txt (
    echo [-] No results found
)

:end
echo.
pause
