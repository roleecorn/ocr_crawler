from selenium.webdriver.remote.webelement import WebElement
from pathlib import Path
import uuid


def capture(ele: WebElement, path: Path, name: str=""):
    """
    輸入一個網頁物件，並對他進行快照，之後將圖片儲存在本地
    """
    if not name:
        uuid_obj = uuid.uuid4()
        filename = str(uuid_obj)[:8]+'.png'
    else:
        filename = name + '.png'
    ele.screenshot(str(path / filename))
    return filename


if __name__ == "__main__":
    import time
    from new_driver import new_driver
    myhome = Path.cwd().parent
    driver_path = myhome / '.wdm' / 'drivers' / 'chromedriver' / 'win32'
    driver_path = driver_path / '113.0.5672' / 'chromedriver.exe'
    driver = new_driver(driver_path)

    driver.get('https://www.google.co.in')
    time.sleep(5)
    element = driver.find_element('class name', 'lnXdpd')
    file_path = capture(ele=element, driver=driver, path=myhome / 'src')
    driver.close()
    print(file_path)
