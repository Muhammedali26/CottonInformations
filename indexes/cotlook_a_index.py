from Helpers import mail_log

import requests
import datetime
from bs4 import BeautifulSoup
from sys import exc_info
import time
import os


# now = time.time()

def get_cotlook():
    url="https://www.cotlook.com/"
    xml_data = requests.get(url).content 
    soup = BeautifulSoup(xml_data, 'html.parser')
    res=soup.find(id='aIndex').find_all("td")
    price = res[1].text
    change = res[2].text.replace("(","").replace(")","")
    date = res[3].text
    change = float(change)

    date= str(date[10:])
    date=date.split(" ")

    date[0]=date[0].removesuffix('st')
    date[0]=date[0].removesuffix('nd')
    date[0]=date[0].removesuffix('rd')
    date[0]=date[0].removesuffix('th')
    date[1]=date[1].removesuffix(',')
    date=date[0] + ' ' +date[1] + ' ' +date[2]
    date = datetime.datetime.strptime(date, '%d %b %Y').strftime("%d-%m-%Y")     

    dict_ = {
        'date': date,
        'price': float(price),
        'change': change,
        "priceUnit":"POUND/CENT($)"    
    }
    return dict_

try:
    dict1  = get_cotlook()
    dict2 = dict1.copy()

    dict2["title"] = "Cotlook A Index"
    dict2["priceChangeWay"] = "" 
    if float(dict2["change"]) > 0:
        dict2["priceChangeWay"] = "arrow-up"
    elif float(dict2["change"]) < 0:
        dict2["priceChangeWay"] = "arrow-down"

    dict2["priceInUsdPound"] = dict2["price"]
    dict2["priceChangeValue"] = float(dict2["change"])
    dict2["priceChangeValueInUsdPound"]  = dict2["priceChangeValue"]   

    dict2["priceChangePercent"] = str(round(100 *  dict2["priceChangeValue"] / dict2["price"], 2)) + "%" 
    dict2["priceCurrency"] ="USD"
    dict2["previousClose"] = ""
    dict2["bidAskRatio"]= ""
    dict2["daysRange"] = ""
    dict2["realTime"] = dict2["date"]
    _dict_real_time = {"token":"", "userrid":"", "table":"" ,"datas":dict2 }  


except Exception as e:
    e = str(e)
    print(e)
    raise
# print(time.time() - now)

print(_dict_real_time)
