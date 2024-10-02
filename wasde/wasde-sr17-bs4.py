from dataclasses import field
import bs4

import requests
import datetime
from bs4 import BeautifulSoup
from sys import exc_info
import os
from Helpers import mail_log


def generate_url():
    _url_prefix = "https://www.usda.gov/oce/commodity/wasde/"
    _url_suffix = "wasde" + datetime.datetime.today().strftime("%m%y")+ ".xml"
    _url = _url_prefix + _url_suffix
    return _url


def get_wasde_reports():
  
    url = generate_url()
    print(f"Scraping For: {url}")

    try :
        xml_data = requests.get(url).content 
        soup = BeautifulSoup(xml_data, 'html.parser')
       
    except Exception as e:
        e = str(e)
        print(e)
       
        raise
    try:
        res=soup.find(name="sr17") 
        month = soup.sr17.report['report_month'].split(" ")[0]
        year = soup.sr17.report['report_month'].split(" ")[1]
    except Exception as e:
        print(e)
        raise

    return res,month,year



def get_target_data(res,month,year):
    _list = []
    _dict1 = {}
    _dict2 = {}
    _dict3 = {}
    _dict4 = {}

    _date = month+ "-" + year        
    date = datetime.datetime.strptime(_date, '%B-%Y')            
    report_id = date.strftime('%m%y')
    monthNumber = date.strftime("%m")
    report_date = ""
    dayOfReport = ""
    dayOfReportStr = ""

    # _wasdeDates = open("/opt/python-operations/scrapers/wasde/wasde_dates.txt", "r") 
    # ##report date değişecek mi 
    # for rd in _wasdeDates:
    #     _rd =  datetime.datetime.strptime(rd.rstrip("\n"), '%b %d, %Y')
    #     if _rd.year == date.year and _rd.month == date.month:
    #         report_date = _rd.strftime("%d-%m-%Y")     
    #         dayOfReport = _rd.strftime("%d")
    #         dayOfReportStr = _rd.strftime("%A")  
    
    _now = datetime.datetime.now()
    report_date = _now.strftime("%d-%m-%Y") 
    dayOfReport = _now.strftime("%d")
    dayOfReportStr = _now.strftime("%A")  
      
    
    _dict1 = {"reportId":report_id, "reportDate":report_date, "year":int(year), "month":int(monthNumber), "monthString":month, "day":dayOfReport, "dayString":dayOfReportStr}
    _dict2 = {"reportId":report_id, "reportDate":report_date, "year":int(year), "month":int(monthNumber), "monthString":month, "day":dayOfReport, "dayString":dayOfReportStr}
    _dict3 = {"reportId":report_id, "reportDate":report_date, "year":int(year), "month":int(monthNumber), "monthString":month, "day":dayOfReport, "dayString":dayOfReportStr}
    _dict4 = {"reportId":report_id, "reportDate":report_date, "year":int(year), "month":int(monthNumber), "monthString":month, "day":dayOfReport, "dayString":dayOfReportStr}

    att = res.find("attribute4")
    _season = att.find_all("m1_year_group")
    _dict1["season"] = _season[0]["market_year4"]
    _dict2["season"] = _season[1]["market_year4"]
    _dict3["season"] = _season[2]["market_year4"]
    _dict4["season"] = _season[3]["market_year4"]

    _forecastMonth = att.find_all("m1_month_group")
    _dict1["forecastMonth"] = _forecastMonth[0]["forecast_month4"]
    _dict2["forecastMonth"] = _forecastMonth[1]["forecast_month4"]
    _dict3["forecastMonth"] = _forecastMonth[2]["forecast_month4"]
    _dict4["forecastMonth"] = _forecastMonth[3]["forecast_month4"]

    atts = res.find_all("attribute4")  

    for element in atts:
        years = element.find_all("m1_year_group")
        for y in years:
            #col1
            if y["market_year4"] ==_dict1["season"] and y.find("m1_month_group")["forecast_month4"] == _dict1["forecastMonth"]:
                field = element["attribute4"].replace('/','')
                field = ''.join((x for x in field if not x.isdigit() and x != " ")).replace(",","").replace(".","")
                field = field[0].lower() + field[1:]
                value = str(y.find("cell")["cell_value4"])
                if value == "NA":
                        value = str(0.0)  

                                 

                if field != "avgFarmPrice":
                    if "/" in value:
                        value = 999999    
                    else: 
                        value = ''.join((x for x in value if x.isdigit() or x =="."))   
                    _dict1[field] = float(value)

                
                if field == "avgFarmPrice":
                    if "-" in value:
                        valueMin = value.split("-")[0]
                        valueMax = value.split("-")[1]
                        _dict1["avgFarmPriceMin"] = float(valueMin)
                        _dict1["avgFarmPriceMax"] = float(valueMax)                
                    else:
                        _dict1["avgFarmPriceMin"] = float(value)
                        _dict1["avgFarmPriceMax"] = float(value)  

            #col2
            if y["market_year4"] ==_dict2["season"] and y.find("m1_month_group")["forecast_month4"] == _dict2["forecastMonth"]:
                field = element["attribute4"].replace('/','')
                field = ''.join((x for x in field if not x.isdigit() and x != " ")).replace(",","").replace(".","")
                field = field[0].lower() + field[1:]
                value = str(y.find("cell")["cell_value4"])
                if value == "NA":
                    value = str(0.0)                 

                if field != "avgFarmPrice":
                    if "/" in value:
                        value = 999999 
                    else: 
                        value = ''.join((x for x in value if x.isdigit() or x ==".")) 
                    _dict2[field] = float(value)
                
                if field == "avgFarmPrice":
                    if "-" in value:
                        valueMin = value.split("-")[0]
                        valueMax = value.split("-")[1]
                        _dict2["avgFarmPriceMin"] = float(valueMin)
                        _dict2["avgFarmPriceMax"] = float(valueMax)                
                    else:
                        _dict2["avgFarmPriceMin"] = float(value)
                        _dict2["avgFarmPriceMax"] = float(value)
            
            #col3
            if y["market_year4"] ==_dict3["season"] and y.find("m1_month_group")["forecast_month4"] == _dict3["forecastMonth"]:
                field = element["attribute4"].replace('/','')
                field = ''.join((x for x in field if not x.isdigit() and x != " ")).replace(",","").replace(".","")
                field = field[0].lower() + field[1:]
                value = str(y.find("cell")["cell_value4"])
                if value == "NA":
                    value = str(0.0)                                

                if field != "avgFarmPrice":
                    if "/" in value:
                        value = 999999    
                    else: 
                        value = ''.join((x for x in value if x.isdigit() or x =="."))    
                        _dict3[field] = float(value)
                
                if field == "avgFarmPrice":
                    if "-" in value:
                        valueMin = value.split("-")[0]
                        valueMax = value.split("-")[1]
                        _dict3["avgFarmPriceMin"] = float(valueMin)
                        _dict3["avgFarmPriceMax"] = float(valueMax)                
                    else:
                        _dict3["avgFarmPriceMin"] = float(value)
                        _dict3["avgFarmPriceMax"] = float(value) 
            #col4
            if y["market_year4"] ==_dict4["season"] and y.find("m1_month_group")["forecast_month4"] == _dict4["forecastMonth"]:                
                field = element["attribute4"].replace('/','')
                field = ''.join((x for x in field if not x.isdigit() and x != " ")).replace(",","").replace(".","")
                field = field[0].lower() + field[1:]
                value = str(y.find("cell")["cell_value4"])                
                if value == "NA":
                    value = str(0.0)  

                        

                if field != "avgFarmPrice":
                    if "/" in value:
                        value = 999999    
                    else: 
                        value = ''.join((x for x in value if x.isdigit() or x ==".")) 
                    _dict4[field] = float(value)
                
                if field == "avgFarmPrice":
                    if "-" in value:
                        valueMin = value.split("-")[0]
                        valueMax = value.split("-")[1]
                        _dict4["avgFarmPriceMin"] = float(valueMin)
                        _dict4["avgFarmPriceMax"] = float(valueMax)                
                    else:
                        _dict4["avgFarmPriceMin"] = float(value)
                        _dict4["avgFarmPriceMax"] = float(value)
        
 
    _list.append(_dict1)
    _list.append(_dict2)
    _list.append(_dict3)
    _list.append(_dict4)        
    return _list

