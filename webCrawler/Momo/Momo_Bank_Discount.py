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

TARGET_URL = "https://www.momoshop.com.tw/edm/cmmedm.jsp?lpn=O0Y2mh4ttZH&n=1&mdiv=1099900000-bt_0_249_01-bt_0_249_01_e1&ctype=B"
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
# }



options = r'D:\DATA\Python\chrome-win64\chromedriver.exe' #指定Webdriver網頁檔案路徑
service = Service(options)
options = webdriver.ChromeOptions()
options.add_argument("incognito")
# options.add_argument("headless")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options = options)
# driver.get("https://www.facebook.com")
driver.get(TARGET_URL)

soup = BeautifulSoup(driver.page_source, 'html.parser')
with open('Momo_Bank_Discount.txt', 'w', encoding='utf-8') as f:
    f.write(soup.prettify())

from bs4 import BeautifulSoup

# 假設html_content是您從文件或網頁中讀取的HTML內容
html_content = """
您的HTML內容
"""

# 找到所有銀行的項目
bank_items = soup.find_all('li', class_='bank-item')

for bank_item in bank_items:
    # 提取銀行的logo圖片URL
    logo_img_src = bank_item.find('div', class_='logo').img['src']
    # 從logo圖片URL中提取銀行代號
    bank_code = logo_img_src.split('/')[-1].split('_')[-1].split('.')[0]
    
    # 找到該銀行項目下的所有優惠信息
    promotions = bank_item.find_all('li', class_='info')
    for promo in promotions:
        promo_time = promo.find('small', class_='info-time').text.strip()
        promo_text = " ".join([t.text.strip() for t in promo.find_all(['span', 'b'], class_=['info-text-normal', 'info-text-strong'])])
        # 輸出銀行代號與相關優惠信息
        print(f"{bank_code}: {promo_time} - {promo_text}")


