from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import json

# 初始化 WebDriver
s = Service(r'D:\DATA\Python\chrome-win64\chromedriver.exe')
driver = webdriver.Chrome(service=s)

try:
    # 打開目標網頁
    driver.get("https://www.momoshop.com.tw/edm/cmmedm.jsp?lpn=O1K5FBOqsvN&n=1#posTag1")

    # 等待網頁加載完成
    time.sleep(5)  # 調整等待時間，確保網頁元素已經加載完畢

    # 抓取數據
    periods = [element.text for element in driver.find_elements(By.CLASS_NAME, "period")]
    item_names = [element.text for element in driver.find_elements(By.ID, "gdsBrand_1")]
    discounts = [element.text for element in driver.find_elements(By.CLASS_NAME, "discount")]
    prices = [element.text for element in driver.find_elements(By.CLASS_NAME, "price")]

    # 整理成 JSON 格式
data = []
for item in items:
    period = item.find_element(By.CLASS_NAME, "period").text
    item_name = item.find_element(By.CSS_SELECTOR, "#gdsBrand_1").text
    discount = item.find_element(By.CLASS_NAME, "discount").text
    price = item.find_element(By.CLASS_NAME, "price").text
    
    item_data = {
        "time": period,
        "item_name": item_name,
        "item_discount": discount,
        "item_price": price,
    }
    
    data.append(item_data)
