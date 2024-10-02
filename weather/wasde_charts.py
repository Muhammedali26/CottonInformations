from datetime import datetime
import json
import time
import urllib.request
from bs4 import BeautifulSoup      
import re

from datetime import timedelta

url = "https://ipad.fas.usda.gov/cropexplorer/cropview/Default.aspx"

def get_cotton_url(url):
  url_response = urllib.request.urlopen(url)
  xml_content = str(url_response.read()).replace("\"     ","\"").replace("\"    ","\"").replace("\"   ","\"").replace("\"  ","\"").replace("\" ","\"")
  soup= BeautifulSoup(xml_content, features="html.parser")
  cotton_url = soup.find('div', {'id': 'divCommodity'}).find('div', {'class': 'col-md-2'}).find('div', {'class': 'thumbnail'}).find(href=True)

  return cotton_url["href"]


def get_country_url():## aynı anda ndvi urlleri
  pages = []
  country_url = []
  cotton_url = get_cotton_url(url)
  pages.append("https://ipad.fas.usda.gov/cropexplorer/cropview/" + cotton_url)
  pages.append("https://ipad.fas.usda.gov/cropexplorer/cropview/" + cotton_url[0:19] + "startrow=11&" + cotton_url[19:])
  pages.append("https://ipad.fas.usda.gov/cropexplorer/cropview/" + cotton_url[0:19] + "startrow=21&" + cotton_url[19:])
  pages.append("https://ipad.fas.usda.gov/cropexplorer/cropview/" + cotton_url[0:19] + "startrow=31&" + cotton_url[19:])

  # for page in pages:#40 ülkenin hepsi alınmak istendiğinde açılması gerek bu haliyle ilk 10 ülke alınıyor
  url_response = urllib.request.urlopen(pages[0])
  xml_content = str(url_response.read()).replace("\"     ","\"").replace("\"    ","\"").replace("\"   ","\"").replace("\"  ","\"").replace("\" ","\"")
  soup = BeautifulSoup(xml_content, features="html.parser")

  list_len = len(soup.find('table', {'class': 'WhiteBackgroundColor'}).table.find_all('tr'))
  for tds in range(3,list_len):
    country_url.append("https://ipad.fas.usda.gov/cropexplorer/cropview/" + soup.find('table', {'class': 'WhiteBackgroundColor'}).table.find_all('tr')[tds].find_all('td')[2].find(href=True)["href"].replace("®","&reg"))

  return country_url


def get_precipitation_url(country_url):
  
  # del country_url[-2]#40 ülkeyide çektiğimizde sondan 2. ülkede veri yok o yüzden del yapıyoruz
  precipitation_urls = []
  for page in country_url:
    url_response = urllib.request.urlopen(page)
    xml_content = str(url_response.read()).replace("\"     ","\"").replace("\"    ","\"").replace("\"   ","\"").replace("\"  ","\"").replace("\" ","\"")
    soup = BeautifulSoup(xml_content, features="html.parser")
    precipitation_urls.append("https://ipad.fas.usda.gov/cropexplorer/cropview/" + soup.find(id="nav").find("a", string="Moving Precipitation and Cumulative Precipitation (Pentad)",href=True)["href"])

  return precipitation_urls


def get_temperature_url(country_url):
  
  # del country_url[-2]#40 ülkeyide çektiğimizde sondan 2. ülkede veri yok o yüzden del yapıyoruz
  temperature_urls = []
  for page in country_url:
    url_response = urllib.request.urlopen(page)
    xml_content = str(url_response.read()).replace("\"     ","\"").replace("\"    ","\"").replace("\"   ","\"").replace("\"  ","\"").replace("\" ","\"")
    soup = BeautifulSoup(xml_content, features="html.parser")
    temperature_urls.append("https://ipad.fas.usda.gov/cropexplorer/cropview/" + soup.find(id="nav").find("a", string="Average Temperature",href=True)["href"])

  return temperature_urls


def get_soil_moisture_url(country_url):
  
  # del country_url[-2]#40 ülkeyide çektiğimizde sondan 2. ülkede veri yok o yüzden del yapıyoruz
  soil_moisture_urls = []
  for page in country_url:
    url_response = urllib.request.urlopen(page)
    xml_content = str(url_response.read()).replace("\"     ","\"").replace("\"    ","\"").replace("\"   ","\"").replace("\"  ","\"").replace("\" ","\"")
    soup = BeautifulSoup(xml_content, features="html.parser")
    soil_moisture_urls.append("https://ipad.fas.usda.gov/cropexplorer/cropview/" + soup.find(id="nav").find("a", string="Soil Moisture (CPC Leaky Bucket)",href=True)["href"])

  return soil_moisture_urls


