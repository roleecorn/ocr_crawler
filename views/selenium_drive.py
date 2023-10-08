from pathlib import Path
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
import sys
load_dotenv()


class driver_class:
    def __init__(self) -> None:
        self.driverpath = Path(os.getenv("DriverPath"))
        self.chromepath = Path(os.getenv("Chromepath"))
        self.driver = None

    def new_driver(self) -> None:
        '''開啟瀏覽器視窗(Chrome)'''

        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.binary_location = str(self.chromepath)
        try:
            s = Service(executable_path=self.driverpath.resolve())
            self.driver = webdriver.Chrome(service=s, options=options)
        except WebDriverException as e:
            print(e)
            print("please check your driver version")
            sys.exit()
        return

    def close(self):
        if self.driver:
            self.driver.close()
