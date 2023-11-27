from datetime import datetime
from Domain.Assets import AssetPriceProvider


def load_all_hour_prices(symbol, price_provider: AssetPriceProvider):
    return None


def load_hour_prices(symbol, price_provider: AssetPriceProvider, from_ts:datetime):
    if price_provider.price_provider_name == 'flipside':
        return None
    return None
