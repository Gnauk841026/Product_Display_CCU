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
from datetime import datetime

# #DB設定
def insert_sql(list):
    db = pymysql.connect(host="localhost",
                     user="root",
                     password="root",
                     database="momo")
    cursor = db.cursor()
    for item in list:
        bank_name = item['bank']
        bank_id = item['bank_id']
        strdate = item['strdate']
        enddate = item['enddate']
        event = item['event']
        sql = "INSERT INTO discount (bank, bank_id,strdate,enddate,event) VALUES (%s, %s, %s, %s, %s)"
        val = (bank_name, bank_id, strdate, enddate, event)
        cursor.execute(sql, val)
        db.commit()

        

# 自動化命名檔案名稱
def generate_filename(prefix="momo_bank_discount"):
    # 獲取當前的日期和時間
    now = datetime.now()
    # 格式化日期時間為 'YYYYMMDDHHMM' 的格式
    date_time_format = now.strftime("%Y%m%d%H%M")
    # 組合檔案名稱
    filename = f"{prefix}_{date_time_format}.json"
    return filename


TARGET_URL = "https://www.momoshop.com.tw/edm/cmmedm.jsp?lpn=O0Y2mh4ttZH&n=1&mdiv=1099900000-bt_0_249_01-bt_0_249_01_e1&ctype=B"

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

banks_df = pd.read_csv('taiwan_banks.csv')
banks_mapping = dict(zip(banks_df['銀行代碼'].astype(str), banks_df['銀行名稱']))
results = []

for bank_item in bank_items:
    logo_img_src = bank_item.find('div', class_='logo').img['src']
    bank_code = logo_img_src.split('/')[-1].split('_')[-1].split('.')[0]
    bank_name = banks_mapping.get(bank_code, "未知銀行")  # 用對應表取得銀行名稱
    
    promotions = bank_item.find_all('li', class_='info')
    for promo in promotions:
        promo_time = promo.find('small', class_='info-time').text.strip()
        strday , endday = promo_time.split('-')
        promo_text = " ".join([t.text.strip() for t in promo.find_all(['span', 'b'], class_=['info-text-normal', 'info-text-strong'])])
        
        # 將信息儲存到字典中，然後加入到結果列表
        result = {
            "bank": bank_name,
            "bank_id": bank_code,
            "strdate": strday,
            "enddate": endday,
            "event": promo_text
        }
        results.append(result)

# 將結果列表轉換成 JSON 字串，然後列印或儲存
results_json = json.dumps(results, ensure_ascii=False, indent=2)
filename = generate_filename()
with open(filename, 'w', encoding='utf-8') as file:
    file.write(results_json)
    
insert_sql(results)