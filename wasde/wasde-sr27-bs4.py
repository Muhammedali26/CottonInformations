from builtins import print
import requests
import datetime
from bs4 import BeautifulSoup
from sys import exc_info
import os
from Helpers import mail_log
from Helpers import server_operations as Server

def generate_url():
    _url_prefix = "https://www.usda.gov/oce/commodity/wasde/"
    _url_suffix = "wasde" + datetime.datetime.today().strftime("%m%y")+ ".xml"
    _url = _url_prefix + _url_suffix
    return _url


def get_wasde_reports():
  
    url = generate_url()
    # url = link#"https://www.usda.gov/oce/commodity/wasde/wasde0922.xml"
    # is_valid_link = False
    # is_valid_content = False
    # res = None

    print(f"Scraping For: {url}")

    try :
        xml_data = requests.get(url).content 
        soup = BeautifulSoup(xml_data, 'html.parser')
        # is_valid_link = True
    except Exception as e:
        e = str(e)
        print(e)
        # is_valid_link = False
        raise
    try:
        res=soup.find(name="sr27") 
        month = soup.sr27.report['report_month'].split(" ")[0]
        year = soup.sr27.report['report_month'].split(" ")[1]
    except Exception as e:
        # mail_log.mail_log_document("İçerik yanlış!",e,os.path.basename(__file__),os.path.dirname(__file__))
        mail_log.log_error("wasde-sr27-bs4-log",exc_info()[0], exc_info()[1], 'Rapor henüz yayınlanmadı!') 
        raise

    return res,month,year



def get_target_data(res,month,year):
    _list = []
    season = res.matrix2["region_header2"]
    att = res.find_all("m1_region_group2")   
    
    
    for element in att:
        _dict = {}        
        region = str(element["region2"]).replace(" ","").replace('/','')
        region = ''.join((x for x in region if not x.isdigit()))
        _date = month+ "-" + year        
        date = datetime.datetime.strptime(_date, '%B-%Y')
        report_id = date.strftime('%m%y')
        monthNumber = date.strftime("%m")
        report_date = ""
        dayOfReport = ""
        dayOfReportStr = ""

        _now = datetime.datetime.now()
        report_date = _now.strftime("%d-%m-%Y") 
        dayOfReport = _now.strftime("%d")
        dayOfReportStr = _now.strftime("%A") 

        # _wasdeDates = open("/opt/python-operations/scrapers/wasde/wasde_dates.txt", "r")        
        # for rd in _wasdeDates:
        #     _rd =  datetime.datetime.strptime(rd.rstrip("\n"), '%b %d, %Y')
        #     if _rd.year == date.year and _rd.month == date.month:
        #         report_date = _rd.strftime("%d-%m-%Y")     
        #         dayOfReport = _rd.strftime("%d")
        #         dayOfReportStr = _rd.strftime("%A")  




        forecast_month = element.find("m1_month_group2_collection")
        forecast_month1 = forecast_month.find_all("m1_month_group2")

  
        for index,col1 in enumerate(forecast_month1):  

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

         #region ----- set parent and place
            if _dict["region"] == "World":            
                _dict["place"] = 1000
            if _dict["region"] == "WorldLessChina":               
                _dict["place"] = 1100
            if _dict["region"] == "UnitedStates":   
                _dict["place"] = 2000
            if _dict["region"] == "TotalForeign":          
                _dict["place"] = 3000
            if _dict["region"] == "MajorExporters":      
                _dict["place"] = 3100
            if _dict["region"] == "CentralAsia":           
                _dict["place"] = 3110
            if _dict["region"] == "Afr.Fr.Zone":            
                _dict["place"] = 3120
            if _dict["region"] == "S.Hemis." or _dict["region"] == "S.Hemis" :            
                _dict["place"] = 3130
            if _dict["region"] == "Australia":            
                _dict["place"] = 3131
            if _dict["region"] == "Brazil":        
                _dict["place"] = 3132
            if _dict["region"] == "India":        
                _dict["place"] = 3140
            if _dict["region"] == "MajorImporters":         
                _dict["place"] = 3200
            if _dict["region"] == "Mexico":         
                _dict["place"] = 3210
            if _dict["region"] == "China":         
                _dict["place"] = 3220
            if _dict["region"] == "EuropeanUnion" or _dict["region"] == "EU-":         
                _dict["place"] = 3230
            if _dict["region"] == "Turkey":        
                _dict["place"] = 3240
            if _dict["region"] == "Pakistan":        
                _dict["place"] = 3250
            if _dict["region"] == "Indonesia":         
                _dict["place"] = 3260
            if _dict["region"] == "Thailand":        
                _dict["place"] = 3270
            if _dict["region"] == "Bangladesh":         
                _dict["place"] = 3280
            if _dict["region"] == "Vietnam":         
                _dict["place"] = 3290        
        
        #endregion

            months = col1["forecast_month2"]
            _dict["forecastMonth"] = f"{months}"  
            collection2 = col1.find("m1_attribute_group2_collection")
            collection3 = collection2.find_all("m1_attribute_group2")
            for col in collection3:
                attribute = str(col["attribute2"]).replace('\n', '').replace('\r', '').replace(' ','').replace('/','')
                attribute = ''.join((x for x in attribute if not x.isdigit()))

                if attribute in ["BeginningStocks","Production","Imports","DomesticUse","Exports","Loss","EndingStocks"]:
                    attribute = attribute[0].lower() + attribute[1:]  
                values = col.formatfiller5.cell["cell_value2"]
                if "/" in values:
                    values = 999999
                else:
                    values = values
                if values == "NA":
                    values = 0.0 
                _dict[f"{attribute}"] = f"{values}" 

    
            _list.append(_dict)     
    return _list


def wasde():
    

    # _linkList =[]
    # links = open("/opt/python-operations/scrapers/wasde/wasde_historical/links.txt", "r") 
    # for link in links:
    #     if len(link) >2:
    #         _linkList.append(link.rstrip("\n"))  
   
    # for count,lnk in enumerate(_linkList):

    res, month,year = get_wasde_reports()
    list1 = get_target_data(res,month,year)
    for data in list1:   
        print(data)

    # if count == 2:
    #     break
        
            

wasde()