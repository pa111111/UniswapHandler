from datetime import datetime
from Domain.Assets import AssetHourPrice
from Repository.AssetRepository import get_asset_price_provider, get_asset, \
    get_all_hour_prices, get_last_hour_price, update_hour_prices
from Service.FlipsideService import FlipsideService


def main():
    asset = get_asset('ARB')
    service = FlipsideService('6f931420-e70d-404a-a123-50959b03a493')
    prices_list = service.load_all_prices(asset)
    update_hour_prices(asset.id, prices_list)

def test_save_new_price():
    prices = []
    asset_hour_price = AssetHourPrice(symbol='WETH',
                                      hour=datetime.strptime('2023-11-25T16:00:00.000Z', '%Y-%m-%dT%H:%M:%S.%fZ'),
                                      price=1.00)
    prices.append(asset_hour_price)
    update_hour_prices(prices)

def load_price_from_flipside():
    symbol = 'WETH'
    price_provider = get_asset_price_provider(symbol)
    last_price = get_last_hour_price(symbol)

    service = FlipsideService('6f931420-e70d-404a-a123-50959b03a493')
    #result = service.load_prices(price_provider[0].token_address, price_provider[0].blockchain, last_price.hour)
    #print(result)

def test_load_asset_data():
    prices = get_all_hour_prices('WMATIC')
    last_price = get_last_hour_price('WETH')

    print(type(prices))
    print(prices)

    print(type(last_price))
    print(last_price)

main()
