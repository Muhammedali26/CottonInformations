import os
from sys import exc_info

from Helpers import cftc_scraper
from Helpers import mail_log

try:
  data_dict,_date = cftc_scraper.getCurrentData("focr")
  table = "cftcFOCR"
  
except Exception as e:
    e = str(e)
    mail_log.mail_log_document("Veriyi çekerken hata alındı!",e,os.path.basename(__file__),os.path.dirname(__file__))
    mail_log.log_error("focr_log",exc_info()[0], exc_info()[1], 'Veriyi çekerken hata alındı.')
    raise

