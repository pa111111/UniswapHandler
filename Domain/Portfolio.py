import decimal
from dataclasses import dataclass, field
from datetime import datetime
from pyarrow import timestamp
from Domain.Assets import Asset
from typing import List


@dataclass
class PortfolioElementTransaction:
    ts: datetime
    price: decimal
    coins_bought: decimal
    investment_amount: decimal


@dataclass
class PortfolioElement:
    asset: Asset
    period_start: datetime
    period_end: datetime
    volume: decimal
    _transactions = List[PortfolioElementTransaction]

    def add_transaction(self, transaction):
        self._transactions.append(transaction)

    def get_transactions(self):
        return self._transactions


@dataclass
class Portfolio:
    name: str
    numeraire: str
    purchase_period: str
    _portfolio_elements: List[PortfolioElement] = field(default_factory=list)

    def add_portfolio_element(self, element: PortfolioElement):
        self._portfolio_elements.append(element)

    def get_portfolio_elements(self):
        return self._portfolio_elements


