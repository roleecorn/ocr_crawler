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

parser = argparse.ArgumentParser(description="自動飯用爬蟲程式")
parser.add_argument("--shop_name", type=str, help="網站名稱", required=True)
parser.add_argument("--test", action='store_true', help="測試選項，只進行一次運作")
args = parser.parse_args()

# 設定logging的配置

start = time.time()
myhome = Path.cwd()

logging.basicConfig(
    filename=myhome / 'logfile' / f'{args.shop_name}.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


listsite, site_feature = util.read_csv(
    (myhome / 'cite_file' / f'{args.shop_name}.csv'))
with open('driver_path', 'r', encoding='big5') as f:
    tmp = f.read()
driver = util.new_driver(myhome / tmp)
with open('cite_fathers.json', 'r') as file:
    father: str = json.load(file)[args.shop_name]
if args.test:
    driver.get(url=listsite[0])
    imgpath = util.check_imgpath(imgpath=myhome / args.shop_name,
                                 imgfile=site_feature[0])
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
    for element in child_elements:
        tmp = util.capture(ele=element, path=imgpath)
        print(tmp)
    import sys
    sys.exit()
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
