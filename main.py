
from modules.login import *


if __name__ == "__main__":
    if confCheck() == True:

        print("로그인정보 암호화중")
        loginkey = getLoginKey()
        if loginkey != None:
            if doLogin(loginkey) == True:
                stdNo, sbjCd, unitCd, pageCnt = getProperty()
                doAction(stdNo, sbjCd, unitCd, pageCnt)