def scraper(url):   
    url_response = urllib.request.urlopen(url)
    xml_content = str(url_response.read()).replace("\"     ","\"").replace("\"    ","\"").replace("\"   ","\"").replace("\"  ","\"").replace("\" ","\"")
    soup= BeautifulSoup(xml_content, features="html.parser")

    area_count = len(soup.find(id="CountryChartDiv").find_all("ul")[0].find_all("li")[4].find("map").find_all("area"))
    date = soup.find(id="CountryChartDiv").find_all("ul")[0].find_all("li")[4].find("img")["onclick"]
    ndvi_infos1 = soup.find(id="CountryChartDiv").find_all("ul")[0].find_all("li")[4].find("map").find_all("area")[int(area_count/2)-2]["title"]
    country = soup.find(id="breadCrumb").find("tbody").find("tr").find_all("td")[0].find("span").text
    image = soup.find(id="CountryChartDiv").find_all("ul")[0].find_all("li")[0].find_all("ul")[0].find_all("li")[0].a.img["src"]

    start_date_string = re.findall(r'startdate=(.+?)&', date)[0]
    end_date_string = re.findall(r'enddate=(.+?)&', date)[0]

    start_date = datetime.strptime(start_date_string, "%m/%d/%Y")

    end_date = datetime.strptime(end_date_string, "%m/%d/%Y")

    first_year = start_date.year
    last_year = end_date.year
    areas = soup.find(id="CountryChartDiv").find_all("ul")[0].find_all("li")[4].find("map").find_all("area")
    dates = []
    values = []
    for area in areas:
        if(area["shape"] == "circle"):
            _date = area["title"].replace(r"\t","").split(r"\n")[1].split(":")[1].replace(" ","")
            _value = area["title"].replace(r"\t","").split(r"\n")[2].split(":")[1].replace(" ","")
            dates.append(_date)
            values.append(_value)
        
    dates = dates[::-1]
    values = values[::-1]

    return dates,values,first_year,last_year,country,image

def season_lists_temp(dates,values,first_year,last_year):
    graphicDatas = []

    dataListNormal = {}
    dataListNormal["dates"] = []
    dataListNormal["values"] = []
    
    dataListCurrent = {}
    dataListCurrent["dates"] = []
    dataListCurrent["values"] = []
    

    dataListNext = {}
    dataListNext["dates"] = []
    dataListNext["values"] = []       

    if first_year == last_year:
        dataListNormal["season"] = "normal"
        dataListCurrent["season"] = str(first_year -1)
        dataListNext["season"] = str(first_year )

    else:
        dataListNormal["season"] = "normal"
        dataListCurrent["season"] = str(first_year - 1) + "/" + str(first_year) 
        dataListNext["season"] = str(first_year) + "/" + str(last_year)


    first_indexes = []
    control_date = []



    j = 999999
    ##3 farklı değer kümesi var bunları ayırmak için tarihler aynı veya belirli farklarla yazılmış olmalı o yüzden ilk kontrol yapılıyor. ayrıca tarihin yılı verilmediği için bazı yıl geçişleri olabiliyor o da ikinci kontrol ile sağlanıyor
    ##normalden current a geçerken ilk tarih geri gidiyorsa geri gidilenden başla ve bir adım atla ki bir sonraki adımda da yeniden seçilmesin
    for i in range(int(len(dates))):
        control_date.append(datetime.strptime(dates[i] + "2022" , "%b%d%Y"))
        if j == i:
          continue
        else:
          if 0 <= abs((control_date[i] - control_date[0]).days) < 6:
              first_indexes.append(i)
              if 0 > (control_date[i] - control_date[0]).days:
                j = i+1 
    print(first_indexes)



    

    year = first_year
    for i in range(0,first_indexes[1]):
        if i != 0:
            if dates[i-1][:3] == "Dec" and dates[i][:3] == "Jan":
                year = last_year
        dateStr = dates[i][:3] + "-"+dates[i][3:] + "-" + str(year)

        date = datetime.strptime(dateStr,"%b-%d-%Y").strftime("%d-%m-%Y")        
        dataListNormal["dates"].append(date)
        dataListNormal["values"].append(values[i])




    year = first_year
    for i in range(first_indexes[1],first_indexes[2]):
        if i != 0:
            if dates[i-1][:3] == "Dec" and dates[i][:3] == "Jan":
                year = last_year
        dateStr = dates[i][:3] + "-"+dates[i][3:] + "-" + str(year)

        date = datetime.strptime(dateStr,"%b-%d-%Y").strftime("%d-%m-%Y")        
        dataListCurrent["dates"].append(date)
        dataListCurrent["values"].append(values[i])

        
    
    year = first_year
    for i in range(first_indexes[2],len(dates)):
        if i != 0:
            if dates[i-1][:3] == "Dec" and dates[i][:3] == "Jan":
                year = last_year
        dateStr = dates[i][:3] + "-"+dates[i][3:] + "-" + str(year)
        
        date = datetime.strptime(dateStr,"%b-%d-%Y").strftime("%d-%m-%Y")        
        dataListNext["dates"].append(date)
        dataListNext["values"].append(values[i])


    graphicDatas.append(dataListNormal)   
    graphicDatas.append(dataListCurrent)   
    graphicDatas.append(dataListNext)


    return graphicDatas

