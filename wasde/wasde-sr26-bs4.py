import requests
import datetime
from bs4 import BeautifulSoup
from sys import exc_info
import os
from Helpers import mail_log


def generate_url():
    _url_prefix = "https://www.usda.gov/oce/commodity/wasde/"
    _url_suffix = "wasde" + datetime.datetime.today().strftime("%m%y") + ".xml"
    _url = _url_prefix + _url_suffix
    return _url

def get_wasde_reports():

    url = generate_url()


  
    print(f"Scraping For: {url}")

    try:
        xml_data = requests.get(url).content
        soup = BeautifulSoup(xml_data, 'html.parser')
        # is_valid_link = True
    except Exception as e:
        e = str(e)
        mail_log.mail_log_document("Link hatalı!", e, os.path.basename(
            __file__), os.path.dirname(__file__))
        mail_log.log_error("wasde-sr26-bs4-log", exc_info()
                           [0], exc_info()[1], 'Link hatalı!')
        # is_valid_link = False
        raise
    try:
        res = soup.find(name="sr26")
        month = soup.sr26.report['report_month'].split(" ")[0]
        year = soup.sr26.report['report_month'].split(" ")[1]
    except Exception as e:
        print(e)
                           
        raise

    return res, month, year

  
def get_target_data_first(res, month, year):
    _list = []
    season = res.matrix3["region_header3"]
    att = res.find_all("m1_region_group2")

    for element in att:
        # print(len(att))
        _dict = {}

        collection = element.find("m1_attribute_group2_collection")
        collection2 = collection.find_all("m1_attribute_group2")
        region = str(element["region3"]).replace(" ", "").replace('/', '')
        region = ''.join((x for x in region if not x.isdigit()))
        _date = month + "-" + year
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

        _dict = {"reportId": report_id, 
                 "reportDate":report_date,
                 "year":int(year),
                 "month":int(monthNumber),
                 "monthString":month,                    
                 "day":dayOfReport,
                 "dayString":dayOfReportStr,
                 "season": season,
                 "region": region,                       
                 "place":0
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
        for col in collection2:
            attribute = str(col["attribute3"]).replace('\n', '').replace(
                '\r', '').replace(' ', '').replace('/', '')
            attribute = ''.join((x for x in attribute if not x.isdigit()))
            if attribute in ["BeginningStocks","Production","Imports","DomesticUse","Exports","Loss","EndingStocks"]:
                attribute = attribute[0].lower() + attribute[1:]  
            values = col.formatfiller2.cell["cell_value3"]
            if "/" in values:
                values = 999999
            else:
                values = values
            _dict[f"{attribute}"] = f"{values}"

        _list.append(_dict)

    return _list


def get_target_data_second(res, month, year):
    _list = []
    season = res.matrix4["region_header4"]
    att = res.find_all("m2_region_group2")

    for element in att:
        _dict = {}
        collection = element.find("m2_attribute_group2_collection")
        collection2 = collection.find_all("m2_attribute_group2")
        region = str(element["region4"]).replace(" ", "").replace('/', '')
        region = ''.join((x for x in region if not x.isdigit()))
        _date = month + "-" + year
        date = datetime.datetime.strptime(_date, '%B-%Y')
        report_id = date.strftime('%m%y')  

        monthNumber = date.strftime("%m")
        report_date = ""
        dayOfReport = ""
        dayOfReportStr = ""


        _wasdeDates = open("/opt/python-operations/scrapers/wasde/wasde_dates.txt", "r")        
        for rd in _wasdeDates:
            _rd =  datetime.datetime.strptime(rd.rstrip("\n"), '%b %d, %Y')
            if _rd.year == date.year and _rd.month == date.month:
                report_date = _rd.strftime("%d-%m-%Y")     
                dayOfReport = _rd.strftime("%d")
                dayOfReportStr = _rd.strftime("%A")  

        _dict = {"reportId": report_id, 
                 "reportDate":report_date,
                 "year":int(year),
                 "month":int(monthNumber),
                 "monthString":month,                    
                 "day":dayOfReport,
                 "dayString":dayOfReportStr,
                 "season": season,
                 "region": region,       
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


        for col in collection2:
            attribute = str(col["attribute4"]).replace('\n', '').replace(
                '\r', '').replace(' ', '').replace('/', '')
            attribute = ''.join((x for x in attribute if not x.isdigit()))
            if attribute in ["BeginningStocks","Production","Imports","DomesticUse","Exports","Loss","EndingStocks"]:
                attribute = attribute[0].lower() + attribute[1:]  
            values = col.formatfiller6.cell["cell_value4"]
            if "/" in values:
                values = 999999
            else:
                values = values
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
    res, month, year = get_wasde_reports()
    list1 = get_target_data_first(res, month, year)
    list2 = get_target_data_second(res, month, year)

    
    print("---------------------------------------")
    for data in list1:
        print(data)
    print("---------------------------------------")
    for data in list2:
        print(data)
    # if count ==2:
    #     break

wasde()

