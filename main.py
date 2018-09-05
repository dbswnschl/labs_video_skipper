from selenium import webdriver

# driver = webdriver.Chrome()
login_id = ""
login_pw = ""
url = "http://edu.labs.go.kr/MainHome.do?cmd=indexMain"
driver.get(url)
driver.find_element_by_id("login_id").sendkeys(login_id)
driver.find_element_by_id("login_id").sendkeys(login_pw)
driver.find_element_by_class_name("btn btn-green").click()


# login


# page_open

