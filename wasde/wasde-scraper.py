import re
from unittest import result
import cloudscraper
from html.parser import HTMLParser
from bs4 import BeautifulSoup         
import xml.etree.ElementTree as ET
import urllib.request
import pandas as pd 
from datetime import datetime
import pymongo



"""
url generator: 
"""
def generate_url():
    _url_prefix = "https://www.usda.gov/oce/commodity/wasde/"
    _url_suffix = "wasde" + datetime.today().strftime("%m%y")+ ".xml"
    _url = _url_prefix + _url_suffix
    return _url


def get_wasde_report():

    _url = generate_url()
    is_valid_link = False
    is_valid_content = False
    res = None
    
    print(f"Scraping For: {_url}")
    try:     
        url_response = urllib.request.urlopen(_url)
        xml_content = str(url_response.read()).replace("\"     ","\"").replace("\"    ","\"").replace("\"   ","\"").replace("\"  ","\"").replace("\" ","\"")
        results=BeautifulSoup(xml_content, features="html.parser")
       
        res=results.find(name="sr17") 
        
        if res:
            is_valid_content = True
        else:
            is_valid_content = False
        is_valid_link = True
    except Exception as e:
        print(e)
        is_valid_link = False


    print(is_valid_link)
    print(is_valid_content)

    
    if is_valid_link and is_valid_content:   
        return res     

    else:
        return res


def get_target_data(res,month,year):
    
    _list = [] 
    att=re.findall(r'<attribute4(.+?)</attribute4>', str(res))

    for i in att:
        i=re.findall(r'="(.+?)">', str(i))   
        _dict = {}
        

        if month == 'May' or month == 'June' or month == 'July':
            season=i[3]
            field=i[0]
            value=str(i[4]).split("\"")[-1]
            _date = month+ "-" + year        
            date = datetime.strptime(_date, '%B-%Y')
            _dict= {"date":date,"year":year,"month":month,"season":season,"field":field,"value":value}
            _list.append(_dict)
        
        else:
            season=i[8]
            field=i[0]
            value=i[10]
            _date = month+ "-" + year        
            date = datetime.strptime(_date, '%B-%Y')
            _dict= {"date":date,"year":year,"month":month,"season":season,"field":field,"value":value}        
            _list.append(_dict)
        
    return _list

def printing():
    res = get_wasde_report()
    if res:
        month=str(re.findall(r'report_month=\"(.+?)\"', str(res))[0]).split(" ")[0]
        year=str(re.findall(r'report_month=\"(.+?)\"', str(res))[0]).split(" ")[1]
        _date = month+ "-" + year 
        date = datetime.strptime(_date, '%B-%Y')
        print(date)

        
        data = get_target_data(res,month,year)

        print(data)
            

printing()