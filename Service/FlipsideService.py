from flipside import Flipside
import pandas as pd
from datetime import datetime
from Domain.Assets import AssetHourPrice, Asset, AssetPrice

_flipside_url = 'https://api-v2.flipsidecrypto.xyz'
_flipside_api = '6f931420-e70d-404a-a123-50959b03a493'

"""
def load_all_prices(asset: Asset):
    sql = "select symbol, price, hour from crosschain.price.ez_hourly_token_prices " \
          "where token_address = lower('{0}') and blockchain = lower('{1}') order by hour desc" \
        .format(asset.price_provider.token_address, asset.price_provider.blockchain)
    query_result_set = Flipside(_flipside_api, _flipside_url).query(sql)

    price_list = []
    for index, row in pd.DataFrame(query_result_set.rows, columns=query_result_set.columns).iterrows():
        price_list.append(AssetHourPrice(row['symbol'],
                                         datetime.strptime(row['hour'], '%Y-%m-%dT%H:%M:%S.%fZ'),
                                         row['price']))
    return price_list
"""


def load_hour_usd_prices_from_last_hour(asset: Asset):
    sql = "select symbol, price, hour from crosschain.price.ez_hourly_token_prices " \
          "where token_address = lower('{0}') and blockchain = lower('{1}') and hour > '{2}' order by hour desc" \
        .format(asset.price_provider.token_address, asset.price_provider.blockchain,
                asset.last_hour_of_usd_price.strftime('%Y-%m-%d %H:%M:%S'))
    query_result_set = Flipside(_flipside_api, _flipside_url).query(sql)

    prices = []
    for index, row in pd.DataFrame(query_result_set.rows, columns=query_result_set.columns).iterrows():
        prices.append(AssetPrice(row['symbol'], datetime.strptime(row['hour'], '%Y-%m-%dT%H:%M:%S.%fZ'),
                                 'hour', row['price'], 'USD'))
    return prices

