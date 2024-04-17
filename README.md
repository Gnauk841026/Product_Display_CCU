# 中國文化大學推廣部_AI大數據班
## 目錄
- [ELK](#elk)
- [資料收集到資訊處理](#資料收集到資訊處理)

## ELK
查看ELK conf檔：[conf檔](/ELK/ELK_conf檔.conf)
### [ELK_Sales_Analytics](https://yummy-homegrown-8cf.notion.site/ELK_-6d79239160bc4814ba2a2184d072227e?pvs=4)
<img src="Picture/ELK_DashBoard.jpg">
此專題目的是在GCP上，將商場數據以Logstash進行資料清洗與轉換，並上傳至elastic進行數據的分析。
其中，因為經緯度在logstash中轉換後依舊無法被是別為geo_point，因此需要事先建立好index並設定mapping，使經緯度在帶入時可以被是別為地理位置。

## 資料收集到資訊處理
Code:[Code](WebAPI/onedragon)
### [資料收集到資訊處理](https://yummy-homegrown-8cf.notion.site/eec92b02528449839d88cd2003d503b8?pvs=4)
<img src="Picture/onedragon.png">
此專案是我們所學習的技能，進一步的整合與應用。
此次目標是分析Momo與Pchome的差異，並給予Pchome建議。
我主要撰寫的code為以爬蟲抓取Momo的購物網站上的數據，並加以分析。
我抓取了Momo與各銀行的折扣、每日限時搶購的商品資訊、自動搜索指定商品並將所有相關商品抓取。

