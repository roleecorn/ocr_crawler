import time
from selenium import webdriver
def scroll_to_bottom_and_wait(driver:webdriver.Chrome):
    last_height = driver.execute_script(
        "return document.documentElement.scrollHeight")
    print(f"last_height:{last_height}")
    height_w = 100
    while height_w < last_height-1000:
        # 模擬滑鼠滾輪滾動
        driver.execute_script(f"window.scrollTo(0, {height_w});")
        # print(f"scrollTo: {height_w}")
        time.sleep(1)
        # 檢查是否滾動完成
        height_w += 300

def go_bottom_and_wait(driver:webdriver.Chrome):
    last_height = driver.execute_script(
        "return document.documentElement.scrollHeight")
    print(f"last_height:{last_height}")
    height_w = 100
    driver.execute_script(f"window.scrollTo(0, {last_height-300});")

    time.sleep(1)
