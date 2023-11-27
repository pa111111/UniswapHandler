from Domain.CryptoCurrency import Cryptocurrency
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials


# https://www.pylenin.com/blogs/connecting-python-to-google-sheets/
class GoogleSheetsRepository:
    def __init__(self, credentials):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        # credentials to the account
        cred = Credentials.from_service_account_file(credentials, scopes=scope)
        # authorize the clientsheet
        self.client = gspread.authorize(cred)

    def load_assets_list(self, google_sheet):
        google_sheet = self.client.open(google_sheet)
        assets_worksheet = google_sheet.worksheet("Assets")
        assets_df = pd.DataFrame(assets_worksheet.get_all_records())

        currency_list = []
        for index, row in assets_df.iterrows():
            currency_list.append(Cryptocurrency(symbol=row['Symbol'], address=row['Address'], blockchain=row['Blockchain']))

        return currency_list
