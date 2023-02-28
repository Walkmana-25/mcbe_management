from optparse import Option
from webbrowser import Chrome
from selenium import webdriver
#from selenium.webdriver.firefox.options import Options
#from selenium.webdriver.firefox import service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome import service
from selenium.common.exceptions import TimeoutException
import chromedriver_binary
import time
from pyvirtualdisplay import Display
from mcbe_management import lib, exceptions


def get_update_url():
    #ヘッドレスモードの設定
    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument(f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36')
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    #options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--lang=en-US")
    #displayの生成
    display = Display(visible = 0, size=(1920,1080))
    display.start()
    #ここまで
    browser = webdriver.Chrome(chrome_options=options)#chromeを使ってスクレイピング
    browser.delete_all_cookies()
    browser.set_page_load_timeout(30)
    try:
        browser.get("https://www.minecraft.net/en-us/download/server/bedrock")#Minecraft bedrock server download pageを開く
    except TimeoutException:
            pass
        #チェックボックスを押す
    elements = browser.find_elements_by_xpath('/html/body/div/div[1]/div[3]/div[2]/div/div/div[1]/div/div/div/div[2]/div/div/div/div[2]/div[3]/div/label/input') # チェックボックスを取得
    for element in elements:#チェックボックスを全部押す
        element.click()
    time.sleep(2)
    elements = browser.find_elements_by_xpath('/html/body/div/div[1]/div[3]/div[2]/div/div/div[1]/div/div/div/div[2]/div/div/div/div[2]/div[3]/div/a')#download linkを取得
    for element in elements:
        return element.get_attribute("href")
    #print(elements.get_attribute("herf"))    
    
    browser.quit()
    display.stop()
    
def server_update(manual=True):
    if manual == True:
        print("Update Minecraft Server")
    #Serverが起動しているか確認
    if lib.check_server_started() == True:
        raise exceptions.server_is_started()

if __name__ == "__main__":
    print(get_update_url())
    

