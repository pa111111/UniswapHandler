from datetime import datetime
from typing import List
from pandas import DataFrame
from sqlalchemy.exc import IntegrityError

from Domain.Assets import Asset, AssetPriceProvider, AssetHourPrice, AssetPrice
from Repository.SessionContext import SessionContext
from Repository.db_uniswap import AssetHourUsdPrice as HourUsdPrice, \
    AssetDailyUsdPrice as DailyUsdPrice, AssetDailyWethPrice as DailyWethPrice, \
    Asset as Asset_DB, AssetPriceProvider as AssetPriceProvider_DB


def get_asset(symbol, load_price_provider=True, load_last_hour_usd_price=True,
              load_last_day_of_usd_price=True, load_last_day_of_weth_price=True):
    with SessionContext() as session:
        asset_db = session.query(Asset_DB).filter_by(symbol=symbol).first()

    asset = Asset(id=asset_db.id, symbol=asset_db.symbol, name=asset_db.name)

    price_provider = None
    if load_price_provider:
        price_provider = _get_asset_price_provider(asset_db.symbol)[0]
    asset.set_price_provider(price_provider)

    if load_last_hour_usd_price:
        asset.set_last_hour_of_usd_price(_get_last_hour_usd_price(asset_db.symbol))

    if load_last_day_of_usd_price:
        asset.set_last_day_of_usd_price(_get_last_day_of_usd_price(asset_db.symbol))

    if load_last_day_of_weth_price:
        asset.set_last_day_of_weth_price(_get_last_day_of_weth_price(asset_db.symbol))

    return asset


def get_asset_list_for_load_prices():
    with SessionContext() as session:
        assets_db = session.query(Asset_DB).filter_by(load_prices=True).all()

    return [get_asset(asset.symbol) for asset in assets_db]


def _get_asset_price_provider(symbol):
    with SessionContext() as session:
        providers = session.query(Asset_DB, AssetPriceProvider_DB) \
            .join(Asset_DB, Asset_DB.id == AssetPriceProvider_DB.asset_id).filter_by(symbol=symbol).all()
        providers_list = []
        for result in providers:
            providers_list.append(AssetPriceProvider(result.AssetPriceProvider.token_address,
                                                     result.AssetPriceProvider.price_provider,
                                                     result.AssetPriceProvider.blockchain.name))
    return providers_list


def _get_last_hour_usd_price(symbol) -> datetime:
    with SessionContext() as session:
        last_hour_of_usd_price = session.query(Asset_DB, HourUsdPrice) \
            .join(Asset_DB, Asset_DB.id == HourUsdPrice.asset_id) \
            .filter_by(symbol=symbol).order_by(HourUsdPrice.ts.desc()).first()

    return last_hour_of_usd_price.AssetHourUsdPrice.ts if last_hour_of_usd_price is not None else None


def _get_last_day_of_usd_price(symbol) -> datetime:
    with SessionContext() as session:
        last_day_of_usd_price = session.query(Asset_DB, DailyUsdPrice) \
            .join(Asset_DB, Asset_DB.id == DailyUsdPrice.asset_id) \
            .filter_by(symbol=symbol).order_by(DailyUsdPrice.ts.desc()).first()

    return last_day_of_usd_price.AssetDailyUsdPrice.ts if last_day_of_usd_price is not None else None


def _get_last_day_of_weth_price(symbol) -> datetime:
    with SessionContext() as session:
        last_day_of_weth_price = session.query(Asset_DB, DailyWethPrice) \
            .join(Asset_DB, Asset_DB.id == DailyWethPrice.asset_id) \
            .filter_by(symbol=symbol).order_by(DailyWethPrice.ts.desc()).first()

    return last_day_of_weth_price.AssetDailyWethPrice.ts if last_day_of_weth_price is not None else None


def get_daily_usd_prices_from_last_weth_price_day(asset: Asset):
    with SessionContext() as session:
        daily_usd_prices = session.query(DailyUsdPrice) \
            .filter_by(asset_id=asset.id) \
            .filter(DailyUsdPrice.ts > asset.last_day_of_weth_price) \
            .order_by(DailyUsdPrice.ts.desc()).all()
    asset_prices = []
    for price in daily_usd_prices:
        asset_prices.append(
            AssetPrice(symbol=asset.symbol, ts=price.ts, period='day', price=price.price, numeraire='USD'))
    return asset_prices


def get_daily_usd_prices_of_weth_from_date(date: datetime):
    with SessionContext() as session:
        asset = get_asset('WETH')
        daily_usd_prices = session.query(DailyUsdPrice) \
            .filter_by(asset_id=asset.id) \
            .filter(DailyUsdPrice.ts > date).order_by(DailyUsdPrice.ts.desc()).all()
    asset_prices = []
    for price in daily_usd_prices:
        asset_prices.append(
            AssetPrice(symbol=asset.symbol, ts=price.ts, period='day', price=price.price, numeraire='USD'))
    return asset_prices


def get_hour_prices_from_last_day(asset: Asset):
    with SessionContext() as session:
        hour_of_usd_prices = session.query(HourUsdPrice) \
            .filter_by(asset_id=asset.id) \
            .filter(HourUsdPrice.ts > asset.last_day_of_usd_price) \
            .order_by(HourUsdPrice.ts.desc()).all()

    asset_prices = []
    for price in hour_of_usd_prices:
        asset_prices.append(
            AssetPrice(symbol=asset.symbol, ts=price.ts, period='hour', price=price.price, numeraire='USD'))
    return asset_prices


def update_prices(asset_id: int, prices: List[AssetPrice]):
    with SessionContext() as session:
        for price in prices:
            if price.period == 'hour':
                asset_price_cls = HourUsdPrice
            elif price.period == 'day' and price.numeraire == 'USD':
                asset_price_cls = DailyUsdPrice
            elif price.period == 'day' and price.numeraire == 'WETH':
                asset_price_cls = DailyWethPrice
            else:
                ValueError('Период и/или Numeraire неопределен.')

            asset_price = asset_price_cls(asset_id=asset_id, price=price.price, ts=price.ts)
            session.add(asset_price)

        try:
            session.commit()
        except IntegrityError:
            session.rollback()
