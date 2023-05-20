import sqlite3
import time
import logging
import json
from pathlib import Path
import argparse
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

import util
import driver_control

parser = argparse.ArgumentParser(description="這是一個簡單的範例 argparse 程式")
parser.add_argument("--shop_name", help="提供一個名字作為參數", required=True)
args = parser.parse_args()

# 設定logging的配置

start = time.time()
myhome = Path.cwd()

logging.basicConfig(
    filename=myhome / 'logfile' / '{shop_name}.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 使用logging對象輸出日誌
logging.info('This is a test message')

a, b = util.read_csv(Path.cwd() / 'eddiebauer_test.csv')
listsite, site_feature = util.read_csv(
    (myhome / 'cite_file' / f'{args.shop_name}.csv').resolve())

driver = util.new_driver()
with open('cite_fathers.json', 'r') as file:
    father: str = json.load(file)[args.shop_name]
for i in len(listsite):
    driver.get(url=listsite[i])
    time.sleep(5)
    driver_control.scroll_to_bottom_and_wait(driver=driver)
    try:
        parent_element = driver.find_element("class name", father)
    except NoSuchElementException:
        logging.error('element not find in parent_element')
    try:
        child_elements = parent_element.find_elements('xpath', "./*")
    except NoSuchElementException:
        logging.error('element not find in child_elements')
    # 接下來開始對每個子元素截圖

    # 然後按下一頁
