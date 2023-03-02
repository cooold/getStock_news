import resources
import datetime
import webbrowser
import time
import json
from bs4 import BeautifulSoup
import copy
import pandas as pd
import requests

#問日期
print('請輸入日期')
today = input()
#沒有的話取今日
if(today == ''):
    today = datetime.datetime.now().strftime("%m%d")

downloadURL = resources.downloadURL()
#是假日不重新下載
if(resources.isNotHoliday(today)):
    #1 取得request
    request = downloadURL.getRequests(downloadURL.day_URL)
    if(not downloadURL.checkRequestsSuccess(request)):
        error = input()
    #2 加入格式需要的東西
    soup = downloadURL.resToParser(request)
    save_dow = resources.Get_text('F:/daywork_ver3/TemporarilySave/dow.txt')
    save_dow += str(soup)
    #3 刪除舊的csv html
    resources.removeOldFile('F:/daywork_ver3/TemporarilySave/save.html')
    resources.removeOldFile('F:/daywork_ver3/StockList.csv')
    #4 建立新的
    resources.writeFile('F:/daywork_ver3/TemporarilySave/save.html', save_dow)
    #5 註冊瀏覽器
    firefoxPath = "C:/Program Files/Mozilla Firefox/firefox.exe"
    webbrowser.register('firefox', None, webbrowser.BackgroundBrowser(firefoxPath))
    #6 開啟下載
    webbrowser.get('firefox').open('file:///F:/daywork_ver3/TemporarilySave/save.html')
    time.sleep(10)
    #7 建立今日資料夾轉出TXT
    resources.makedirs('F:/daywork_ver3/look/'+ today)
    resources.makedirs('F:/daywork_ver3/observation/'+ today)
    save_csv = resources.Get_textLines('F:/daywork_ver3/StockList.csv')
    #8 CSV轉TEXT
    resources.csvToText(save_csv,'F:/daywork_ver3/look/'+ today + '/' + today + '.txt')

    #抓取其他URL
    for fileName, URL in downloadURL.other_URL.items():
        request = downloadURL.getRequests(URL)
        if(not downloadURL.checkRequestsSuccess(request)):
            error = input()
        soup = downloadURL.resToParser(request)
        resources.writeFile('F:/daywork_ver3/otherLook/'+ today + fileName,str(soup))
        time.sleep(8)
else:
   resources.makedirs('F:/daywork_ver3/look/'+ today)
   resources.makedirs('F:/daywork_ver3/observation/'+ today)
   save_csv = resources.Get_textLines('F:/daywork_ver3/StockList.csv')
   resources.csvToText(save_csv,'F:/daywork_ver3/look/'+ today + '/' + today + '.txt')


#json
saveStockListToJson = {}
saveStockToJson = {}
saveStockNewsToJson = {}
saveNews = {}
stockInfoList = []
stockMonthly_revenueList ={}
stockInfo = resources.stockInfo()

def dictToJson(saveStockListToJson,savepath):
    with open(savepath + '.json', 'w') as fp:
        json.dump(saveStockListToJson, fp)
    stockInfoList.clear()
    print(savepath + '.json 成功儲存')

#抓營收
get_twse_months = resources.get_twse_months()
monthly_revenue = resources.get_twse_monthly_revenue()
#上市
twseList_sii_0 = {}
twseList_sii_1 = {}
#上櫃
twseList_otc_0 = {}
twseList_otc_1 = {}
for i in get_twse_months:
    temp1_0 = monthly_revenue.getRequests(i,'sii','0')
    time.sleep(5)
    print('取得月營收1')
    temp1_1 = monthly_revenue.getRequests(i,'sii','1')
    time.sleep(8)
    print('取得月營收2')
    temp2_0 = monthly_revenue.getRequests(i,'otc','0')
    time.sleep(10)
    print('取得月營收3')
    temp2_1 = monthly_revenue.getRequests(i,'otc','1')
    time.sleep(10)
    print('取得月營收4')
    twseList_sii_0[i] = temp1_0
    twseList_sii_1[i] = temp1_1
    twseList_otc_0[i] = temp2_0
    twseList_otc_1[i] = temp2_1