def wasde():

    res,month,year =  get_wasde_reports()
    dataList = get_target_data(res,month,year)


    try:
        
        for data in dataList:
            print(data)
            
    except Exception as e:
        print(e)
        raise  
wasde()















# server = Server.ServerOps()
# _linkList = []
# links = open("/opt/python-operations/scrapers/wasde/wasde_historical/links.txt", "r") 
# for link in links:
#     if len(link) >2:            
#         _linkList.append(link.rstrip("\n"))   

# for count,lnk in enumerate(_linkList):

#     res,month,year =  get_wasde_reports(url=lnk)     
#     dataList = get_target_data(res,month,year)
#     for data in dataList:

#         print('data ----' , data)
#         print(server.postWasdeSr17(data)) 
#     if count== 0:
        #break
        #print(server.postWasdeSr17(data))   
    

    #     for j in range(4):
    #         season = element.find_all("m1_year_group")[j]["market_year4"]            
    #         forecast_month =element.find_all("m1_year_group")[j].m1_month_group["forecast_month4"]


    #         _date = month+ "-" + year        
    #         date = datetime.datetime.strptime(_date, '%B-%Y')            
    #         report_id = date.strftime('%m%y')
    #         monthNumber = date.strftime("%m")
    #         report_date = ""
    #         _wasdeDates = open("/opt/python-operations/scrapers/wasde/wasde_dates.txt", "r")        
    #         for rd in _wasdeDates:
    #             _rd =  datetime.datetime.strptime(rd.rstrip("\n"), '%b %d, %Y')
    #             if _rd.year == date.year and _rd.month == date.month:
    #                 report_date = _rd.strftime("%d-%m-%Y")     
    #                 dayOfReport = _rd.strftime("%d")
    #                 dayOfReportStr = _rd.strftime("%A")  

            
    #         field = element["attribute4"].replace('/','')
    #         field = ''.join((x for x in field if not x.isdigit() and x != " ")).replace(",","").replace(".","")
    #         field = field[0].lower() + field[1:]   



    #         value =element.find_all("m1_year_group")[j].cell["cell_value4"]
    #         value = str(value) 



    #         if "/" in value:
    #             value = 999999


    #         if field != "avgFarmPrice":
    #             value = ''.join((x for x in value if x.isdigit() or x =="."))   
        
       



    #         if field == "avgFarmPrice":
    #             if "-" in value:
    #                 value1 = value.split("-")[0]
    #                 value2 = value.split("-")[1]
    #                 print("min - ", value1, "max - ", value2)
    #             else:

    #                 print(float(value))
    #         _dict= {"reportId":report_id,"reportDate":report_date,"year":year,"month":monthNumber, "monthString":month, "day":dayOfReport,"dayString":dayOfReportStr, "season":season,"field":field,"value":value,"forecastMonth":forecast_month}
    #         _list.append(_dict)
