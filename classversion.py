# Standard library imports
import sqlite3
from pathlib import Path
from datetime import datetime
import os
import time

# Third-party imports
from dotenv import load_dotenv
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
import yaml

# Load environment variables (special case)
load_dotenv()

# Local application imports that depend on environment variables
import util
import driver_control
from debugger import Debugger


class ocr_crawler:
    def __init__(self, cite: str, test: bool = True) -> None:
        self.cite = cite
        self.home = Path.cwd()
        self.test = test
        # self.driverpath = self.home / 'chromedriver.exe'
        self.driverpath = Path(os.getenv("DriverPath"))
        self.chromepath = Path(os.getenv("Chromepath"))
        self.driver = None
        self.db_path = self.home / 'sql' / f"{cite}.db"
        self.read_csv()
        current_time = datetime.now()
        self.current_date = str(current_time.date())
        self.version = int(current_time.timestamp())
        if not self.db_path.exists():
            self.sql_add()
            time.sleep(1)
        with open(self.home / 'cite_envs' / f"{cite}.yml", 'r') as file:
            cite_config = yaml.safe_load(file)
        self.target_class: str = cite_config.get('target', "")
        self.position: dict[str, dict[str, int]
                            ] = cite_config.get('position', {})
        self.nextpage: dict[str, str] = cite_config.get('nextpage', {})
        # self.SESSION = sqlite3.connect(self.db_path)

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
        self.driver = util.new_driver(dpath=self.driverpath,
                                      cpath=self.chromepath)

    def close(self):
        if self.driver:
            self.driver.close()

    def one_page_start(self, imgpath: Path, img_features: list[str],
                       ocr: bool = False):
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
        SESSION = sqlite3.connect(self.db_path)
        for element in target_elements:
            tmp = util.capture(ele=element, path=imgpath)
            datas = {
                # "price": 100.50,
                # "oriprice": 150.00,
                "imgcode": tmp,
                # "facturer": "ABC Company",
                # "feature": "Waterproof",
                # "color": "Blue",
                # "name": "Cool Shoe",
                # "star": 4.5,
                "path": '/'.join(img_features),
                # "sex": 1,
                # # Assuming 0 for Female, 1 for Male, -1 for Unknown
                "ver": self.version
            }
            if ocr:
                datas["price"] = util.Ocr(img=imgpath/tmp,
                                          posit=self.position['money'])
                datas["name"] = util.Ocr(img=imgpath/tmp,
                                         posit=self.position['title'])
                datas["star"] = util.Ocr(img=imgpath/tmp,
                                         posit=self.position['star'])
            clo = util.cloth(datas=datas)
            clo.writedb(db=SESSION, tablename=self.cite)
            del clo
        SESSION.commit()
        SESSION.close()

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
        self.one_page_start(imgpath=imgpath, img_features=['test'])

    def regular_start(self, subcite: int, ocr: bool = False):
        """
        執行選定目標編號網址
        """
        img_features = self.site_feature[subcite]
        Debugger.info_print(f'regular start {img_features}')
        self.driver.get(url=self.listsite[subcite])
        if self.driver.current_url != self.listsite[subcite]:
            self.driver.get(url=self.listsite[subcite])
        p = self.home / 'image' / self.cite / self.current_date
        imgpath = util.check_imgpath(imgpath=p,
                                     imgfile=img_features)
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
            self.one_page_start(
                imgpath=imgpath, img_features=img_features, ocr=ocr)
        elif self.nextpage['method'] == 'new':
            while True:
                self.one_page_start(
                    imgpath=imgpath, img_features=img_features, ocr=ocr)
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

    def all_start(self, ocr: bool = False):
        """
        遍歷所有網址進行一次regular_start
        """
        start = time.time()
        for i in range(len(self.listsite)):
            self.regular_start(i, ocr=ocr)
        end = time.time()
        Debugger.dc_print(f'all start end cost {end - start}(s)')

    def shot_all_classes(self):
        time.sleep(2)
        self.new_driver()
        self.driver.get(url=self.listsite[0])
        time.sleep(5)
        driver_control.scroll_to_bottom_and_wait(driver=self.driver)
        # 使用 XPath 選擇器來選擇所有有 class 屬性的元素
        elements = driver_control.get_all_classes(self.driver)
        search_path = self.home / 'search'
        if not search_path.exists():
            search_path.mkdir(parents=True, exist_ok=True)
        for element in elements:
            try:
                ele = self.driver.find_element(
                    "class name", element)
            except NoSuchElementException:
                continue
            except Exception as e:
                # Debugger.error_print(str(e))
                continue
            try:
                util.capture(ele=ele, path=search_path, name=element)
            except ElementNotInteractableException:
                continue
            except Exception as e:
                Debugger.error_print(str(e))
