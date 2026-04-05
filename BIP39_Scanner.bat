@Echo off
title BIP39 Seed Phrase Scanner [MMDRZA.CoM]
Pushd "%~dp0"
color 0a

echo.
echo ============================================
echo  BIP39 Seed Phrase Generator & Scanner
echo  Generates 12/18/24 word phrases
echo  Checks addresses against the target blockchain file
echo  Saves matches to FOUND.txt
echo ============================================
echo.
echo Choose blockchain:
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
echo [A] All blockchains

echo.
set /p choice="Enter choice: "

if /I "%choice%"=="1" python bip39_scanner.py bitcoin & goto done
if /I "%choice%"=="2" python bip39_scanner.py bitcoincash & goto done
if /I "%choice%"=="3" python bip39_scanner.py bitcoingold & goto done
if /I "%choice%"=="4" python bip39_scanner.py dash & goto done
if /I "%choice%"=="5" python bip39_scanner.py digibyte & goto done
if /I "%choice%"=="6" python bip39_scanner.py doge & goto done
if /I "%choice%"=="7" python bip39_scanner.py ethereum & goto done
if /I "%choice%"=="8" python bip39_scanner.py litecoin & goto done
if /I "%choice%"=="9" python bip39_scanner.py qtum & goto done
if /I "%choice%"=="10" python bip39_scanner.py tron & goto done
if /I "%choice%"=="11" python bip39_scanner.py zcash & goto done
if /I "%choice%"=="A" (
    call BIP39_AllChains.bat
    goto done
)

echo Invalid selection. Please run this batch again.
goto end

:done
echo.
echo ============================================
echo  SCAN COMPLETE
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

:end