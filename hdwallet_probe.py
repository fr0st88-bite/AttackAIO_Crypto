from hdwallet import HDWallet
from hdwallet.cryptocurrencies import BitcoinMainnet, BitcoinCashMainnet, LitecoinMainnet, DashMainnet, DigiByteMainnet, DogecoinMainnet, QtumMainnet, ZcashMainnet, EthereumMainnet
from hdwallet.symbols import BTC, BCH, LTC, DASH, DGB, DOGE, QTUM, ZEC, ETH
seed='abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about'
checks=[('bitcoin',BitcoinMainnet,BTC),('bitcoincash',BitcoinCashMainnet,BCH),('litecoin',LitecoinMainnet,LTC),('dash',DashMainnet,DASH),('digibyte',DigiByteMainnet,DGB),('doge',DogecoinMainnet,DOGE),('qtum',QtumMainnet,QTUM),('zcash',ZcashMainnet,ZEC),('ethereum',EthereumMainnet,ETH)]
for name,crypto,symbol in checks:
    try:
        hdw=HDWallet(cryptocurrency=crypto,symbol=symbol)
        hdw.from_mnemonic(seed)
        methods=[m for m in dir(hdw) if 'address' in m.lower()]
        print('---', name)
        print('methods:', methods)
        print('p2pkh:', getattr(hdw,'p2pkh_address', lambda:None)())
        print('address:', getattr(hdw,'address', lambda:None)())
    except Exception as e:
        print('ERROR', name, e)
