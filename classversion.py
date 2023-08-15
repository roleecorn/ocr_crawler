import sqlite3
from drive_downloader import download_driver
from pathlib import Path
import time
import json
from selenium.common.exceptions import NoSuchElementException
import logging
import util
import driver_control
from debugger import Debugger


class ocr_crawler:
    def __init__(self, cite: str, test: bool = True) -> None:
        self.cite = cite
        self.home = Path.cwd()
        self.test = test
        self.driverpath = download_driver(self.home)
        self.driver = None
        self.db_path = self.home / 'sql' / f"{cite}.db"
        if not self.db_path.exists():
            self.sql_add()
            time.sleep(1)
        with open('cite_fathers.json', 'r') as file:
            self.target_class: str = json.load(file)[self.cite]

    def sql_add(self) -> None:
        Debugger.info_print('new database')
        status = sqlite3.connect(self.db_path)
        query = f"""
        CREATE TABLE {self.cite} (
            name TEXT,
            imgcode TEXT,
            oriprice INT,
            price INT,
            color INT,
            feature TEXT,
            gender INT,
            brand TEXT,
            fabric TEXT,
            path TEXT,
            ver INT
        )
        """
        status.execute(query)
        status.close()

    def read_csv(self) -> None:
        self.listsite, self.site_feature = util.read_csv(
            (self.home / 'cite_file' / f'{self.cite}.csv'))

    def new_driver(self):
        Debugger.info_print('new driver')
        self.driver = util.new_driver(self.driverpath)

    def close(self):
        if self.driver:
            self.driver.close()

    def test_start(self):
        Debugger.info_print('test start')
        self.driver.get(url=self.listsite[0])
        imgpath = util.check_imgpath(imgpath=self.home / self.cite,
                                     imgfile=self.site_feature[0])
        time.sleep(5)
        driver_control.scroll_to_bottom_and_wait(driver=self.driver)
        try:
            target_elements = self.driver.find_elements(
                "class name", self.target_class)
        except NoSuchElementException:
            Debugger.error_print('element not find in target_element')

        for element in target_elements:
            tmp = util.capture(ele=element, path=imgpath)

    def shot_all_classes(self):
        self.driver.get(url=self.listsite[0])
        time.sleep(5)
        # 使用 XPath 選擇器來選擇所有有 class 屬性的元素
        elements = driver_control.get_all_classes(self.driver)

        for element in elements:
            try:
                ele = self.driver.find_element(
                    "class name", element)
            except Exception:
                continue
            try:
                util.capture(ele=ele, path=self.home / 'search')
            except Exception:
                pass
