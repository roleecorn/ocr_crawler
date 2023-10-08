# Standard library imports
import sqlite3
from pathlib import Path
from datetime import datetime
import time
from typing import List
# Third-party imports
from dotenv import load_dotenv
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
import yaml
from views.selenium_drive import driver_class
from views.new_db import sql_add

# Load environment variables (special case)
load_dotenv()

# Local application imports that depend on environment variables
from debugger import Debugger
import driver_control
import util



class ocr_crawler(driver_class):
    def __init__(self, cite: str, test: bool = True) -> None:
        super().__init__()
        self.cite = cite
        self.home = Path.cwd()
        self.test = test
        self.db_path = self.home / 'sql' / f"{cite}.db"
        self.read_csv()
        current_time = datetime.now()
        self.current_date = str(current_time.date())
        self.version = int(current_time.timestamp())
        if not self.db_path.exists():
            Debugger.info_print("新增資料庫")
            sql_add(db_path=self.db_path, cite=cite)
            time.sleep(1)
        with open(self.home / 'cite_envs' / f"{cite}.yml", 'r') as file:
            cite_config = yaml.safe_load(file)
        self.target_class: str = cite_config.get('target', "")
        self.position: dict[str, dict[str, int]
                            ] = cite_config.get('position', {})
        self.nextpage: str = cite_config.get('nextpage', "")
        self.nextpage_method: str = cite_config.get('method', "")

    def read_csv(self) -> None:
        self.listsite, self.site_feature = util.read_csv(
            (self.home / 'cite_file' / f'{self.cite}_test.csv'))

    def one_page_capture(self, imgpath: Path,
                         img_features: List[str],
                         ocr: bool = False,
                         save: bool = True):
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
            return
        SESSION = sqlite3.connect(self.db_path)
        for element in target_elements:
            tmp = util.capture(ele=element, path=imgpath)
            datas = {
                "imgcode": tmp,
                "path": '/'.join(img_features),
                "ver": self.version
            }
            if ocr:
                price = util.Ocr(img=imgpath/tmp,
                                 posit=self.position['money'])
                datas["price"] = util.remove_non_number(price)
                name = util.Ocr(img=imgpath/tmp,
                                posit=self.position['title'])
                datas["name"] = util.remove_non_alphanumeric(name)
                star = util.Ocr(img=imgpath/tmp,
                                posit=self.position['star'])
                datas["star"] = util.remove_non_number(star)
            clo = util.cloth(datas=datas)
            clo.writedb(db=SESSION, tablename=self.cite)
            del clo
        if save:
            SESSION.commit()
        else:
            SESSION.rollback()
        SESSION.close()

    def test_start(self):
        """
        執行第一個網址的執行
        """
        Debugger.info_print('Test start')
        self.driver.get(url=self.listsite[0])
        time.sleep(3)
        if self.driver.current_url != self.listsite[0]:
            self.driver.get(url=self.listsite[0])
        p = self.home / 'image' / self.cite / self.current_date
        imgpath = util.check_imgpath(imgpath=p, imgfile=['test'])
        self.one_page_capture(imgpath=imgpath,
                              img_features=['test'], save=False)

    def regular_start(self, subcite: int, ocr: bool = False):
        """
        執行選定目標編號網址
        """
        img_features = self.site_feature[subcite]
        self.driver.get(url=self.listsite[subcite])
        if self.driver.current_url != self.listsite[subcite]:
            self.driver.get(url=self.listsite[subcite])
        p = self.home / 'image' / self.cite / self.current_date
        imgpath = util.check_imgpath(imgpath=p,
                                     imgfile=img_features)
        if self.nextpage_method == 'append':
            driver_control.append_page(obj=self)
            self.one_page_capture(
                imgpath=imgpath, img_features=img_features, ocr=ocr)
        elif self.nextpage_method == 'next':
            driver_control.next_page(obj=self, imgpath=imgpath,
                                     img_features=img_features,
                                     ocr=ocr)
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
            except Exception:
                continue
            try:
                util.capture(ele=ele, path=search_path, name=element)
            except ElementNotInteractableException:
                continue
            except Exception as e:
                Debugger.error_print(str(e))
