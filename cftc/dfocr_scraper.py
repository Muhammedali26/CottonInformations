from Helpers import server_operations as Server
from Helpers import cftc_scraper
from Helpers import mail_log
import os
from sys import exc_info

url="https://www.cftc.gov/MarketReports/CommitmentsofTraders/HistoricalCompressed/index.htm"
try:
  data_dict,_date = cftc_scraper.getCurrentData("dfocr")
  table = "cftcDFOCR"
  print(data_dict)
except Exception as e:
    e = str(e)
    mail_log.mail_log_document("Veriyi çekerken hata alındı!",e,os.path.basename(__file__),os.path.dirname(__file__))
    mail_log.log_error("dfocr_log",exc_info()[0], exc_info()[1], 'Veriyi çekerken hata alındı.')
    raise

