from datetime import timedelta
import pandas as pd
from Domain.Assets import AssetPrice, Asset
from Repository import AssetRepository
from Service import FlipsideService
import datetime
import logging


def update_all_prices():
    logging.info('update_all_prices start at {0}'.format(str(datetime.datetime.now())))
    asset_list = AssetRepository.get_asset_list_for_load_prices()
    # Первым шагом обновляем цены WETH
    for asset in [a for a in asset_list if a.is_weth()]:
        update_hour_usd_prices(asset)
        update_daily_usd_prices(asset)
        update_daily_weth_prices(asset)
    # Далее обновляем цены остальных активов
    for asset in [a for a in asset_list if not a.is_weth()]:
        update_hour_usd_prices(asset)
        update_daily_usd_prices(asset)
        update_daily_weth_prices(asset)
    logging.info('update_all_prices end at {0}'.format(str(datetime.datetime.now())))


def update_all_prices_by_symbol(symbol):
    logging.info('update_all_prices_by_symbol start at {0}'.format(str(datetime.datetime.now())))
    asset = AssetRepository.get_asset(symbol)
    update_hour_usd_prices(asset)
    update_daily_usd_prices(asset)
    update_daily_weth_prices(asset)
    logging.info('update_all_prices_by_symbol end at {0}'.format(str(datetime.datetime.now())))


def update_hour_usd_prices(asset: Asset):
    if asset.price_provider.price_provider_name == 'flipside':
        prices = FlipsideService.load_hour_usd_prices_from_last_hour(asset)
        AssetRepository.update_prices(asset.id, prices)
    else:
        raise ValueError('Price provider not found!')

    message = "{0} hourly usd prices is up to date".format(asset.symbol)
    if len(prices) != 0:
        message = "{0} hourly usd prices uploaded from {1} to {2}".format(asset.symbol,
                                                                          str(prices[-1].ts),
                                                                          str(prices[0].ts))

    logging.info(message)


def update_daily_usd_prices(asset: Asset):
    # забираем часовые цены, которые больше чем крайняя дневная цена актива
    prices = AssetRepository.get_hour_prices_from_last_day(asset)
    # приводим лист объектов к DataFrame
    df = pd.DataFrame([asset_price.__dict__ for asset_price in prices])
    # за цену закрытия цены берем период 0:00:00 следующего дня (фактически цены открытия след дня)
    # фильтруем цены 0:00:00 и вычитаем 1 день, чтобы получилась не цена открытия след дня, а цена закрытия текущего дня
    # сортируем по возрастанию и удаляем 1 строку, чтобы не получить дублирование строк с последней записью дневной цены в таблице.
    selected_rows = df[(df['ts'].dt.time == pd.to_datetime('0:00:00').time()) & (df['symbol'] == asset.symbol)]
    selected_rows.loc[:, 'ts'] = selected_rows['ts'].dt.date - timedelta(1)
    selected_rows.loc[:, 'period'] = 'day'
    selected_rows = selected_rows.sort_values(by='ts', ascending=True)
    selected_rows = selected_rows.iloc[1:, :]
    # приводим получившийся DataFrame к List[AssetPrice] для последующего сохранения в БД
    converted_asset_prices = [AssetPrice(**row) for row in selected_rows.to_dict(orient='records')]
    # сохраняем daily prices в БД
    AssetRepository.update_prices(asset.id, converted_asset_prices)

    message = "{0} daily usd prices is up to date".format(asset.symbol)
    if not selected_rows.empty:
        message = "{0} daily usd prices uploaded from {1} to {2}".format(asset.symbol,
                                                                         str(selected_rows['ts'].iloc[0]),
                                                                         str(selected_rows['ts'].iloc[-1]))
    logging.info(message)


def update_daily_weth_prices(asset):
    # Загружаем дневные цены актива, которые после последней даты дневной WETH цены актива
    daily_usd_prices = AssetRepository.get_daily_usd_prices_from_last_weth_price_day(asset)
    # Конвертируем в DataFrame
    daily_usd_prices_df = pd.DataFrame([asset_price.__dict__ for asset_price in daily_usd_prices])
    # Загружаем дневные цены WETH, которые идут после последней даты дневной WETH цены актива
    daily_weth_prices = AssetRepository.get_daily_usd_prices_of_weth_from_date(asset.last_day_of_weth_price)
    # Конвертируем в DataFrame
    daily_weth_prices_df = pd.DataFrame([asset_price.__dict__ for asset_price in daily_weth_prices])
    # Если не пустой DataFrame с дневными ценами WETH, которые идут после последней даты дневной WETH цены актива
    if not daily_weth_prices_df.empty:
        # Связываем датафреймы по дате
        merged_df = pd.merge(daily_usd_prices_df, daily_weth_prices_df, on=['ts'])
        # формируем итоговый датафрейм с рассчетной ценой актива в WETH
        df_daily_asset_weth_price = pd.DataFrame({
            'symbol': merged_df['symbol_x'],
            'ts': merged_df['ts'],
            'period': merged_df['period_x'],
            'price': merged_df['price_x'] / merged_df['price_y'],
            'numeraire': merged_df['symbol_y']})

        # сортируем итоговый актив по возрастанию даты
        df_daily_asset_weth_price = df_daily_asset_weth_price.sort_values(by='ts', ascending=True)
        # конвертируем датафрейм в List[AssetPrice]
        daily_asset_weth_price = [AssetPrice(**row) for row in df_daily_asset_weth_price.to_dict(orient='records')]
        # сохраняем daily prices в БД
        AssetRepository.update_prices(asset.id, daily_asset_weth_price)

        message = "{0} daily weth prices uploaded from {1} to {2}".format(asset.symbol,
                                                                          str(df_daily_asset_weth_price['ts'].iloc[0]),
                                                                          str(df_daily_asset_weth_price['ts'].iloc[-1]))
    else:
        message = "{0} daily weth prices is up to date".format(asset.symbol)

    logging.info(message)
