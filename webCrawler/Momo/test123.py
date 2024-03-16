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

with open('Momo_slash.txt', 'w', encoding='utf-8') as f:
    f.write(soup.prettify())
product_area = soup.find_all(class_="product_Area")

for product in product_area:
    print(product.text.strip())
    # 透過class和id提取元素
    # period_elements = product_area.find_all(class_="period")
    brand2_elements = product.find(class_="brand2")
    discAmt_1_element = product.find(id="discAmt_1")
    nPrice_1_element = product.find(id="nPrice_1")
    # 打印提取的元素
    # 對於多個'period'元素
print(brand2_elements.text.strip())



