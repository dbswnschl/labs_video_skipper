from selenium import webdriver
from selenium.common.exceptions import *
from . import staticValues
import requests
from urllib.parse import quote
import os
def makeConf():
    print("[ 계정정보 등록 ]")
    loginId = input("로그인 아이디 입력 :")
    loginPw = input("로그인 비밀번호 입력 :")
    staticValues.parser['SERVER'] = {
        'server_addr': 'http://127.0.0.1:8000'
    }
    staticValues.parser['TARGET'] = {
        'target_addr': 'http://edu.labs.go.kr'
    }
    staticValues.parser['ACCOUNT'] = {
        'user_id': loginId,
        'user_pw': loginPw
    }
    key = getLoginKey()
    if key != None:
        doLogin(key)
        staticValues.parser.write(open(staticValues.conf_file_name, 'w'))
        print("[설정파일 작성완료]")
        return True
    else:
        return False



def confCheck():
    if not os.path.exists(staticValues.conf_file_name):
        print("[경고] 설정파일을 불러오는데 실패했습니다 !")
        print("[설정파일 작성을 시작합니다.]")

        return makeConf()
    else:
        staticValues.parser.read("conf.ini")
        return True


def getLoginKey():
    driver = webdriver.PhantomJS('./phantomjs')
    driver.get(
        staticValues.parser['SERVER']['server_addr'] + "?id=" + staticValues.parser['ACCOUNT']['user_id'] + "&pw=" +
        staticValues.parser['ACCOUNT']['user_pw'])
    try:
        return driver.find_element_by_id("key").text
    except NoSuchElementException as exc:
        print("인증서버 접속에 실패했습니다 ! ")
        return None


def doLogin(loginkey):
    staticValues.pageObj.sess = requests.session()
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
        'Referer': staticValues.parser['TARGET']['target_addr'] + '/UserHome.do?cmd=loginForm',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    staticValues.pageObj.postdata = staticValues.pageObj.sess.post(
        staticValues.parser['TARGET']['target_addr'] + "/UserHome.do", data=logindata, headers=loginheader)
    txt = staticValues.pageObj.postdata.content.decode('utf-8')
    if '로그아웃</a>' in txt:
        print('로그인 성공')
        return True
    else:
        print("로그인에 실패했습니다 !")
        makeConf()
        return False


def getProperty():
    staticValues.pageObj.getdata = staticValues.pageObj.sess.get(
        staticValues.parser['TARGET']['target_addr'] + "/MainHome.do?cmd=goMenuPage&mcd=MC00000032")
    stdNo_list = str(staticValues.pageObj.getdata.content.decode("utf-8")).split("reshView('")
    title_list = str(staticValues.pageObj.getdata.content.decode("utf-8")).split('mT10">')
    sub_code_list = str(staticValues.pageObj.getdata.content.decode('utf-8')).split("listContentsView('")

    for i in range(1, len(stdNo_list)):
        print("[{}] 과목명:{}, 과목번호:{}, 학생번호:{}".format(i, title_list[(i - 1) * 4 + 1].split('</p>')[0],
                                                     sub_code_list[i].split("'")[4], stdNo_list[i].split("'")[0]))

    sub_no = int(input("강의 선택 ([ ] 사이 숫자 입력): "))
    sbjCd = sub_code_list[sub_no].split("'")[4]
    crsCreCd = sub_code_list[sub_no].split("'")[0]
    crsCd = sub_code_list[sub_no].split("'")[2]
    stdNo = stdNo_list[sub_no].split("'")[0]
    staticValues.pageObj.getdata = staticValues.pageObj.sess.get(staticValues.parser['TARGET'][
                                                                     'target_addr'] + "/MainBookmarkLecture.do?cmd=listStuBookmark&mcd=MC00000101&bookmarkDTO.crsCreCd=" + crsCreCd + "&bookmarkDTO.crsCd=" + crsCd + "&bookmarkDTO.sbjCd=" + sbjCd)
    unit_list = str(staticValues.pageObj.getdata.content.decode('utf-8')).split("viewContents('" + sbjCd + "','")
    for i in range(1, len(unit_list), 2):
        unit_no = unit_list[i].split("'")[0]
        unit_title = unit_list[i].split(unit_no + "');\" >")[1].split('</a>')[0].strip().replace("\t", "").replace("  ",
                                                                                                                   "")
        print("[{}] 유닛명:{}".format(int(i / 2 + 1), unit_title))
    unit_sel = int(input("유닛 선택(숫자) : "))
    unitCd = unit_list[(unit_sel - 1) * 2 + 1].split("'")[0]
    pageCnt = input("최대 페이지 수 입력(숫자) : ")
    # doAction(stdNo, sbjCd, unitCd, pageCnt)
    return stdNo, sbjCd, unitCd, pageCnt


def doAction(stdNo, sbjCd, unitCd, pageCnt):
    staticValues.pageObj.sess.get(staticValues.parser['TARGET'][
                                      'target_addr'] + "/MainBookmarkLecture.do?cmd=getTimeStamp&mcd=MC00000101&param=end")
    staticValues.pageObj.sess.get(staticValues.parser['TARGET'][
                                      'target_addr'] + "/MainBookmarkLecture.do?cmd=getTimeStamp&mcd=MC00000101&param=start")
    data = '{"stdNo":"' + stdNo + '","sbjCd":"' + sbjCd + '","unitCd":"' + unitCd + '","studyYn":"Y","studyDttm":"20181007094315","regNo":"USR000125460","quizPassYn":"","passScore":0,"maxScore":0,"minScore":0,"connTotTm":1500,"connTm":1500,"mobileConnTotTm":0,"mobileConnTm":0,"finalConnPage":"1:1:0201","finalStudyPage":' + pageCnt + ',"accmConnPage":"","connPageCnt":"","totPageCnt":"' + pageCnt + '","prgrRatio":4.761904761904762,"connCnt":3,"seekTime":"90","mobileSeekTime":"","errorCode":"0","result":"true","prgrChkType":"PAGE"}'
    url = staticValues.parser['TARGET']['target_addr'] + "/MainBookmarkLecture.do?"
    url += "cmd=addBookmark&mcd=MC00000101&bookmarkJson="
    en_data = quote(data)
    url += en_data
    staticValues.pageObj.getdata = staticValues.pageObj.sess.get(url)
    if 'returnDto' in staticValues.pageObj.getdata.content.decode('utf-8'):
        print("진도율 100% 성공 ! 페이지를 새로고침 해보세요.")
    else:
        print("진도율 달성에 실패했습니다. 최대페이지 등 올바른 정보인지 확인해 보세요.")
