from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webelement import WebElement
from pathlib import Path
from .new_driver import new_driver


def capture(ele: WebElement, driver: webdriver.Chrome, path: Path):
    """
    輸入一個網頁物件，並對他進行快照，之後將圖片儲存在本地
    """

    return path


if __name__ == "__main__":
    
    print(capture())