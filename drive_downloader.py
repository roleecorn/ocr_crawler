from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path


def download_driver(path: Path):
    """
    下载 Chrome 驱动程序并将其路径保存到文件中。

    Args:
        path (str): Chrome 驱动程序下载路径。
    """
    driver = ChromeDriverManager().install()
    driver = Path(driver)
    # relative_path = driver.relative_to(Path.cwd())
    # with open('driver_path', mode='w', encoding='big5') as f:
    #     f.write(str(relative_path))

    print(f'Chrome driver is installed at {driver}')
    return driver


if __name__ == "__main__":
    download_driver(Path.cwd())
