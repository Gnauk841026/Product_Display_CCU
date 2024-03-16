import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import json

TARGET_URL = "https://www.momoshop.com.tw/edm/cmmedm.jsp?lpn=O1K5FBOqsvN&n=1#posTag1"

# 设置WebDriver
options = webdriver.ChromeOptions()
options.add_argument("incognito")  # 无痕模式
# options.add_argument("headless")  # 无头模式

# 初始化WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.get(TARGET_URL)
time.sleep(5)  # 给页面加载留出时间

# 解析页面
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()  # 关闭浏览器

product_areas = soup.find_all(class_="product_Area")
products = []

for product in product_areas:
    # 直接访问每个元素的文本属性
    item_name = product.find(class_="brand2").text.strip() if product.find(class_="brand2") else "N/A"
    discount = product.find(class_="discAmt").text.strip() if product.find(class_="discAmt") else "N/A"
    price = product.find(class_="nPrice").text.strip() if product.find(class_="nPrice") else "N/A"

    product_info = {
        "item_name": item_name,
        "discount": discount,
        "price": price
    }

    products.append(product_info)

# 将列表转换成JSON格式
products_json = json.dumps(products, ensure_ascii=False, indent=4)

# 显示或保存JSON数据
print(products_json)



'''
    products = []

    for i in range(len(brand2_elements)):
        item_name = brand2_elements[i].text.strip() if i < len(brand2_elements) else None
        discount = discAmt_1_element[i].text.strip() if i < len(discAmt_1_element) else None
        price = nPrice_1_element[i].text.strip() if i < len(nPrice_1_element) else None

        product_info = {
        "item_name": item_name,
        "discount": discount,
        "price": price
    }

        products.append(product_info)
print(products)
'''