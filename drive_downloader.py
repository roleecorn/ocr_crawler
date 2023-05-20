from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path
import os
myhome = Path.cwd()


def download_driver(path):
    """
    下载 Chrome 驱动程序并将其路径保存到文件中。

    Args:
        path (str): Chrome 驱动程序下载路径。
    """
    driver = ChromeDriverManager(path=path).install()
    relative_path = os.path.relpath(driver)
    with open('driver_path', mode='w', encoding='big5') as f:
        f.write(relative_path)

    print(f'Chrome driver is installed at {driver}')


if __name__ == "__main__":
    download_location = myhome.resolve()
    download_driver(download_location)
