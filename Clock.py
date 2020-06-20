import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from getpass import getpass

# 要打卡的公司登入首頁
url = ''

# 依序填入公司代碼/員工編號/密碼
companyCode = ''
empCode = ''
empPwd = ''
clockType = True

options = webdriver.ChromeOptions()
# options.add_argument('--headless')   在背景執行，不跳出視窗
chrome = webdriver.Chrome(options=options, executable_path='/Users/IEUser/Desktop/chromedriver')
chrome.set_page_load_timeout(10)


# 自動登入流程
def loginAct(url, companyCode, empCode, empPwd):
    chrome.get(url)
    # 找出登入時需要輸入的欄位id

    # 公司代號
    com = chrome.find_element_by_name("input1")
    com.clear()
    com.send_keys(companyCode)

    # 員工編號
    elem = chrome.find_element_by_name('input2')
    elem.clear()
    elem.send_keys(empCode)

    # 密碼
    pwd = chrome.find_element_by_name('input3')
    pwd.clear()
    pwd.send_keys(empPwd)

    # 登入
    # 找出登入時點擊的button_id
    chrome.find_element_by_id("login-button").send_keys(Keys.ENTER)
    time.sleep(5)


# 登入後上下班打卡的流程
def clockAct(clockType):
    try:
        # 找出上下班卡的xpath並click()
        if clockType:
            clockinBtn = chrome.find_element_by_xpath('//*[@id="clockin"]').click()
            print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: Clockin Success!!!')
        else:
            clockoutBtn = chrome.find_element_by_xpath('//*[@id="clockout"]').click()
            print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())} Clockout Success!!!')
    except Exception as ex:
        if clockType:
            print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())} Clockin Failed!!!')
        else:
            print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())} Clockout Failed!!!')
        print(f"Exception:{ex}")


# 登出流程
def logoutAct():
    logoutTest = chrome.find_element_by_xpath('//*[@id="headingFour"]/h4/a/div')
    print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())} Logout Success!!!')
    logoutTest.click()


try:
    checkHost = input('是否為本人(Y/N):')
    if checkHost.lower() != 'y':
        url = input('輸入登入網址:')
        companyCode = input('輸入公司代號:')
        empCode = input('輸入員工編號')
        empPwd = getpass('Password:')

    loginAct(url, companyCode, empCode, empPwd)
    actType = input('1.打卡(上班) 2.打卡(下班) 9.登出 其他數字:不動作')

    if int(actType) == 1:
        clockAct(True)
    elif int(actType) == 2:
        clockAct(False)
    elif int(actType) == 9:
        logoutAct()
    else:
        print('End Close Window')

except Exception as ex:
    chrome.close()
    print(f"Exception:{ex}")
