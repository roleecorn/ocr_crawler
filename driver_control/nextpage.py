from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from debugger import Debugger


def next_page(obj, imgpath, img_features, ocr):
    while True:
        obj.one_page_capture(
            imgpath=imgpath, img_features=img_features, ocr=ocr)
        try:
            buttom = obj.driver.find_element(
                "class name", obj.nextpage)
            action = ActionChains(obj.driver)
            action.move_to_element(buttom)
            action.click().perform()
            # obj.driver.execute_script(
            #     "arguments[0].scrollIntoView();", buttom)
            # buttom.click()
        except NoSuchElementException:
            break
        except Exception as e:
            Debugger.error_print(str(e))
            break


def append_page(obj):
    while True:
        try:
            buttom = obj.driver.find_element(
                "class name", obj.nextpage)
            # obj.driver.execute_script(
            #     "arguments[0].scrollIntoView();", buttom)
            # buttom.click()
            action = ActionChains(obj.driver)
            action.move_to_element(buttom)
            action.click().perform()
        except NoSuchElementException:
            Debugger.info_print('no nextpage')
            break
        except Exception as e:
            Debugger.error_print(str(e))
            break