
import datetime
from playwright.sync_api import sync_playwright
from datetime import datetime

from sys import exc_info
import os
_dict = {}


try:
    with sync_playwright() as p:
        url = "https://www.cepea.esalq.usp.br/en/indicator/cotton.aspx"
        row = 1
        date_xpath = f'//*[@id="imagenet-indicador2"]/tbody/tr[{row}]/td[1]'
        price_xpath = f'//*[@id="imagenet-indicador2"]/tbody/tr[{row}]/td[2]'
        daily_xpath = f'//*[@id="imagenet-indicador2"]/tbody/tr[{row}]/td[3]'
        monthly_xpath = f'//*[@id="imagenet-indicador2"]/tbody/tr[{row}]/td[4]'

        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        
        date = page.locator(date_xpath).inner_text()
        price = page.locator(price_xpath).inner_text()
        price = float(price)
        daily = page.locator(daily_xpath).inner_text().rstrip("%")
        daily = float(daily)
        monthly = page.locator(monthly_xpath).inner_text()

        date = date.replace("/"," ")
        _dict = {"date":datetime.strptime(date, '%m %d %Y').strftime("%d-%m-%Y"),"price":price,"priceUnit":"POUND/CENT($)", "change":daily}

        print(_dict)

        _dict2= _dict.copy()
        _dict2["title"] = "CEPEA/ESALQ Cotton Price Index"

        _dict2["priceChangeWay"] = ""
        if float(_dict2["change"]) > 0:
                _dict2["priceChangeWay"] = "arrow-up"
        elif float(_dict2["change"]) < 0:
                _dict2["priceChangeWay"] = "arrow-down"   

        cr =  100 + _dict2["change"]
        pv = _dict2["price"] / cr
        _dict2["previousClose"] =round(pv * 100,2) 

        _dict2["priceChangeValue"]  = round(_dict2["price"] - _dict2["previousClose"],2) 
        _dict2["priceChangePercent"] = str(_dict2["change"]) + "%"
        _dict2["priceCurrency"] ="USD" 
        _dict2["bidAskRatio"]= ""
        _dict2["daysRange"] = ""
        _dict2["realTime"] = _dict2["date"]
     
        _dict2["priceInUsdPound"] = _dict2["price"]        
        _dict2["priceChangeValueInUsdPound"] = _dict2["priceChangeValue"]      
        _dict_real_time = {"token":"", "userrid":"", "table":"" ,"datas":_dict2 } 


        print(_dict_real_time)
        browser.close()
    
except Exception as e:
    e = str(e)  
    print(e)
    raise



