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
else:
    print("로그인실패")
print("학생번호 취득중")
getdata = sess.get("http://edu.labs.go.kr/MainHome.do?cmd=goMenuPage&mcd=MC00000032")
stdNo_list = str(getdata.content.decode("utf-8")).split("reshView('")
title_list = str(getdata.content.decode("utf-8")).split('mT10">')
sub_code_list = str(getdata.content.decode('utf-8')).split("listContentsView('")

for i in range(1,len(stdNo_list)):
    print("[{}] 과목명:{}, 과목번호:{}, 학생번호:{}".format(i,title_list[(i-1)*4+1].split('</p>')[0],sub_code_list[i].split("'")[4],stdNo_list[i].split("'")[0]))

sub_no = int(input("강의 선택 ([ ] 사이 숫자 입력): "))
sbjCd = sub_code_list[sub_no].split("'")[4]
crsCreCd = sub_code_list[sub_no].split("'")[0]
crsCd = sub_code_list[sub_no].split("'")[2]
stdNo = stdNo_list[sub_no].split("'")[0]
getdata = sess.get("http://edu.labs.go.kr/MainBookmarkLecture.do?cmd=listStuBookmark&mcd=MC00000101&bookmarkDTO.crsCreCd="+crsCreCd+"&bookmarkDTO.crsCd="+crsCd+"&bookmarkDTO.sbjCd="+sbjCd)

unit_list = str(getdata.content.decode('utf-8')).split("viewContents('"+sbjCd+"','")
# print(getdata.content.decode('utf-8'))
# print("viewContents('"+sbjCd+"','")
for i in range(1,len(unit_list),2):
    unit_no= unit_list[i].split("'")[0]
    unit_title = unit_list[i].split(unit_no+"');\" >")[1].split('</a>')[0].strip().replace("\t","").replace("  ","")
    print("[{}] 유닛명:{}".format(int(i/2+1),unit_title))
unit_sel = int(input("유닛 선택(숫자) : "))
unitCd = unit_list[(unit_sel-1)*2+1].split("'")[0]
pageCnt = input("최대 페이지 수 입력(숫자) : ")
# input("{} {} {}".format(stdNo,sbjCd,unitCd))

sess.get("http://edu.labs.go.kr/MainBookmarkLecture.do?cmd=getTimeStamp&mcd=MC00000101&param=end")
sess.get("http://edu.labs.go.kr/MainBookmarkLecture.do?cmd=getTimeStamp&mcd=MC00000101&param=start")
url = "http://edu.labs.go.kr/MainBookmarkLecture.do?"
url+="cmd=addBookmark&mcd=MC00000101&bookmarkJson="
# stdNo = "EN0000989621"
# sbjCd = "NSC0085628"
# unitCd = "CNT000000806"
# pageCnt = "11"
# data = '{"stdNo":"EN0000968806","sbjCd":"NSC0059822","unitCd":"CNT000000853","studyYn":"","studyDttm":"20181007093526","regNo":"USR000125460","quizPassYn":"","passScore":0,"maxScore":0,"minScore":0,"connTotTm":22,"connTm":12,"mobileConnTotTm":0,"mobileConnTm":0,"finalConnPage":"1:1:0201","finalStudyPage":21,"accmConnPage":"","connPageCnt":"","totPageCnt":"21","prgrRatio":6.25,"connCnt":2,"seekTime":"0","mobileSeekTime":"","errorCode":"0","result":"true","prgrChkType":"PAGE"}'
# data = '{"stdNo":"EN0000968809","sbjCd":"NSC0059822","unitCd":"CNT000000853","studyYn":"Y","studyDttm":"20181007094315","regNo":"USR000125460","quizPassYn":"","passScore":0,"maxScore":0,"minScore":0,"connTotTm":66,"connTm":19,"mobileConnTotTm":0,"mobileConnTm":0,"finalConnPage":"1:1:0201","finalStudyPage":21,"accmConnPage":"","connPageCnt":"","totPageCnt":"21","prgrRatio":4.761904761904762,"connCnt":3,"seekTime":"0","mobileSeekTime":"","errorCode":"0","result":"true","prgrChkType":"PAGE"}'
data = '{"stdNo":"'+stdNo+'","sbjCd":"'+sbjCd+'","unitCd":"'+unitCd+'","studyYn":"Y","studyDttm":"20181007094315","regNo":"USR000125460","quizPassYn":"","passScore":0,"maxScore":0,"minScore":0,"connTotTm":1500,"connTm":1500,"mobileConnTotTm":0,"mobileConnTm":0,"finalConnPage":"1:1:0201","finalStudyPage":'+pageCnt+',"accmConnPage":"","connPageCnt":"","totPageCnt":"'+pageCnt+'","prgrRatio":4.761904761904762,"connCnt":3,"seekTime":"90","mobileSeekTime":"","errorCode":"0","result":"true","prgrChkType":"PAGE"}'
# data = '{"stdNo":"EN0000989621","sbjCd":"NSC0085628","unitCd":"CNT000000805","studyYn":"Y","studyDttm":"20181007095312","regNo":"USR000125460","quizPassYn":"","passScore":0,"maxScore":0,"minScore":0,"connTotTm":74,"connTm":5,"mobileConnTotTm":0,"mobileConnTm":0,"finalConnPage":"1:1:0101","finalStudyPage":1,"accmConnPage":"","connPageCnt":"","totPageCnt":"17","prgrRatio":5.88235294117647,"connCnt":4,"seekTime":"0","mobileSeekTime":"","errorCode":"0","result":"true","prgrChkType":"PAGE"}'
# data = '{"stdNo":"EN0000968806","sbjCd":"NSC0078590","unitCd":"CNT000000816","studyYn":"","studyDttm":"20181007093526","regNo":"USR000125460","quizPassYn":"","passScore":0,"maxScore":0,"minScore":0,"connTotTm":22,"connTm":12,"mobileConnTotTm":0,"mobileConnTm":0,"finalConnPage":"1:1:0201","finalStudyPage":16,"accmConnPage":"","connPageCnt":"","totPageCnt":"16","prgrRatio":6.25,"connCnt":2,"seekTime":"0","mobileSeekTime":"","errorCode":"0","result":"true","prgrChkType":"PAGE"}'
# print(data)
en_data = quote(data)
# print(en_data)
url+=en_data
getdata = sess.get(url)
if 'returnDto' in getdata.content.decode('utf-8'):
    print("진도율 100% 성공 ! 페이지를 새로고침 해보세요.")