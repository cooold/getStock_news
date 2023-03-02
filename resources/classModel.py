import requests
import pandas as pd
from bs4 import BeautifulSoup
from resources.baseFunction import *

class httpRequests:
    def getRequests(self, url):
        res = requests.get(url, headers=headers) 
        res.encoding = 'utf-8'
        return res

    def checkRequestsSuccess(self,res):
        if res.status_code == 200:
           print("篩選網站成功回應")
           return True
        else:
            print("爬取失敗，伺服器沒有回應")
            return False
    
    def resToParser(self,res):
        soup = BeautifulSoup(res.text,"html.parser")
        return soup


class stockInfo(httpRequests):
    number = ""
    name = ""
    news = []
    listedOrOtc = ''
    monthly_revenue = {
        '當月營收' : '0',
        '上月營收' : '0',
        '去年當月營收' : '0',
        '上月比較增減(%)' : '0',
        '去年同月增減(%)' : '0',
        '當月累計營收' : '0',
        '去年累計營收' : '0',
        '前期比較增減(%)' : '0'
    }
    eps  = []

class downloadURL(httpRequests):
    day_URL = get_dayURL
    other_URL = {}
    other_URL['歷史新高.html'] = get_historicalHigh_URL
    other_URL["投信上市.html"] = get_InvestmentTrust_URL1
    other_URL["投信上櫃.html"] = get_InvestmentTrust_URL2

class googleWebVariable(httpRequests):
    Class_title = Class_title
    Class_time = Class_time
    Class_media = Class_media
    Class_href = Class_href

    def googleNewsURL(self,b):
        a ='https://www.google.com.tw/search?q='
        c = '&tbm=nws'
        googleURL = a + b + c
        return googleURL

class get_twse_monthly_revenue:
    
    def getRequests(self, date, web, ky):
        url = 'https://mops.twse.com.tw/nas/t21/'+ web +'/t21sc03_'+ date +'_' + ky +'.html'
        res = requests.get(url, headers=headers) 
        res.encoding = 'big5'
        if res.status_code == 200:
           pass
        else:
            print("爬取失敗，公開資訊觀測站沒有回應")
            dd = input()
        html_df = pd.read_html(res.text)
        # 剃除行數錯誤的表格,並將表格合併
        df = pd.concat([df for df in html_df if df.shape[1] == 11]) 
        # 設定表格的header 
        df.columns = df.columns.get_level_values(1)
        return df
    



