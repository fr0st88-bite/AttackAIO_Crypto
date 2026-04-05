@Echo off
title Bitcoin ALL Type [MMDRZA.CoM]
Pushd "%~dp0"

echo [*] Running Bitcoin P2PKH...
python bitcoin-p2pkh.py

echo [*] Running Bitcoin P2SH...
python bitcoin-p2sh.py

echo [*] Running Bitcoin P2WPKH...
python bitcoin-p2wpkh.py

echo [*] Running Bitcoin P2WSH...
python bitcoin-p2wsh.py

echo [*] Running Bitcoin P2WPKH-nested...
python bitcoin-p2wpkh1.py

echo [*] Running Bitcoin P2WSH-nested...
python bitcoin-p2wsh2.py

echo [+] All Bitcoin variants complete!
