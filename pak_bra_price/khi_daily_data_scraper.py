
import datetime
from playwright.sync_api import sync_playwright
from datetime import datetime

from sys import exc_info
import os
from forex_python.converter import CurrencyRates
import math
c = CurrencyRates()

from Helpers import usd_rates_current as rt


rates = rt.UsdRates()
c = CurrencyRates()

_dict = {}
_dict_real_time = {}

try:
    with sync_playwright() as p:
        url = "https://www.khistocks.com/commodity/karachi-cotton-rates.html"
        # önce table data buttonuna basılmalı
        table_data_xpath = '//*[@id="tabledata"]'
        kg_button_xpath = '//*[@id="s2id_myindex"]'
        search_area_xpath = '//*[@id="s2id_autogen2_search"]'
        search_area_input = '40 (KG)'
        
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        # çalışıyor
        page.click(table_data_xpath)
        # çalışıyor
        page.click(kg_button_xpath)
        # çalışıyor
        page.click(search_area_xpath)
        # çalışıyor
        page.fill(search_area_xpath, search_area_input)
        # arada bekleme süresi koyulmazsa çalışmıyor
        page.keyboard.press('Enter')
        page.wait_for_timeout(500)

        row = 1
        date = page.locator(f'//*[@id="mytable"]/tbody/tr[{row}]/td[{1}]').inner_text()
        ex_gin = page.locator(f'//*[@id="mytable"]/tbody/tr[{row}]/td[{2}]').inner_text()
        upcountry = page.locator(f'//*[@id="mytable"]/tbody/tr[{row}]/td[{3}]').inner_text()
        spot_rate = page.locator(f'//*[@id="mytable"]/tbody/tr[{row}]/td[{4}]').inner_text()

        row2 = row + 1
        pdate = page.locator(f'//*[@id="mytable"]/tbody/tr[{row2}]/td[{1}]').inner_text()
        pex_gin = page.locator(f'//*[@id="mytable"]/tbody/tr[{row2}]/td[{2}]').inner_text()
        pupcountry = page.locator(f'//*[@id="mytable"]/tbody/tr[{row2}]/td[{3}]').inner_text()
        pspot_rate = page.locator(f'//*[@id="mytable"]/tbody/tr[{row2}]/td[{4}]').inner_text()

        date = date.replace(",", "")

        __date = datetime.strptime(date, '%b %d %Y')
        _date = __date.strftime("%d-%m-%Y")
        _price = float(ex_gin.replace(",",""))
        _upcountry = float(upcountry)   
        _spotrate = float(spot_rate.replace(",",""))
        _pprice = float(pex_gin.replace(",",""))
        _pupcountry = float(pupcountry)   
        _pspotrate = float(pspot_rate.replace(",",""))


        _dict = {"date":_date,"exGinPrice":_price,"upCountry":_upcountry,"spotRate":_spotrate,"priceUnit":"40KG/PKR"}
        _dict2 = _dict.copy()

        rate = 0
        try:
            rate = c.get_rate('PKR', 'USD')  
        except Exception as e:
            rate = rates.getPkrUsdRate()

        

        _dict2["title"] = "Karachi Cotton Rates"
        _dict2["price"] = _spotrate
        _dict2["priceChangeValue"] = _spotrate - _pspotrate
        _dict2["priceChangePercent"] = str(round(((_dict2["priceChangeValue"] / _pspotrate) * 100),2) ) + "%"
        _dict2["priceChangeWay"] = ""

        if float(_dict2["priceChangeValue"]) > 0:
            _dict2["priceChangeWay"] = "arrow-up"
        elif float(_dict2["priceChangeValue"]) < 0:
                _dict2["priceChangeWay"] = "arrow-down"  

        _convertRatio = 100*rate/88.1849
        _dict2["khiToIceRatio"] = _convertRatio
        _dict2["priceInUsdPound"] = _convertRatio * _dict2["price"]
        _dict2["priceChangeValueInUsdPound"] = rate * _dict2["priceChangeValue"]



        _dict2["priceCurrency"] ="PKR"        
        _dict2["bidAskRatio"]= ""
        _dict2["daysRange"] = ""
        _dict2["realTime"] = _dict2["date"]         
    

        
        
        _dict_real_time = {"token":"", "userrid":"", "table":"" ,"datas":_dict2}

        print(_dict_real_time)
      
except Exception as e:
    e = str(e)
    print(e)
    raise
    



  