def season_lists(dates,values,first_year,last_year):
    graphicDatas = []

    dataListNormal = {}
    dataListNormal["dates"] = []
    dataListNormal["values"] = []
    
    dataListCurrent = {}
    dataListCurrent["dates"] = []
    dataListCurrent["values"] = []
    

    dataListNext = {}
    dataListNext["dates"] = []
    dataListNext["values"] = []       

    if first_year == last_year:
        dataListNormal["season"] = "normal"
        dataListCurrent["season"] = str(first_year -1)
        dataListNext["season"] = str(first_year )

    else:
        dataListNormal["season"] = "normal"
        dataListCurrent["season"] = str(first_year - 1) + "/" + str(first_year) 
        dataListNext["season"] = str(first_year) + "/" + str(last_year)


    first_indexes = []


    ##3 farklı değer kümesi var bunları ayırmak için tarihler aynı veya belirli farklarla yazılmış olmalı o yüzden ilk kontrol yapılıyor
    for i in range(int(len(dates))):
        
        if dates[0] == dates[i]:
            first_indexes.append(i)
        
    print(first_indexes)


    

    year = first_year
    for i in range(0,first_indexes[1]):
        if i != 0:
            if dates[i-1][:3] == "Dec" and dates[i][:3] == "Jan":
                year = last_year
        dateStr = dates[i][:3] + "-"+dates[i][3:] + "-" + str(year)

        date = datetime.strptime(dateStr,"%b-%d-%Y").strftime("%d-%m-%Y")        
        dataListNormal["dates"].append(date)
        dataListNormal["values"].append(values[i])




    year = first_year
    for i in range(first_indexes[1],first_indexes[2]):
        if i != 0:
            if dates[i-1][:3] == "Dec" and dates[i][:3] == "Jan":
                year = last_year
        dateStr = dates[i][:3] + "-"+dates[i][3:] + "-" + str(year)

        date = datetime.strptime(dateStr,"%b-%d-%Y").strftime("%d-%m-%Y")        
        dataListCurrent["dates"].append(date)
        dataListCurrent["values"].append(values[i])

        
    
    year = first_year
    for i in range(first_indexes[2],len(dates)):
        if i != 0:
            if dates[i-1][:3] == "Dec" and dates[i][:3] == "Jan":
                year = last_year
        dateStr = dates[i][:3] + "-"+dates[i][3:] + "-" + str(year)
        
        date = datetime.strptime(dateStr,"%b-%d-%Y").strftime("%d-%m-%Y")        
        dataListNext["dates"].append(date)
        dataListNext["values"].append(values[i])


    graphicDatas.append(dataListNormal)   
    graphicDatas.append(dataListCurrent)   
    graphicDatas.append(dataListNext)


    return graphicDatas   

def printing():
    

    
    ndvi_url = get_country_url()
    precipitation_url = get_precipitation_url(ndvi_url)
    soil_moisture_url = get_soil_moisture_url(ndvi_url)
    temperature_url = get_temperature_url(ndvi_url)
    all_url = [ndvi_url,precipitation_url,soil_moisture_url]
    # url = "https://ipad.fas.usda.gov/cropexplorer/cropview/comm_chartview.aspx?fattributeid=1&cropid=2631000&startrow=1&sel_year=2022&ftypeid=47&regionid=che&cntryid=CHN&nationalGraph=False"
    #url = "https://ipad.fas.usda.gov/cropexplorer/cropview/comm_chartview.aspx?ftypeid=47&fattributeid=1&fctypeid=19&fcattributeid=10&regionid=br&cntryid=BRA&cropid=2631000&nationalgraph=False&sel_year=2022&startrow=1"
    ##Ndvi
    for url in temperature_url:
            dates,values,first_year,last_year,country,image = scraper(url)
            gDatas =  season_lists_temp(dates,values,first_year,last_year)

            
            data = {
                    "region":country,
                    "type":"Temperature",
                    "tcpgif":image,
                    "datas":gDatas
                }  
            # print(data)

            # with open("/opt/python-operations/scrapers/weather/dict.json", "a") as outfile:
            #     json.dump(data, outfile)

            print(data,country) 
            


    for count,urls in enumerate(all_url):
        for url in urls:
            dates,values,first_year,last_year,country,image = scraper(url)
            gDatas =  season_lists(dates,values,first_year,last_year)

            if 0<=count<=9 :
                data = {
                    "region":country,
                    "type":"NDVI",
                    "tcpgif":image,
                    "datas":gDatas
                }
            if 10<=count<=19 :
                data = {
                    "region":country,
                    "type":"Precipitation",
                    "tcpgif":image,
                    "datas":gDatas
                }
            if 20<=count <=29:
                data = {
                    "region":country,
                    "type":"SoilMoisture",
                    "tcpgif":image,
                    "datas":gDatas
                }
            
                
            
            # with open("/opt/python-operations/scrapers/weather/dict.json", "a") as outfile:
            #     json.dump(data, outfile)
                
            # print(data)

            print(data,country)


