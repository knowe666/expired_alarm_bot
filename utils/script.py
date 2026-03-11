from time import sleep
import datetime
import requests
from pyunycode import pyunycode
from data.config import tonconsole_apikey


def get_domains(wallet):
    domains_list = []
    offset = 0
    data = True
    while data:
        url = f"https://tonapi.io/v2/accounts/{wallet}/nfts?collection=0:b774d95eb20543f186c06b371ab88ad704f7e256130caf96189368a7d0cb6ccf&limit=1000&offset={offset}&indirect_ownership=true"
        while True:
            response = requests.get(url, headers={"Authorization": f"Bearer {tonconsole_apikey}"})
            if response.status_code == 200:
                break
        sleep(1.1)
        data = response.json()['nft_items']
        domains_list.extend([(i, wallet[-4:]) for i in data])
        offset += 1000
    return domains_list


def check_domains(data, on_wallet):
    session = requests.session()
    domains = []
    for i, name_wallet in data:
        if on_wallet.get(i['dns']):
            timestamp_fill = on_wallet[i['dns']]
            expired_days = datetime.datetime.fromtimestamp(timestamp_fill)
            days_left = expired_days - datetime.datetime.now()
        else:
            while True:
                response = session.get(f"https://tonapi.io/v2/blockchain/accounts/{i['address']}/methods/get_last_fill_up_time", headers={"Authorization": f"Bearer {tonconsole_apikey}"})
                if response.status_code == 200:
                    break
                sleep(1.1)
            timestamp_fill = response.json()['decoded']['last_fill_up_time']
            expired_days = datetime.datetime.fromtimestamp(timestamp_fill) + datetime.timedelta(days=366)
            days_left = expired_days - datetime.datetime.now()
        if i.get('sale'):
            market_data = f" {i['sale']['market']['name'].replace('Marketplace', '').replace('Sales', '').replace(' ', '')}" if i['sale']['market'].get('name') else " 🛍️"
        else:
            market_data = ''
        try:
            domain = pyunycode.convert(i['dns'])
        except Exception as e:
            domain = e.args[0].partition(" of '")[2].partition("' not allowed")[0] + '.ton'
        domains.append([days_left, expired_days, domain, market_data, name_wallet])
    domains = sorted(domains, key=lambda x: x[0])
    return domains


def check_on_address(wallet):
    url = f'https://tonapi.io/v2/accounts/{wallet}/dns/expiring'
    while True:
        response = requests.get(url, headers={"Authorization": f"Bearer {tonconsole_apikey}"})
        if response.status_code == 200:
            break
        sleep(1.1)
    data = {i['name']: i['expiring_at'] for i in response.json()['items']}
    return data
