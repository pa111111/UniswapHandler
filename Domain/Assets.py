import decimal
from dataclasses import dataclass
from datetime import datetime
from pyarrow import timestamp


@dataclass
class AssetHourPrice:
    symbol: str
    hour: timestamp
    price: decimal


@dataclass
class AssetPrice:
    symbol: str
    ts: datetime
    period: str
    price: decimal
    numeraire: str


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
    _price_provider = None
    _last_hour_of_usd_price = datetime(2000, 1, 1)
    _last_day_of_usd_price = datetime(2000, 1, 1)
    _last_day_of_weth_price = datetime(2000, 1, 1)

    def is_weth(self):
        return self.symbol == 'WETH'

    def set_price_provider(self, provider: AssetPriceProvider):
        self._price_provider = provider

    @property
    def price_provider(self) -> AssetPriceProvider:
        return self._price_provider

    def set_last_hour_of_usd_price(self, last_hour_of_usd_price: datetime):
        if last_hour_of_usd_price is not None:
            self._last_hour_of_usd_price = last_hour_of_usd_price

    @property
    def last_hour_of_usd_price(self):
        return self._last_hour_of_usd_price

    def set_last_day_of_usd_price(self, last_day_of_usd_price: datetime):
        if last_day_of_usd_price is not None:
            self._last_day_of_usd_price = last_day_of_usd_price

    @property
    def last_day_of_usd_price(self):
        return self._last_day_of_usd_price

    def set_last_day_of_weth_price(self, last_day_of_weth_price: datetime):
        if last_day_of_weth_price is not None:
            self._last_day_of_weth_price = last_day_of_weth_price

    @property
    def last_day_of_weth_price(self):
        return self._last_day_of_weth_price


class BlockchainAsset(Asset):

    def __init__(self, name, symbol, token_address, blockchain):
        self.token_address = token_address
        self.blockchain = blockchain
        Asset.__init__(self, name, symbol)
