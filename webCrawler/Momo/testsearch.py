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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

target_item = ["iphone","衛生紙"]
result_list = []
# #DB設定
def insert_sql(list):
    db = pymysql.connect(host="localhost",
                     user="root",
                     password="root",
                     database="momo")
    cursor = db.cursor()
    for item in list:
        item_key = item['item']
        name = item['name']
        price = item['price']
        sale = item['sale']
        state = item['state']
        sql = "INSERT INTO items (item, name,price,sale,state) VALUES (%s, %s, %s, %s, %s)"
        val = (item_key, name, price, sale, state)
        cursor.execute(sql, val)
        db.commit()

def save_to_json_file(data, file_name_prefix='Items'):
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

for item_n in target_item:
    TARGET_URL = "https://www.momoshop.com.tw/main/Main.jsp"
    options = r'D:\IT\Python\chrome-win64\chromedriver.exe' #指定Webdriver網頁檔案路徑
    service = Service(options)
    options = webdriver.ChromeOptions()
    # options.add_argument("incognito")
    options.add_argument("headless")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options = options)
    driver.get(TARGET_URL)
    searchbox = driver.find_element(By.NAME, "keyword")
    search_button = driver.find_element(By.CLASS_NAME, "inputbtn")
    searchbox.send_keys(item_n)
    search_button.click()

    try:
        # 等待最終頁按鈕加載
        last_page_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[@title="最終頁"]'))
        )
        total_pages = int(last_page_button.get_attribute('pageidx'))
        print(f"總頁數為: {total_pages}")

        current_page = 1
        while current_page <= total_pages:
            print(f"正在處理第 {current_page} 頁")

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            
            clearfix_elements = soup.find_all(class_='clearfix')
            # 遍历每个 clearfix 元素，然后获取其中的所有 li 元素
            for clearfix in clearfix_elements:
                li_elements = clearfix.find_all('li')
                for li in li_elements:
                    item_name = li.find(class_='prdName').text
                    price1 = li.find(class_='price')
                    price2 = price1.find('b').text
                    sale = li.find(class_="totalSales goodsTotalSales").text
                    icon_areas = li.find(class_="iconArea")
                    states = []
                    for icon_area in icon_areas:
                        # 对于每个 iconArea，抓取其下所有子节点的文本并存入临时列表
                        state_texts = icon_area.text
                        # 将所有文本添加到 states 列表中
                        states.append(state_texts)
                        result_string = '\t'.join(states)
                        result = {
                            "item":item_n,
                            "name":item_name,
                            "price":price2,
                            "sale": sale,
                            "state": result_string,
                    }
                    result_list.append(result)

            if current_page < total_pages:
                # 若不是最後一頁，則尋找並點擊下一頁按鈕
                next_page_button_xpath = f'//a[@pageidx="{current_page + 1}"]'
                next_page_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, next_page_button_xpath))
                )
                next_page_button.click()  # 點擊翻頁按鈕
                sleep(2)  # 稍等2秒，等待頁面加載

            current_page += 1

    except Exception as e:
        print(f"處理過程中發生錯誤: {e}")
    finally:
        # 完成後關閉瀏覽器
        driver.quit()

save_to_json_file(result_list)
insert_sql(result_list)





