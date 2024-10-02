from Helpers import yahoo_scraper
from Helpers import mail_log



class UsdRates:
    __urlCny = "https://finance.yahoo.com/quote/CNYUSD=X/"
    __urlInr = "https://finance.yahoo.com/quote/INRUSD=X/"

    def getCnyUsdRate(self):    
        ys = yahoo_scraper.YahooScraper(self.__urlCny)
        data = ys.GetCurrentData()
        return data["Price"]

    def getInrUsdRate(self):
        ys = yahoo_scraper.YahooScraper(self.__urlInr)
        data = ys.GetCurrentData()
        return data["Price"]
