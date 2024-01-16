from datetime import datetime, timedelta
from Domain.Assets import AssetHourPrice, AssetPrice
from Repository import AssetRepository
from Service import FlipsideService, PriceServiceManager
import pandas as pd
from IPython.display import display
import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('application.log', mode='a')])


def main():
    #logging.info('process start at {0}'.format(str(datetime.datetime.now())))
    #PriceServiceManager.update_all_prices_by_symbol('OP')
    PriceServiceManager.update_all_prices()

main()
