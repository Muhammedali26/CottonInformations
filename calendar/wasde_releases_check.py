from playwright.sync_api import sync_playwright
from playwright.sync_api import expect
from datetime import datetime
import re



with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    
    page.goto(f"https://usda.library.cornell.edu/concern/publications/3t945q76s?locale=en#release-items")
    for k in range(3):
      _clink = page.locator(f'//*[@id="release-items"]/tr[{k+1}]/td[2]/div/a[1]').get_attribute("href")
      _dateRawString = page.locator(f'//*[@id="release-items"]/tr[{k+1}]/td[1]').inner_text()
      _dateRaw = datetime.strptime(_dateRawString,"%b %d, %Y")
      _date = _dateRaw.strftime("%d-%m-%Y")
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
      "cLink":_clink,
      "className":"bg-soft-warning",
      "reportId":_reportId
      }
      
      print(obj)