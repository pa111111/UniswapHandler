import xml.etree.ElementTree as et

from Domain.CryptoCurrency import Cryptocurrency
from Service.FlipsideService import FlipsideService
from Service.GoogleSheetsRepository import GoogleSheetsRepository

root = et.parse('Config.xml').getroot()
flipside_api = root.find(".//items/item[@name='Flipside']/api").text
google_sheet = root.find(".//items/item[@name='Google_Sheets']/googlesheet").text
google_sheet_credential = root.find(".//items/item[@name='Google_Sheets']/credetials").text

#repo = AssetsRepo.AssetsRepository()
#result = repo.find_asset('WETH')
# repo.update_asset()
# result = repo.load_assets()

# print(result)

google_repo = GoogleSheetsRepository(google_sheet_credential)

currency_list = []
cr = Cryptocurrency('WETH', '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', 'ethereum', '0.00')
currency_list.append(cr)

repo = FlipsideService(flipside_api)
pd = repo.load_current_prices(currency_list)
print(pd)
