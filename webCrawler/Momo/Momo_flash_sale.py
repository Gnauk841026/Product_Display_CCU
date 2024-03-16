import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pymysql
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import json

# #DB設定
def insert_sql(list):
    db = pymysql.connect(host="localhost",
                     user="root",
                     password="root",
                     database="momo")
    cursor = db.cursor()
    for item in list:
        period = item['period']
        date = item['date']
        time = item['time']
        title = item['title']
        name = item['name']
        discount = item['discount']
        price = item['price']
        sql = "INSERT INTO flesh (period, date,time,title,name,discount,price) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (period, date, time, title, name, discount, price)
        cursor.execute(sql, val)
        db.commit()

def save_to_json_file(data, file_name_prefix='flash_sale'):
    """將陣列輸出成 JSON 檔案。
    
    Args:
        data (list): 要轉換成 JSON 的陣列。
        file_name_prefix (str): 檔案名稱前綴。
    """
    # 生成檔案名稱，格式為 '前綴_年月日時分.json'
    file_name = f"{file_name_prefix}_{datetime.now().strftime('%Y%m%d%H%M')}.json"
    
    # 將陣列轉換成 JSON 字串並寫入檔案
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
    print(f"檔案已儲存為 {file_name}")

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
    
slash_mental = soup.find_all('div' ,class_="MENTAL")

result_list = []

for mental in slash_mental:
    period = mental.find(class_="period")
    slash_time = period.find('span').text.strip()
    date1,_= slash_time.split('~')
    date , periodtime = date1.split(' ')
    box1 = mental.find_all(class_="box1")
    for box in box1:
        slash_title = box.find(class_="brand").text.strip()
        slash_detail = box.find(class_="brand2").text.strip()
        slash_price = box.find(id="nPrice_1").text.strip()
        slash_discount = box.find(id="discAmt_1").text.strip()

        result = {
            "period":slash_time,
            "date":date,
            "time": periodtime,
            "title": slash_title,
            "name": slash_detail,
            "discount": slash_discount,
            "price": slash_price
        }
        result_list.append(result)
save_to_json_file(result_list)
insert_sql(result_list)