start_time = time.time()
printing()

print("First function--- %s seconds ---" % (time.time() - start_time))


# {'region': 'Brazil', 'type': 'Soil Moisture', 'tcpgif': 'https://ipad.fas.usda.gov/rssiws/images/br/br_bra000_gadm_2631000.gif',
# 'datas': [{'dates':
# ['05-03-2022', '13-03-2022', '21-03-2022', '29-03-2022', '06-04-2022', '14-04-2022', '22-04-2022', '30-04-2022', '08-05-2022', '16-05-2022', '24-05-2022', '01-06-2022', '09-06-2022', '17-06-2022', '25-06-2022', '03-07-2022', '11-07-2022', '19-07-2022', '27-07-2022', '04-08-2022', '12-08-2022', '20-08-2022', '28-08-2022', '05-09-2022', '13-09-2022', '21-09-2022', '29-09-2022', '07-10-2022', '15-10-2022', '23-10-2022', '31-10-2022'],
# 'values': ['0.31', '0.33', '0.35', '0.37', '0.39', '0.43', '0.45', '0.47', '0.48', '0.48', '0.46', '0.43', '0.4', '0.41', '0.44', '0.5', '0.56', '0.62', '0.67', '0.69', '0.69', '0.69', '0.69', '0.66', '0.63', '0.57', '0.52', '0.45', '0.41', '0.37', '0.36'],
# 'season': 'normal'},
# {'dates': ['05-03-2022', '13-03-2022', '21-03-2022', '29-03-2022', '06-04-2022', '14-04-2022', '22-04-2022', '30-04-2022', '08-05-2022', '16-05-2022', '24-05-2022', '01-06-2022', '09-06-2022', '17-06-2022', '25-06-2022', '03-07-2022', '11-07-2022', '19-07-2022', '27-07-2022', '04-08-2022', '12-08-2022', '20-08-2022', '28-08-2022', '05-09-2022', '13-09-2022', '21-09-2022', '29-09-2022', '07-10-2022', '15-10-2022', '23-10-2022', '31-10-2022'],
# 'values': ['0.42', '0.37', '0.38', '0.42', '0.43', '0.5', '0.49', '0.51', '0.52', '0.52', '0.5', '0.46', '0.45', '0.43', '0.49', '0.53', '0.58', '0.66', '0.71', '0.72', '0.72', '0.72', '0.69', '0.69', '0.66', '0.6', '0.54', '0.51', '0.43', '0.41', '0.42'],
# 'season': '2022'}, {'dates': ['05-03-2022', '13-03-2022', '21-03-2022', '29-03-2022', '06-04-2022', '14-04-2022', '22-04-2022', '30-04-2022', '08-05-2022', '16-05-2022', '24-05-2022', '01-06-2022', '09-06-2022', '17-06-2022', '25-06-2022', '03-07-2022', '11-07-2022', '19-07-2022', '27-07-2022', '04-08-2022', '12-08-2022', '20-08-2022', '28-08-2022', '05-09-2022', '13-09-2022', '21-09-2022', '29-09-2022', '07-10-2022', '15-10-2022', '31-10-2022'],
# 'values': ['0.34', '0.38', '0.35', '0.42', '0.45', '0.48', '0.5', '0.53', '0.52', '0.52', '0.49', '0.46', '0.43', '0.45', '0.46', '0.56', '0.59', '0.65', '0.67', '0.69', '0.69', '0.68', '0.68', '0.65', '0.62', '0.55', '0.49', '0.47', '0.41', '0.38'], 'season': '2023'}]}
