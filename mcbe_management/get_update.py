from optparse import Option
from webbrowser import Chrome
from selenium import webdriver
#from selenium.webdriver.firefox.options import Options
#from selenium.webdriver.firefox import service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome import service
import chromedriver_binary
import time


#def get_update_url():
#    option = Options()
#    option.headless = True
#    geckodriver = service.Service(executable_path="/var/games/mcbe/lib/geckodriver")
#    browser = webdriver.Firefox(service=geckodriver, options=option)#firefoxを使ってスクレイピング
#    browser.get("https://www.minecraft.net/en-us/download/server/bedrock")#Minecraft bedrock server download pageを開く
#    #チェックボックスを押す
#    elements = browser.find_element_by_class_name("form-check-input") # チェックボックスを取得
#    for element in elements:#チェックボックスを全部押す
#        element.click()
#    elements = browser.find_element_by_xpath('//a[@aria-label="Download Ubuntu Server software for Ubuntu"]')#download linkを取得
#    url = elements.get_attribute("href")
#    return url

def get_update_url():
    #ヘッドレスモードの設定
    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3864.0 Safari/537.36')
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--lang=en-US")
    #ここまで
    browser = webdriver.Chrome(chrome_options=options)#chromeを使ってスクレイピング
    browser.get("https://www.minecraft.net/en-us/download/server/bedrock")#Minecraft bedrock server download pageを開く
    #チェックボックスを押す
    elements = browser.find_elements_by_xpath('/html/body/div/div[1]/div[3]/div/div/div/div[1]/div/div/div/div[1]/div[2]/div/div/div[2]/div[3]/div/label/input') # チェックボックスを取得
    for element in elements:#チェックボックスを全部押す
        element.click()
    time.sleep(2)
    elements = browser.find_elements_by_xpath('/html/body/div/div[1]/div[3]/div/div/div/div[1]/div/div/div/div[1]/div[2]/div/div/div[2]/div[3]/div/a')#download linkを取得
    for element in elements:
        return element.get_attribute("href")
    #print(elements.get_attribute("herf"))    
    
    browser.quit()
    #return url
print(get_update_url())



