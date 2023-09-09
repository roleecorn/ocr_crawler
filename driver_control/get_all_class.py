from selenium import webdriver


def get_all_classes(driver: webdriver.Chrome) -> list[str]:
    """
    Get all unique class names from the current page.
    :param driver: The selenium webdriver instance.
    :return: A set containing all unique class names.
    """
    # 使用 XPath 選擇器來選擇所有有 class 屬性的元素
    elements = driver.find_elements('xpath', '//*[@class]')

    # 獲取所有的 class 值，並將其拆分為獨立的 class 名稱
    all_classes = set()
    for element in elements:
        classes = element.get_attribute('class').split(' ')
        # for cla in classes:
        all_classes.update(classes)

    return list(all_classes)
