import imp
from Helpers import yahoo_scraper
from Helpers import mail_log
from Helpers import yahoo_scraper


class UsdRates:

    __urlPkr = "https://finance.yahoo.com/quote/PKRUSD=X/"    
    def getPkrUsdRate(self):
        ys = yahoo_scraper.YahooScraper(self.__urlPkr)
        data = ys.GetCurrentData()
        return data["Price"]
