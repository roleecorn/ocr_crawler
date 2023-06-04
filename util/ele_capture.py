from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webelement import WebElement
from pathlib import Path
from .new_driver import new_driver
from PIL import Image
import uuid


def capture(ele: WebElement, driver: webdriver.Chrome, path: Path):
    """
    輸入一個網頁物件，並對他進行快照，之後將圖片儲存在本地
    """
    location = element.location
    size = element.size

    driver.save_screenshot("shot.png")

    x = location['x']
    y = location['y']
    w = size['width']
    h = size['height']
    width = x + w
    height = y + h
    filename = str(uuid.uuid4()[:8])+'.png'

    im = Image.open('shot.png')
    im = im.crop((int(x), int(y), int(width), int(height)))
    im.save(path / filename)
    return path / filename


if __name__ == "__main__":
    driver_path = Path('')
    driver = new_driver(driver_path)

    driver.get('https://www.google.co.in')

    element = driver.find_element_by_id("lst-ib")
    file_path = capture(ele=element, driver=driver, path=Path.cwd())
    print(file_path)
