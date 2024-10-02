import requests
from bs4 import BeautifulSoup   
import pandas as pd
import requests, zipfile, io, os
import json
from datetime import datetime



def getCurrentData(title):
  url="https://www.cftc.gov/MarketReports/CommitmentsofTraders/HistoricalCompressed/index.htm"

  title_no = 0
  title = title.lower()
  if title == "dfor":##Disaggregated Futures Only Reports
    title_no = 0
  elif title == "dfocr":##Disaggregated Futures-and-Options Combined Reports
    title_no = 1
  elif title == "for":##Futures Only Reports
    title_no = 4
  elif title == "focr":##Futures-and-Options Combined Reports
    title_no = 5
  elif title == "cits":##Commodity Index Trader Supplement
    title_no = 6


  page = requests.get(url)
  soup= BeautifulSoup(page.content, features="html.parser")
  df = pd.DataFrame()

  zip_url = soup.find(id= "content-container").find_all("table")[title_no].tbody.find_all("tr")[0].find_all("td")[0].find_all("a",href=True)[1]["href"]
  zip_url = "https://www.cftc.gov" + zip_url
  
  r = requests.get(zip_url, stream=True)
  z = zipfile.ZipFile(io.BytesIO(r.content))
  filename = [i.filename for i in z.infolist()][0]
  z.extractall("/opt/python-operations/scrapers/cftc/Helpers/temp_data")
  all_data = pd.read_excel(f"/opt/python-operations/scrapers/cftc/Helpers/temp_data/{filename}")
  os.remove(f"/opt/python-operations/scrapers/cftc/Helpers/temp_data/{filename}")
  df = pd.concat([df,all_data[all_data.Market_and_Exchange_Names.str.contains("COTTON")]])
  # print(df.shape)

  out = df.head(1).to_json(orient='records')
  data = json.loads(out)
  data = data[0]
  _dict2 = {}
  for items in data:
    _dict2[items.replace(" ","")] = data[items]


  if title == "dfor" or title == "dfocr":
    _dict2.pop("Market_and_Exchange_Names")
    _dict2.pop("Report_Date_as_MM_DD_YYYY")
    _dict2.pop("CFTC_Contract_Market_Code")
    _dict2.pop("CFTC_Market_Code")
    _dict2.pop("CFTC_Region_Code")
    _dict2.pop("CFTC_Commodity_Code")
    _dict2.pop("FutOnly_or_Combined")
    _dict2.pop("CFTC_SubGroup_Code")
    
  if title == "for" or title == "focr" or title == "cits":
    _dict2.pop("Market_and_Exchange_Names")
    _dict2.pop("Report_Date_as_MM_DD_YYYY")
    _dict2.pop("CFTC_Contract_Market_Code")
    _dict2.pop("CFTC_Market_Code")
    _dict2.pop("CFTC_Region_Code")
    _dict2.pop("CFTC_Commodity_Code")


  dateRaw = _dict2.pop("As_of_Date_In_Form_YYMMDD")

  _date = datetime.strptime(str(dateRaw),"%y%m%d")
  _dict2["date"]= _date.strftime("%d-%m-%Y")

  # with open("sample.json", "w") as outfile:
  #   json.dump(data, outfile)

  data_dict = {"data":_dict2}

  return data_dict,_dict2["date"]