import urllib
import util
from pathlib import Path
import sqlite3
import logging
import traceback


def saveimg(src: str, path: Path, shop_name: str,
            datas: dict, db: sqlite3.Cursor):
    """
    從指定的 URL 下載圖片並儲存到指定路徑，然後將資料寫入 SQLite 資料庫。
    需置入參數：
    - src: 圖片的來源 URL
    - path: 圖片的儲存路徑
    - shop_name: 商店名稱
    - datas: 資料字典
    - db: SQLite 資料庫的游標物件
    """
    try:
        urllib.request.urlretrieve(
            src, path)
        tmp = util.cloth(datas)
        tmp.writedb(db, shop_name)
        del tmp
    except urllib.error.HTTPError as e:
        logging.error(f"HTTPError: {e.code} - {e.reason}")
    except urllib.error.URLError as e:
        logging.error(f"URLError: {e.reason}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        with open("error.log", "a") as f:
            traceback.print_exc(file=f)
