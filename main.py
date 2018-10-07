import requests
import configparser
from selenium import webdriver
import json
from urllib.parse import urlencode
from urllib.parse import quote
parser = configparser.ConfigParser()
parser.read("conf.ini")
user_id = parser['ACCOUNT']['user_id']
user_pw = parser['ACCOUNT']['user_pw']
sess = requests.Session()
getdata = sess.get('http://edu.labs.go.kr/UserHome.do?cmd=loginForm')
driver = webdriver.Chrome('./chromedriver')
driver.get("http://127.0.0.1:8000?id="+user_id+"&pw="+user_pw)

loginkey = driver.find_element_by_id("key").text
print(loginkey)
logindata = {
'cmd': 'login',
'goUrl': 'http*3A*2F*2Fedu.labs.go.kr*2FMainHome.do*3Fcmd*3DindexMain',
'loginDTO.encryptData': loginkey
}
loginheader = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'Content-Length': '242',
'Content-Type': 'application/x-www-form-urlencoded',
'Host': 'edu.labs.go.kr',
'Origin': 'http://edu.labs.go.kr',
'Referer': 'http://edu.labs.go.kr/UserHome.do?cmd=loginForm',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}

postdata = sess.post("http://edu.labs.go.kr/UserHome.do", data=logindata,headers=loginheader)
txt= postdata.content.decode('utf-8')
if '로그아웃' in txt:
    print('로그인 성공')

sess.get("http://edu.labs.go.kr/MainBookmarkLecture.do?cmd=getTimeStamp&mcd=MC00000101&param=end")
sess.get("http://edu.labs.go.kr/MainBookmarkLecture.do?cmd=getTimeStamp&mcd=MC00000101&param=start")
url = "http://edu.labs.go.kr/MainBookmarkLecture.do?"
url+="cmd=addBookmark&mcd=MC00000101&bookmarkJson="
stdNo = "EN0000989621"
sbjCd = "NSC0085628"
unitCd = "CNT000000806"
pageCnt = "11"
# data = '{"stdNo":"EN0000968806","sbjCd":"NSC0059822","unitCd":"CNT000000853","studyYn":"","studyDttm":"20181007093526","regNo":"USR000125460","quizPassYn":"","passScore":0,"maxScore":0,"minScore":0,"connTotTm":22,"connTm":12,"mobileConnTotTm":0,"mobileConnTm":0,"finalConnPage":"1:1:0201","finalStudyPage":21,"accmConnPage":"","connPageCnt":"","totPageCnt":"21","prgrRatio":6.25,"connCnt":2,"seekTime":"0","mobileSeekTime":"","errorCode":"0","result":"true","prgrChkType":"PAGE"}'
# data = '{"stdNo":"EN0000968809","sbjCd":"NSC0059822","unitCd":"CNT000000853","studyYn":"Y","studyDttm":"20181007094315","regNo":"USR000125460","quizPassYn":"","passScore":0,"maxScore":0,"minScore":0,"connTotTm":66,"connTm":19,"mobileConnTotTm":0,"mobileConnTm":0,"finalConnPage":"1:1:0201","finalStudyPage":21,"accmConnPage":"","connPageCnt":"","totPageCnt":"21","prgrRatio":4.761904761904762,"connCnt":3,"seekTime":"0","mobileSeekTime":"","errorCode":"0","result":"true","prgrChkType":"PAGE"}'
data = '{"stdNo":"'+stdNo+'","sbjCd":"'+sbjCd+'","unitCd":"'+unitCd+'","studyYn":"Y","studyDttm":"20181007094315","regNo":"USR000125460","quizPassYn":"","passScore":0,"maxScore":0,"minScore":0,"connTotTm":66,"connTm":19,"mobileConnTotTm":0,"mobileConnTm":0,"finalConnPage":"1:1:0201","finalStudyPage":'+pageCnt+',"accmConnPage":"","connPageCnt":"","totPageCnt":"'+pageCnt+'","prgrRatio":4.761904761904762,"connCnt":3,"seekTime":"0","mobileSeekTime":"","errorCode":"0","result":"true","prgrChkType":"PAGE"}'
# data = '{"stdNo":"EN0000989621","sbjCd":"NSC0085628","unitCd":"CNT000000805","studyYn":"Y","studyDttm":"20181007095312","regNo":"USR000125460","quizPassYn":"","passScore":0,"maxScore":0,"minScore":0,"connTotTm":74,"connTm":5,"mobileConnTotTm":0,"mobileConnTm":0,"finalConnPage":"1:1:0101","finalStudyPage":1,"accmConnPage":"","connPageCnt":"","totPageCnt":"17","prgrRatio":5.88235294117647,"connCnt":4,"seekTime":"0","mobileSeekTime":"","errorCode":"0","result":"true","prgrChkType":"PAGE"}'
# data = '{"stdNo":"EN0000968806","sbjCd":"NSC0078590","unitCd":"CNT000000816","studyYn":"","studyDttm":"20181007093526","regNo":"USR000125460","quizPassYn":"","passScore":0,"maxScore":0,"minScore":0,"connTotTm":22,"connTm":12,"mobileConnTotTm":0,"mobileConnTm":0,"finalConnPage":"1:1:0201","finalStudyPage":16,"accmConnPage":"","connPageCnt":"","totPageCnt":"16","prgrRatio":6.25,"connCnt":2,"seekTime":"0","mobileSeekTime":"","errorCode":"0","result":"true","prgrChkType":"PAGE"}'
en_data = quote(data)
print(en_data)
url+=en_data
print(url)
getdata = sess.get(url)
print(getdata.content.decode('utf-8'))