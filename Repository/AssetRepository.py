import pandas as pd
from typing import List
from Domain.Assets import Asset, AssetPriceProvider, BlockchainAsset, AssetHourPrice
from Repository.SessionContext import SessionContext
from Repository.db_uniswap import Blockchain, AssetHourPrice as AssetHourPrice_DB, \
    Asset as Asset_DB, AssetPriceProvider as AssetPriceProvider_DB


def get_asset(symbol, load_price_provider=True, load_last_hour_price=True):
    with SessionContext() as session:
        asset_db = session.query(Asset_DB).filter_by(symbol=symbol).first()

    price_provider = None
    if load_price_provider:
        price_provider = get_asset_price_provider(asset_db.symbol)[0]

    last_hour_price = None
    if load_last_hour_price:
        last_hour_price = get_last_hour_price(asset_db.symbol)

    asset = Asset(id=asset_db.id, symbol=asset_db.symbol, name=asset_db.name)
    asset.set_last_hour_price(last_hour_price)
    asset.set_price_provider(price_provider)
    return asset


def get_all_assets():
    with SessionContext() as session:
        assert_db_list = session.query(Asset_DB).all()
    asset_list = []
    for asset_db in assert_db_list:
        asset_list.append(Asset(asset_db.name, asset_db.symbol))
    return asset_list[0]


def get_asset_price_provider(symbol):
    with SessionContext() as session:
        providers = session.query(Asset_DB, AssetPriceProvider_DB) \
            .join(Asset_DB, Asset_DB.id == AssetPriceProvider_DB.asset_id).filter_by(symbol=symbol).all()
        providers_list = []
        for result in providers:
            providers_list.append(AssetPriceProvider(result.AssetPriceProvider.token_address,
                                                     result.AssetPriceProvider.price_provider,
                                                     result.AssetPriceProvider.blockchain.name))
    return providers_list


def get_all_hour_prices(symbol):
    with SessionContext() as session:
        prices = session.query(Asset_DB, AssetHourPrice_DB) \
            .join(Asset_DB, Asset_DB.id == AssetHourPrice_DB.asset_id).filter_by(symbol=symbol).all()

    prices_df = pd.DataFrame(columns=['Symbol', 'Hour', 'Price'])
    for price in prices:
        new_row = {'Symbol': price.Asset.symbol,
                   'Hour': price.AssetHourPrice.hour,
                   'Price': price.AssetHourPrice.usd_price}
        prices_df = pd.concat([prices_df, pd.DataFrame([new_row])], ignore_index=True)

    return prices_df


def get_last_hour_price(symbol) -> AssetHourPrice:
    with SessionContext() as session:
        last_hour_price = session.query(Asset_DB, AssetHourPrice_DB)\
            .join(Asset_DB, Asset_DB.id == AssetHourPrice_DB.asset_id)\
            .filter_by(symbol=symbol).order_by(AssetHourPrice_DB.hour.desc()).first()

    price = None
    if last_hour_price is not None:
        price = AssetHourPrice(last_hour_price.Asset.symbol, last_hour_price.AssetHourPrice.hour, last_hour_price.AssetHourPrice.usd_price)

    return price


def update_hour_prices(asset_id: int, prices: List[AssetHourPrice]):
    with SessionContext() as session:
        for hour_price in prices:
            asset_hour_price = AssetHourPrice_DB(asset_id=asset_id, usd_price=hour_price.price, hour=hour_price.hour)
            session.add(asset_hour_price)
        session.commit()




# def update_asset(self):
#    asset = self.session.query(Asset).filter_by(symbol='WETH').first()
#    asset.price_value = 1111
#    self.session.commit()
