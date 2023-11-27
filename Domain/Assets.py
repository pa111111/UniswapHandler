import decimal
from dataclasses import dataclass
from pyarrow import timestamp


@dataclass
class AssetHourPrice:
    symbol: str
    hour: timestamp
    price: decimal


@dataclass
class AssetPriceProvider:
    token_address: str
    price_provider_name: str
    blockchain: str


@dataclass
class Asset:
    id: int
    name: str
    symbol: str
    _last_hour_price = None
    _prices = None
    _price_provider = None

    def set_price_provider(self, provider: AssetPriceProvider):
        self._price_provider = provider

    def get_price_provider(self) -> AssetPriceProvider:
        return self._price_provider

    def set_last_hour_price(self, price: AssetHourPrice):
        self._last_hour_price = price

    def get_last_hour_price(self) -> AssetHourPrice:
        return self._last_hour_price

    def set_hour_prices(self, prices):
        self._prices = prices

    def get_hour_prices(self):
        return self._prices


class BlockchainAsset(Asset):

    def __init__(self, name, symbol, token_address, blockchain):
        self.token_address = token_address
        self.blockchain = blockchain
        Asset.__init__(self, name, symbol)
