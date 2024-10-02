from Helpers import mail_log

import requests
import datetime
from bs4 import BeautifulSoup
from sys import exc_info
import time
import os
from forex_python.converter import CurrencyRates
from Helpers import usd_rates_current as rt

rates = rt.UsdRates()
c = CurrencyRates()

# for num in reversed(range(154)):
url="http://english.china-cotton.org/index/ccindex_more?per_page=" + "0"
xml_data = requests.get(url).content 
soup = BeautifulSoup(xml_data, 'html.parser')
rows=soup.find("table",{"class":"p2"}).find_all("tr")


def parse_and_save_row(row):
    # for index, row in enumerate(rows[::-1][1:-2]):
    cells = row.find_all("td")
    dateRaw =  datetime.datetime.strptime(cells[0].get_text(), '%Y-%m-%d')
    dateStr = dateRaw.strftime("%d-%m-%Y")
    priceA = cells[1].get_text()
    changeA = cells[2].get_text()
    priceB = cells[3].get_text()
    changeB = cells[4].get_text()

    dict2 = {}
    dict2 = {"date":dateStr,"priceA":priceA,"priceB":priceB,"changeA":changeA,"changeB":changeB,"priceUnit":"MT/CNY"}
    dict2Daily = {"date":dateStr,"priceA":priceA,"priceB":priceB,"changeA":changeA,"changeB":changeB,"priceUnit":"MT/CNY"}
    _dict_real_time = {"token":"", "userrid":"", "table":"" ,"datas":dict2}

    dict2["title"] = "CHINA Cotton A Index"
    dict2["priceChangeWay"] = "" 
    if float(dict2["changeA"]) > 0:
        dict2["priceChangeWay"] = "arrow-up"
    elif float(dict2["changeA"]) < 0:
        dict2["priceChangeWay"] = "arrow-down"
    dict2["price"] = float(dict2["priceA"])
    dict2["priceChangeValue"] = float(dict2["changeA"])
    dict2["priceChangePercent"] = str(round(100 *  dict2["priceChangeValue"] / dict2["price"], 2)) + "%" 
    dict2["priceCurrency"] ="CNY"
    dict2["previousClose"] = ""
    dict2["bidAskRatio"]= ""
    dict2["daysRange"] = ""
    dict2["realTime"] = dict2["date"]

    rate = 0
    try:
        rate = c.get_rate('CNY', 'USD',dateRaw)  
    except Exception as e:
        print('Cny hatası')
        # rate = rates.getCnyUsdRate()

    _convertRatio = 100*rate/2204.62
    dict2["zceToIceRatio"] = _convertRatio
    dict2["priceInUsdPound"] = _convertRatio * dict2["price"]
    dict2["priceChangeValueInUsdPound"] = rate * dict2["priceChangeValue"]      
    _dict_real_time = {"token":"", "userrid":"", "table":"" ,"datas":dict2}

    print(dict2Daily)
    print(_dict_real_time)


# parse_and_save_row(rows[3])
parse_and_save_row(rows[2])