print('取得月營收完成')

#爬google新聞
def GoogleWebcrawle(stock,savePath):
    googleWebVariable = resources.googleWebVariable()
    times = 0
    c = stock.split()
    stockInfo.number = c[0]
    stockInfo.name = c[1]
    stockInfo.listedOrOtc = c[2]
    stockInfoList.append(copy.deepcopy(stockInfo))
    saveStockToJson['number'] = stockInfo.number
    saveStockToJson['name'] = stockInfo.name
    saveStockToJson['市場'] = stockInfo.listedOrOtc
    url = googleWebVariable.googleNewsURL(c[0] + ' ' + c[1])
    request = stockInfo.getRequests(url)

    if(not stockInfo.checkRequestsSuccess(request)):
        print(stockInfo.name + "google新聞連線失敗")
        error = input()

    soup = stockInfo.resToParser(request)
    #過濾奇摩
    span_tagsYahoo =soup.find_all("div", class_= [googleWebVariable.Class_media])
    #過濾時間
    span_tagsTime =soup.find_all("div", class_= [googleWebVariable.Class_time])
    #過濾標題
    span_tagsTitle =soup.find_all("div", class_= [googleWebVariable.Class_title])
    #過濾連結
    span_tagsHref =soup.find_all("a", class_= [googleWebVariable.Class_href])

    addnumber = 10
    count = 0
    titleCount = 0
    for span_tag in span_tagsYahoo:
        if "奇摩" not in span_tag.span.string and 'LINE' not in span_tag.span.string:
            saveTimes = str(span_tagsTime[times].span.string)
            saveTitle = str(span_tagsTitle[titleCount].string)
            saveHref = str(span_tagsHref[times]["href"])
            saveNews['saveTitle'] = saveTitle
            saveNews['saveTimes'] = saveTimes
            saveNews['saveHref'] = saveHref
            saveStockNewsToJson[count] = copy.deepcopy(saveNews)
            count += 1

            if "分鐘前" in saveTimes or "小時前" in saveTimes:
                if(addnumber > 1):
                    addnumber = 1
            elif "天前" in saveTimes:
                if(addnumber > 2):
                    addnumber = 2
            elif "週前" in saveTimes:
                if(addnumber > 3):
                    addnumber = 3
            elif "月前" in saveTimes:
                if(addnumber > 4):
                    addnumber = 4
            else:
                if(addnumber > 5):
                    addnumber = 5
        times += 1
        titleCount += 2

    if(addnumber == 1):
        resources.writeFile(savePath + '/0小時NEW新聞個股.txt', stockInfo.number + ' ' + stockInfo.name + '\n')
    if(addnumber == 2):
        resources.writeFile(savePath + '/1天NEW新聞個股.txt', stockInfo.number + ' ' + stockInfo.name + '\n')
    if(addnumber == 3):
        resources.writeFile(savePath + '/2週NEW新聞個股.txt', stockInfo.number + ' ' + stockInfo.name + '\n')
    if(addnumber == 4):
        resources.writeFile(savePath + '/3月NEW新聞個股.txt', stockInfo.number + ' ' + stockInfo.name + '\n')
    if(addnumber == 5):
        resources.writeFile(savePath + '/4無NEW新聞個股.txt', stockInfo.number + ' ' + stockInfo.name + '\n')
    print(str(c)+'新聞完成')

