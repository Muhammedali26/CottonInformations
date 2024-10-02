import re
import datetime
from sqlite3 import DataError
from unittest import result
import cloudscraper
from html.parser import HTMLParser
from bs4 import BeautifulSoup         
import xml.etree.ElementTree as ET
import urllib.request
import pandas as pd

f = open("C:\\Users\\muham\\Desktop\\hey\\scrapers\\wasde\\wasde_historical\\pages.txt", "r")

l = open("C:\\Users\\muham\\Desktop\\hey\\scrapers\\wasde\\wasde_historical\\links.txt", "w")

for sayfa in f:
    url_response = urllib.request.urlopen(sayfa)
    xml_content = str(url_response.read()).replace("\"     ","\"").replace("\"    ","\"").replace("\"   ","\"").replace("\"  ","\"").replace("\" ","\"")
    results=BeautifulSoup(xml_content, features="html.parser")
    
    links = re.findall(r'href=\"(.+?)\"', str(results))
    for link in links:
        if str(link).split(".")[-1] == "xml":
            l.writelines(link + "\n") 

f.close()
l.close()
