# -*- coding:utf-8 -*-
from selenium import webdriver
from requests import get
from dataProcess1 import makeArr
import time
import xml.etree.ElementTree as ET

# 구글 맵 지오코딩으로 지명에서 좌표찾기
def mapsfind(name):
    baseURL = "https://maps.googleapis.com/maps/api/geocode/json?address=서울틀별시%20"+name+"&key=AIzaSyAs6l05nxOie1m_lCKiB9IxJt31c5dYPME&lang=ko"
    # baseURL = "https://www.google.co.kr/maps/place/서울특별시+" + name
    # print(baseURL)
    res = get(baseURL).json()["results"]
    location = {}
    if len(res)>0:
        location = res[0]["geometry"]["location"]
    else:
        print("no results")
        location = {"lat":0, "lng":0}
    lan = location["lat"]
    lng = location["lng"]
    print(lan, lng)
    return [str(lan), str(lng)]

def mapsfind2(lat,lng):
    baseURL = "https://maps.googleapis.com/maps/api/geocode/json?latlng="+str(lat)+","+str(lng)+"&key=AIzaSyAs6l05nxOie1m_lCKiB9IxJt31c5dYPME&lang=ko"

def usingSelenium():
    browser = webdriver.PhantomJS()
    browser.implicitly_wait(20)

    browser.get(baseURL)
    time.sleep(5)

    currentURL = browser.current_url
    print(currentURL)
    browser.close()
    temp1 = currentURL.split("/")[4].split(",")[0][1:]
    temp2 = currentURL.split("/")[4].split(",")[1]
    arr = [temp1, temp2]
    print(currentURL.split("/")[4].split(",")[0][1:],currentURL.split("/")[4].split(",")[1])
    return arr

# <SpotInfo>
# <list_total_count>174</list_total_count>
# <RESULT>
# <CODE>INFO-000</CODE>
# <MESSAGE>정상 처리되었습니다</MESSAGE>
# </RESULT>
# <row>
# <spot_num>A-01</spot_num>
# <spot_nm>성산로(금화터널)</spot_nm>
# <grs80tm_x>195489</grs80tm_x>
# <grs80tm_y>452136</grs80tm_y>
# </row>

def parseXML():
    result = open("resultTrafficPoint.txt", "w")
    baseURL = "http://openapi.seoul.go.kr:8088/6c7a556676646e61313038504c69686b/xml/SpotInfo/1/174/"
    res = get(baseURL).text

    root = ET.fromstring(res)
    rows = root.findall("row")
    for row in rows:
        spot_num = row.find("spot_num").text
        spot_nm = row.find("spot_nm").text.encode('cp949')
        grs80tm_x = row.find("grs80tm_x").text
        grs80tm_y = row.find("grs80tm_y").text
        result.write(spot_num + "," +spot_nm.decode('cp949') + "," + grs80tm_x + "," + grs80tm_x + "\n")

    result.close()




# .mol 파일 저장
def download(url, fileName):
    with open("./down/"+fileName, "wb") as file:
        response = get(url)
        file.write(response.content)
    print("check! " + fileName)

def trafficPerPoint():
    result = open("trafficPerPoint2.txt", "w")
    error = open("tppError", "w")
    baseURL = "http://openapi.seoul.go.kr:8088/6c7a556676646e61313038504c69686b/xml/VolInfo/1/20/"

    # 0:지점번호, 1:지점명, 2:X. 3:Y
    arr = makeArr("resultTrafficPoint.txt")

    year = ["2016","2017"]
    month = ["01","02","03","04","05","06","07","08","09","10","11","12"]
    date = ["01","02","03","04","05","06","07","08","09","10"]
    hour = [["00","01","02","03","04","05"],["06","07","08","09","10","11"],["12","13","14","15","16","17"],["18","19","20","21","22","23"]]

    for i in range(11,31):
        date.append(str(i))

    result.write("ymd,hour,spot_num,spot_nm,x,y,io1,io2\n")

    for a in arr:
        print(a[0])
        for y in year:
            for m in month:
                for d in date:
                    if m == 2 and d > 28:
                        continue
                    for hh in hour:
                        vol1 = 0
                        vol2 = 0
                        idx = 1
                        spot_num = a[0]
                        spot_nm = a[1]
                        _x= a[2]
                        _y= a[3]
                        ymd = y+m+str(d)
                        io_type = ""
                        lane_num = ""
                        for h in hh:
                            # print(y,m,d,h)
                            try:
                                targetURL = baseURL+a[0]+"/"+y+m+str(d)+"/"+h+"/"
                                res = get(targetURL).text

                                root = ET.fromstring(res)
                                rows = root.findall("row")
                                for row in rows:
                                    io_type = row.find("io_type").text
                                    if io_type == "1":
                                        vol1 += int(row.find("vol").text)
                                    else:
                                        vol2 += int(row.find("vol").text)
                            except:
                                error.write("/"+a[0]+"/"+ymd+"/"+"h/\n")

                        print(targetURL, vol1, vol2)
                        result.write(ymd+","+str(idx)+","+spot_num+","+spot_nm + "," +_x+","+_y+","+str(vol1)+","+str(vol2)+"\n")

                        idx+=1
    error.close()
    result.close()
# result = open("finalTC.csv", "w")
# lArr = makeArr("resultOfTaxi.csv")
# for loc in lArr:
#     print(loc[1])
#     tmp = mapsfind(loc[1])
#     result.write(loc[0]+","+tmp[0]+","+tmp[1]+","+loc[2]+"\n")
#
# result.close()
# function test
# requestByPubCID("7529")
# requestByPubCID("26041")
# findInCHEBI("OTPSWLRZXRHDNX-UHFFFAOYSA-L", "26041")
# mapsfind("서초3동")

trafficPerPoint()
