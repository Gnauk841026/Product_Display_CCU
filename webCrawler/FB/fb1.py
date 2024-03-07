import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import mysql.connector
from bs4 import BeautifulSoup
import time

#Mariadb
config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'webcrawler',
    'raise_on_warnings': True
}

db = mysql.connector.connect(**config)
cursor = db.cursor()

# Login with Selenium
FACEBOOK_ID = "XXXX@gmail.com"
FACEBOOK_PW = "XXXXXX"
TARGET_URL = "https://www.facebook.com/groups/pythontw"

options = r'D:\IT\Python\chrome-win64\chromedriver.exe' #指定Webdriver網頁檔案路徑
service = Service(options)
options = webdriver.ChromeOptions()
options.add_argument("incognito")
# options.add_argument("headless")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options = options)
# driver.get("https://www.facebook.com")
driver.get(TARGET_URL)


# 获取邮箱和密码DOM元素
email =  driver.find_element(By.ID, "email")
password = driver.find_element(By.ID, "pass")
login = driver.find_element(By.NAME, "login")
# cssnm = ".x1i10hfl.xggy1nq.x1s07b3s.x1kdt53j.x1a2a7pz.xjbqb8w.x1n2xptk"
# email = driver.find_element(By.CSS_SELECTOR, f"{cssnm}[type='email']")
# password = driver.find_element(By.CSS_SELECTOR, f"{cssnm}[type='password']")
# login = driver.find_element(By.CSS_SELECTOR, "div[role='button'][aria-label='Accessible login button']")



email.send_keys(FACEBOOK_ID)
password.send_keys(FACEBOOK_PW)
login.submit()

time.sleep(3)

# Goto website
driver.get(TARGET_URL)
time.sleep(5)

button = driver.find_element(By.CSS_SELECTOR, "div[role='button'][aria-label='关闭']")
time.sleep(5)
button.click()
time.sleep(5)

# 滾動頁面
for x in range(1, 6):
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    titles = soup.findAll("div", {"class": "x1iorvi4 x1pi30zi x1l90r2v x1swvt13"})
    # Get source
    for title in titles:
    # print(title)
        posts = title.findAll('div', {'dir': 'auto'})
        for post in posts:
            with open("fbtitle.txt", "a", encoding="utf-8") as file:
                file.write(post.text+"\n")
                sql = "INSERT INTO fb (data) VALUES (%s)"
                val = (post.text[:255],) 
                cursor.execute(sql, val)
                db.commit()
