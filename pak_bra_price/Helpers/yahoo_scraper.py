import requests
from bs4 import BeautifulSoup
import datetime
from Helpers import mail_log
from sys import exc_info



class YahooScraper:
    __url = None

    def __init__(self, url):
        self.__url = url

    def GetCurrentData(self):
      try:
           
        xml_data = requests.get(self.__url, headers={
    "User-Agent":"Custom"
  }).content ###headers={'User-Agent': 'Custom'} => olmadan 404 veriyor
        soup = BeautifulSoup(xml_data, 'html.parser')
        res = soup.find(id='quote-header-info').find_all("div")
        date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        contract = res[3].text
        currency = res[4].text
        price_col = res[12].find_all("fin-streamer")
        price = price_col[0].text
        change = price_col[1].text
        change_per = price_col[2].text.replace("(","").replace(")","")
        valid_time = res[15].text
        # print(market_open)


        dict_ = {
            'Date':date,
            'Contract': contract,
            'Currency': currency,
            'Price': float(price),
            'Change': change,
            'ChangePercentage': change_per,
            'ValidTime': valid_time
        }
        return dict_
        
      except Exception as e:
          e = str(e)
          mail_log.mail_log_url("Anlık veriyi alırken sorun oluştu!",e,self.__url)   
          mail_log.log_error(exc_info()[0], exc_info()[1], "Anlık veriyi alırken sorun oluştu!")

    def GetHistoricalData(self):

      all_in_one = []
      xml_data = requests.get(self.__url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'}).content ###headers={'User-Agent': 'Custom'} => olmadan 404 veriyor
      soup = BeautifulSoup(xml_data, 'html.parser')
      res = soup.find(id='Col1-1-HistoricalDataTable-Proxy').find("section").find("div",class_="Pb(10px) Ovx(a) W(100%)").find("table").find("tbody").find_all("tr")
      
      one = []
      for day in range(2): 
        date = res[day].find_all("td")[0].text
        open = res[day].find_all("td")[1].text
        high = res[day].find_all("td")[2].text
        low = res[day].find_all("td")[3].text
        close = res[day].find_all("td")[4].text
        adjClose = res[day].find_all("td")[5].text
        volume = res[day].find_all("td")[6].text


        dict_ = {
            
            'Date': date,
            'Open': open,
            'High': high,
            'Low': low,
            'Close': close,
            'Adj Close': adjClose,
            'Volume' : volume
        }
        one.append(dict_)
      all_in_one.append(one)

      return all_in_one