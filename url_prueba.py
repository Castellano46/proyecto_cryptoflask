import requests

'''
url que muestra el precio de todas las criptomonedas.
https://rest.coinapi.io/v1/assets/?apikey=7A83CA6B-6190-415F-89EE-F91E6847848D


Para saber la equivalencia entre cryptos
https://rest.coinapi.io/v1/exchangerate/{}/{}?apikey=7A83CA6B-6190-415F-89EE-F91E6847848D


Para obtener el valor de una crypto en euros
https://rest.coinapi.io/v1/exchangerate/{}/EUR?apikey=7A83CA6B-6190-415F-89EE-F91E6847848D



Pasar de euros a crypto
https://rest.coinapi.io/v1/exchangerate/EUR/{}?apikey=7A83CA6B-6190-415F-89EE-F91E6847848D
'''
'''
    url = 'https://rest.coinapi.io/v1/exchangerate/{crypto}/{convert}?apikey={APIKEY}'.format(crypto, convert, APIKEY)
    data = requests.get(url)
    if data.status_code == 200:
        data = data.json()
        for e in data['data']:
            print(e['rate'])
'''


headers = { 'X-CoinAPI-Key': '7A83CA6B-6190-415F-89EE-F91E6847848D' }
curr = ['BTC','ETH','USDT','BNB','XRP','ADA','SOL','DOT','MATIC']

for i in range(0, 8):
    url = 'https://rest.coinapi.io/v1/exchangerate/EUR/' + curr[i]
    response = requests.get(url, headers=headers)
    res2 = response.json()['rate']
    print('\033[0;36mEUR/' + curr[i] + ' rate:\033[0m', res2)