#讀取路徑開始爬
def startGet(save,savePath):    
    #開始爬
    for i in range(len(save)):
        print('剩餘'+str(len(save)-i)+'檔股票')
        count = 0
        time.sleep(2)
        #抓google
        GoogleWebcrawle(save[i],savePath)
        #放入字典
        saveStockToJson['news'] = copy.deepcopy(saveStockNewsToJson)
        saveStockNewsToJson.clear()
        #判斷上市還是上櫃
        if(stockInfo.listedOrOtc == '市'):
            #判斷國內外
            if('KY' not in stockInfo.name):
                twseList = twseList_sii_0
            else:
                twseList = twseList_sii_1
        else:
            #判斷國內外
            if('KY' not in stockInfo.name):
                twseList = twseList_otc_0
            else:
                twseList = twseList_otc_1
        #整理公開資訊
        for monthTime, twse in twseList.items():
            want = twse[twse['公司 代號'] == stockInfo.number]
            stockInfo.monthly_revenue['當月營收'] = str(want['當月營收'].values[0])
            stockInfo.monthly_revenue['上月營收'] = str(want['上月營收'].values[0])
            stockInfo.monthly_revenue['當月營收'] = str(want['當月營收'].values[0])
            stockInfo.monthly_revenue['去年當月營收'] = str(want['去年當月營收'].values[0])
            stockInfo.monthly_revenue['上月比較增減(%)'] = str(want['上月比較 增減(%)'].values[0])
            stockInfo.monthly_revenue['去年同月增減(%)'] = str(want['去年同月 增減(%)'].values[0])
            stockInfo.monthly_revenue['當月累計營收'] = str(want['當月累計營收'].values[0])
            stockInfo.monthly_revenue['去年累計營收'] = str(want['去年累計營收'].values[0])
            stockInfo.monthly_revenue['前期比較增減(%)'] = str(want['前期比較 增減(%)'].values[0])
            stockMonthly_revenueList[monthTime] = copy.deepcopy(stockInfo.monthly_revenue)
            count += 1
    
        saveStockToJson['monthlyRevenue'] = copy.deepcopy(stockMonthly_revenueList)
        saveStockListToJson[i] = copy.deepcopy(saveStockToJson)
        saveStockToJson.clear()
        print(stockInfo.number + stockInfo.name + '完成')

#每日新聞
getPath1 = 'F:/daywork_ver3/look/'+ today +'/' + today +'.txt'
savePath1 = 'F:/daywork_ver3/look/'+ today
save1 = resources.Get_textLines(getPath1)
resources.writeFile(savePath1 + '/0小時NEW新聞個股.txt', '')
resources.writeFile(savePath1 + '/1天NEW新聞個股.txt', '')
resources.writeFile(savePath1 + '/2週NEW新聞個股.txt','')
resources.writeFile(savePath1 + '/3月NEW新聞個股.txt', '')
resources.writeFile(savePath1 + '/4無NEW新聞個股.txt', '')

startGet(save1,savePath1)
dictToJson(saveStockListToJson,'F:/daywork_ver3/look/'+ today +'/' + today)
#觀察新聞
getPath2 = 'F:/daywork_ver3/observation/observation.txt'
savePath2 = 'F:/daywork_ver3/observation/'+ today
save2 = resources.Get_textLines(getPath2)
resources.writeFile(savePath2 + '/0小時NEW新聞個股.txt', '')
resources.writeFile(savePath2 + '/1天NEW新聞個股.txt', '')
resources.writeFile(savePath2 + '/2週NEW新聞個股.txt','')
resources.writeFile(savePath2 + '/3月NEW新聞個股.txt', '')
resources.writeFile(savePath2 + '/4無NEW新聞個股.txt', '')

startGet(save2,savePath2)
dictToJson(saveStockListToJson,'F:/daywork_ver3/observation/'+ today +'/' + today)

#顯示今日新聞
print(resources.Get_text('F:/daywork_ver3/look/'+ today + '/0小時NEW新聞個股.txt'))
print(resources.Get_text('F:/daywork_ver3/observation/'+ today + '/0小時NEW新聞個股.txt'))

print('全部完成')
DD = input()
