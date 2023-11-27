from collections import namedtuple

Cryptocurrency = namedtuple("Cryptocurrency", "symbol address blockchain hour_prices")

Prices = namedtuple("Prices", "price hour")
