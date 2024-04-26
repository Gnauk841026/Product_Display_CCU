import datetime
import pymysql
import pandas as pd

def load_test_plan() -> list:
    """會讀取plan/general.csv內的資料，並回傳成list。

    Returns:
        list:將plan/general.csv內的資料逐句讀取，並回傳成list。
    """
    with open("plan/general.csv", "r", encoding = "utf-8") as file:
        test_url = file.readlines()
    return test_url

def filename() -> str :
    """
    生成帶有當前日期和時間的文件名字符串。

    Returns:
        str: 返回帶有當前日期和時間的文件名，report-yyyy-mm-dd-hh-mm-ss.csv。
    """
    filename = datetime.datetime.now().strftime("report-"+"%Y-%m-%d-%H-%M-%S"+".csv")
    return filename

def generate_report(list_test_report:list) -> str :
    """
    將輸入的list轉換為csv格式的文件，並保存在report目錄下。
    
    Args:
        list_test_report (list): 列表中，每個元素都是一個字典，分別與 'item'、'response' 和 'screenshot' 三個鍵值對應。
    """
    with open(f"report/{filename()}", "w", encoding = "utf-8") as file:
        file.write("item,response,screenshot\n")
        for item in list_test_report:
            file.write(f"{item['item']},{item['response']},{item['screenshot']}\n")
    print("測試報告產生完成")        
    
def send2sql(list_test_report:list) -> None :
    """將輸入的list中的每個元素，分別寫入到名為webcrawler的資料庫的devops表格中。

    Args:
        list_test_report (list): 列表中，每個元素都是一個字典，分別與 'item'、'response' 和 'screenshot' 三個鍵值對應。
    """
    db = pymysql.connect(host="localhost",
                        user="root",
                        password="root",
                        database="webcrawler")

    cursor = db.cursor()
    sql = "INSERT INTO devops (item, response, screenshot) VALUES (%s, %s, %s)"
    for item in list_test_report:
        val = (item['item'], item['response'], item['screenshot'])
        cursor.execute(sql, val)
        db.commit()