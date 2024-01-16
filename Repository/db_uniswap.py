# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Asset(Base):
    __tablename__ = 'asset'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    symbol = Column(String(50))
    load_prices = Column(Boolean)


class Blockchain(Base):
    __tablename__ = 'blockchain'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))


class PurchasePeriod(Base):
    __tablename__ = 'purchase_period'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))


class AssetBlockchain(Base):
    __tablename__ = 'asset_blockchain'

    id = Column(Integer, primary_key=True)
    token_address = Column(String(50))
    symbol = Column(String(50))
    blockchain_id = Column(ForeignKey('blockchain.id'))
    asset_id = Column(ForeignKey('asset.id'))

    asset = relationship('Asset')
    blockchain = relationship('Blockchain')


class AssetHourUsdPrice(Base):
    __tablename__ = 'asset_hour_usd_price'

    id = Column(Integer, primary_key=True)
    asset_id = Column(ForeignKey('asset.id'))
    price = Column(Numeric)
    ts = Column(DateTime)

    asset = relationship('Asset')


class AssetDailyUsdPrice(Base):
    __tablename__ = 'asset_daily_usd_price'

    id = Column(Integer, primary_key=True)
    asset_id = Column(ForeignKey('asset.id'))
    price = Column(Numeric)
    ts = Column(DateTime)

    asset = relationship('Asset')


class AssetDailyWethPrice(Base):
    __tablename__ = 'asset_daily_weth_price'

    id = Column(Integer, primary_key=True)
    asset_id = Column(ForeignKey('asset.id'))
    price = Column(Numeric)
    ts = Column(DateTime)

    asset = relationship('Asset')


class AssetPriceProvider(Base):
    __tablename__ = 'asset_price_provider'

    id = Column(Integer, primary_key=True)
    asset_id = Column(ForeignKey('asset.id'))
    price_provider = Column(String(50))
    token_address = Column(String(50))
    blockchain_id = Column(ForeignKey('blockchain.id'))

    asset = relationship('Asset')
    blockchain = relationship('Blockchain')


class Pool(Base):
    __tablename__ = 'pool'

    id = Column(Integer, primary_key=True)
    pair = Column(String(50))
    fee_tier = Column(Numeric)
    blockchain_id = Column(ForeignKey('blockchain.id'))
    numeraire_id = Column(ForeignKey('asset_blockchain.id'))
    asset_id = Column(ForeignKey('asset_blockchain.id'))
    contract_address = Column(String(50))

    asset = relationship('AssetBlockchain', primaryjoin='Pool.asset_id == AssetBlockchain.id')
    blockchain = relationship('Blockchain')
    numeraire = relationship('AssetBlockchain', primaryjoin='Pool.numeraire_id == AssetBlockchain.id')


class PoolParameter(Base):
    __tablename__ = 'pool_parameters'

    id = Column(Integer, primary_key=True)
    pool_id = Column(ForeignKey('pool.id'))
    ts = Column(DateTime)
    lcf = Column(Numeric)
    risk = Column(Numeric)
    sharpe = Column(Numeric)

    pool = relationship('Pool')


class Position(Base):
    __tablename__ = 'position'

    id = Column(Integer, primary_key=True)
    pool_id = Column(ForeignKey('pool.id'))
    user_address = Column(String(50))
    price_upper = Column(Numeric)
    price_lower = Column(Numeric)
    status = Column(Integer)
    open_ts = Column(DateTime)
    close_ts = Column(DateTime)

    pool = relationship('Pool')


class PositionTransaction(Base):
    __tablename__ = 'position_transaction'

    id = Column(Integer, primary_key=True)
    position_id = Column(ForeignKey('position.id'))
    direction = Column(Integer)
    numeraire = Column(Numeric)
    numeraire_fees = Column(Numeric)
    asset = Column(Numeric)
    asset_fees = Column(Numeric)
    exchange_rate = Column(Numeric)
    ts = Column(DateTime)

    position = relationship('Position')


class Portfolio(Base):
    __tablename__ = 'portfolio'

    id = Column(Integer, primary_key=True)
    purchase_period_id = Column(ForeignKey('purchase_period.id'))
    name = Column(String(250))
    numeraire = Column(String(50))

    purchase_period = relationship('PurchasePeriod')


class AssetInPortfolio(Base):
    __tablename__ = 'asset_in_portfolio'

    id = Column(Integer, primary_key=True)
    period_start = Column(DateTime)
    period_end = Column(DateTime)
    volume = Column(Numeric)
    asset_id = Column(ForeignKey('asset.id'))
    portfolio_id = Column(ForeignKey('portfolio.id'))

    asset = relationship('Asset')
    portfolio = relationship('Portfolio')
