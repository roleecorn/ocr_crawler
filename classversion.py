import sqlite3
from drive_downloader import download_driver
from pathlib import Path
import time
import yaml
from selenium.common.exceptions import NoSuchElementException
import util
import driver_control
from debugger import Debugger
from datetime import datetime


class ocr_crawler:
    def __init__(self, cite: str, test: bool = True) -> None:
        self.cite = cite
        self.home = Path.cwd()
        self.test = test
        self.driverpath = download_driver(self.home)
        self.driver = None
        self.db_path = self.home / 'sql' / f"{cite}.db"
        self.read_csv()
        self.current_date = str(datetime.now().date())
        if not self.db_path.exists():
            self.sql_add()
            time.sleep(1)
        with open(self.home / 'cite_envs' / f"{cite}.yml", 'r') as file:
            cite_config = yaml.safe_load(file)
        self.target_class: str = cite_config.get('target', "")
        self.position: dict[str, dict[str, int]] = cite_config.get('position', {})
        self.nextpage: dict[str, str] = cite_config.get('nextpage', {})

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
            (self.home / 'cite_file' / f'{self.cite}_test.csv'))

    def new_driver(self):
        Debugger.info_print('new driver')
        self.driver = util.new_driver(self.driverpath)

    def close(self):
        if self.driver:
            self.driver.close()

    def one_page_start(self, imgpath: Path):
        """
        執行一個頁面的截圖
        """
        time.sleep(5)
        driver_control.scroll_to_bottom_and_wait(driver=self.driver)
        try:
            target_elements = self.driver.find_elements(
                "class name", self.target_class)
        except NoSuchElementException:
            Debugger.error_print('element not find in target_element')

        for element in target_elements:
            tmp = util.capture(ele=element, path=imgpath)

    def test_start(self):
        """
        執行第一個網址的執行
        """
        Debugger.info_print('test start')
        self.driver.get(url=self.listsite[0])
        time.sleep(3)
        if self.driver.current_url != self.listsite[0]:
            self.driver.get(url=self.listsite[0])
        p = self.home / 'image' / self.cite / self.current_date
        imgpath = util.check_imgpath(imgpath=p, imgfile=['test'])
        self.one_page_start(imgpath=imgpath)

    def regular_start(self, subcite: int):
        """
        執行選定目標編號網址
        """
        Debugger.info_print(f'regular start {self.site_feature[subcite]}')
        self.driver.get(url=self.listsite[subcite])
        if self.driver.current_url != self.listsite[subcite]:
            self.driver.get(url=self.listsite[subcite])
        p = self.home / 'image' / self.cite / self.current_date
        imgpath = util.check_imgpath(imgpath=p,
                                     imgfile=self.site_feature[subcite])
        if self.nextpage['method'] == 'extend':
            while True:
                driver_control.go_bottom_and_wait(driver=self.driver)
                try:
                    buttom = self.driver.find_element(
                        "class name", self.nextpage['item'])
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView();", buttom)
                    buttom.click()
                except NoSuchElementException:
                    Debugger.info_print('no nextpage')
                    break
                except Exception as e:
                    Debugger.error_print(str(e))
                    break
            self.one_page_start(imgpath=imgpath)
        elif self.nextpage['method'] == 'new':
            while True:
                self.one_page_start(imgpath=imgpath)
                try:
                    buttom = self.driver.find_element(
                        "class name", self.nextpage['item'])
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView();", buttom)
                    buttom.click()
                except NoSuchElementException:
                    Debugger.info_print('no nextpage')
                    break
                except Exception as e:
                    Debugger.error_print(str(e))
                    break
        else:
            raise AttributeError

    def all_start(self):
        """
        遍歷所有網址進行一次regular_start
        """
        start = time.time()
        for i in range(len(self.listsite)):
            self.regular_start(i)
        end = time.time()
        Debugger.dc_print(f'all start end cost {end - start}(s)')

    def shot_all_classes(self):
        self.driver.get(url=self.listsite[0])
        time.sleep(5)
        driver_control.scroll_to_bottom_and_wait(driver=self.driver)
        # 使用 XPath 選擇器來選擇所有有 class 屬性的元素
        elements = driver_control.get_all_classes(self.driver)

        for element in elements:
            try:
                ele = self.driver.find_element(
                    "class name", element)
            except NoSuchElementException:
                continue
            except Exception as e:
                Debugger.error_print(str(e))
            try:
                util.capture(ele=ele, path=self.home / 'search')
            except Exception as e:
                Debugger.error_print(str(e))
