from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from pathlib import Path
import sys


def new_driver(dpath: Path) -> webdriver.Chrome:
    '''開啟瀏覽器視窗(Chrome)'''
    print('執行開始')

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    try:
        s = Service(executable_path=dpath.resolve())
        driver = webdriver.Chrome(service=s, options=options)
    except WebDriverException as e:
        print(e)
        print("please check your driver version")
        sys.exit()
    return driver
