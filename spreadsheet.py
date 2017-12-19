import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint

scope = ["https://spreadsheets.google.com/feeds"]
creds = ServiceAccountCredentials.from_json_keyfile_name("client_secret.json", scope)
client = gspread.authorize(creds)

sheet = client.open("Task Tracker").sheet1

pp = pprint.PrettyPrinter()
result = sheet.get_all_records()
result2 = sheet.row_values(2)
result3 = sheet.col_values(1)
pp.pprint(result)
pp.pprint(result2)
pp.pprint(result3)