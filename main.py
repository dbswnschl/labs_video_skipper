
from modules.login import *
'''
필요사항
login.py의        'server_addr': 'http://127.0.0.1:8000' 부분 


'''

if __name__ == "__main__":
    if confCheck() == True:

        print("로그인정보 암호화중")
        loginkey = getLoginKey()
        if loginkey != None:
            if doLogin(loginkey) == True:
                while True:
                    stdNo, sbjCd, unitCd, pageCnt = getProperty()
                    doAction(stdNo, sbjCd, unitCd, pageCnt)