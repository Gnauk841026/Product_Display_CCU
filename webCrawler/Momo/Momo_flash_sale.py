import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pymysql
from bs4 import BeautifulSoup
import time
import pandas as pd
import json


TARGET_URL = "https://www.momoshop.com.tw/edm/cmmedm.jsp?lpn=O1K5FBOqsvN&n=1#posTag1"

options = r'D:\DATA\Python\chrome-win64\chromedriver.exe' #指定Webdriver網頁檔案路徑
service = Service(options)
options = webdriver.ChromeOptions()
options.add_argument("incognito")
# options.add_argument("headless")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options = options)
driver.get(TARGET_URL)

soup = BeautifulSoup(driver.page_source, 'html.parser')
with open('Momo_Bank_Discount.txt', 'w', encoding='utf-8') as f:
    f.write(soup.prettify())

start_time_element = soup.find_all('div', class_ = 'period')
for i in start_time_element:
    cat_element =i.find('span').text.strip()
    starttime , endtime =cat_element.split('~')
    print(starttime)
    print(endtime)