from cmath import isnan
import datetime
from operator import le

import urllib.request
from bs4 import BeautifulSoup   


def getDateFromString(txt):    
    x = txt.strip(r"\n").replace(" ","").replace(".","").replace("and","").replace(",","")
    dateDayList = []
    l1 = []
    for i in range(len(x)-1):        
        if x[i].isnumeric() == True and x[i+1].isnumeric() == False:           
            l1.append(x[i])
            dateDayList.append(''.join(l1))        
            l1 = []    
        else:
            if i == (len(x)-2):
                l1.append(x[i])
                l1.append(x[i+1])
                dateDayList.append(''.join(l1))           
            l1.append(x[i])          
    return dateDayList

url_response = urllib.request.urlopen("https://www.usda.gov/oce/commodity/wasde")
xml_content = str(url_response.read()).replace("\"     ","\"").replace("\"    ","\"").replace("\"   ","\"").replace("\"  ","\"").replace("\" ","\"")
soup = BeautifulSoup(xml_content, features="html.parser")

_yearRaw1 = soup.find('div', {'class': 'paragraph'}).select("h3")[4].text
_yearString1 = _yearRaw1.split(" ")[0]
dates1 = soup.find('div', {'class': 'paragraph'}).select("p")[8].text
dateList1 = getDateFromString(dates1)
dateList1 = [date + f" { _yearString1 }" for date in dateList1]


_yearRaw2 = soup.find('div', {'class': 'paragraph'}).select("h3")[5].text
_yearString2 = _yearRaw2.split(" ")[0]
dates2 = soup.find('div', {'class': 'paragraph'}).select("p")[9].text
dateList2 = getDateFromString(dates2)
dateList2 = [date + f" { _yearString2 }" for date in dateList2]

dateListTotal = dateList1 + dateList2
 
 #-------------------------------------------


for date in dateListTotal:    
    _dateRaw = datetime.datetime.strptime(date, "%b%d %Y")
    _date = _dateRaw.strftime("%d-%m-%y")
    _cMounth = _dateRaw.month
    _cDay = _dateRaw.day
    _cYear = _dateRaw.year
    _reportId = "wasde" + _dateRaw.strftime("%m%y") 

    obj = {
            "title":"World Agricultural Supply and Demand Estimates",
            "cDate":_date,
            "cDay":_cDay,
            "cMounth":_cMounth,
            "cYear":_cYear,
            "cLink":None,
            "className":"bg-calendar-wasde",
            "reportId":_reportId
    }

print(obj)

    


    





    





