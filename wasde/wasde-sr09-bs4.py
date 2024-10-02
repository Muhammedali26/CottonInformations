
import requests
import datetime
from bs4 import BeautifulSoup
from sys import exc_info
import os
from Helpers import mail_log
import time

def generate_url():
    _url_prefix = "https://www.usda.gov/oce/commodity/wasde/"
    _url_suffix = "wasde" + datetime.datetime.today().strftime("%m%y")+ ".xml"
    _url = _url_prefix + _url_suffix
    return _url
  
def get_wasde_reports(url):  

    
    print(f"Scraping For: {url}")

    try :
        xml_data = requests.get(url).content        
        soup = BeautifulSoup(xml_data, 'html.parser')
       
    except Exception as e:
        e = str(e)
        print(e)
        raise
    try:
        res=soup.find(name="sr09")      
        month = soup.sr09.report['report_month'].split(" ")[0]
        year = soup.sr09.report['report_month'].split(" ")[1]       
    except Exception as e:
        print(e)
        raise


    return res,month,year

def get_target_data(res,month,year):
    _list = []
    att = res.find_all("m2_region_group")      
    
    for element in att:  
        _dict = {}
        region = str(element["region2"]).replace(" ","").replace('/','')
        region = ''.join((x for x in region if not x.isdigit()))
        _date = month+ "-" + year        
        date = datetime.datetime.strptime(_date, '%B-%Y')
        monthNumber = date.strftime("%m")
 
        _now = datetime.datetime.now()
        report_date = _now.strftime("%d-%m-%Y") 
        dayOfReport = _now.strftime("%d")
        dayOfReportStr = _now.strftime("%A")  
      
        report_id = date.strftime('%m%y')


        season1 = element.find("m2_year_group_collection")
        season2 = season1.find_all("m2_year_group")
        for col in season2:
            season = col["market_year2"]
            forecast1 = col.find("m2_month_group_collection")
            forecast2 = forecast1.find_all("m2_month_group")           
            for col1 in forecast2:

                _dict = {
                    "reportId":report_id,
                    "reportDate":report_date,
                    "year":int(year),
                    "month":int(monthNumber),
                    "monthString":month,                    
                    "day":dayOfReport,
                    "dayString":dayOfReportStr,
                    "season": season,
                    "region":region
                    }
                months = col1["forecast_month2"]
                _dict["forecastMonth"] = f"{months}"
                collection1 = col1.find("m2_attribute_group_collection")
                collection2 = collection1.find_all("m2_attribute_group")
                for col2 in collection2:
                    attribute = str(col2["attribute2"]).replace('\n', '').replace('\r', '').replace(' ','').replace('/','')
                    attribute = ''.join((x for x in attribute if not x.isdigit()))
                                       
                    if attribute in ["Output","TotalSupply","Trade","TotalUse","EndingStocks"]:
                        attribute = attribute[0].lower() + attribute[1:]  

                    values = col2.textbox47.cell["cell_value2"]
                    if "/" in values:
                        values = 999999
                    else:
                        values = values
                    if values == "NA":
                        values = 0.00
                    _dict[f"{attribute}"] = f"{values}"    
                _list.append(_dict) 
    return _list

def wasde():    
    url = generate_url()
    res,month,year =  get_wasde_reports(url)
    dataList = get_target_data(res,month,year)

    try:
        
        for data in dataList:
            print(data)

            
    except Exception as e:
        print(e)
        raise  
            

wasde()

   