from pathlib import Path
import util
from typing import List, Tuple


def read_csv(file: Path, encoding: str = 'utf-8-sig'
             ) -> Tuple[List[str], List[List[str]]]:
    """
    從指定路徑的CSV檔案中讀取數據。

    Args:
        file (Path): 要讀取的CSV檔案的路徑。
        encoding (str, optional): 要使用的編碼方式。
        預設為'utf-8-sig'。

    Returns:
        Tuple[List[str], List: 
        包含兩個元素的元組。第一個元素是CSV檔案中最後一個非空欄位的值
        第二個元素是CSV檔案中每一行中最後一個非空欄位之前的所有欄位值，儲存在一個二維字串列表中。

    """
    listsite = []
    site_feature = []
    with open(file.resolve(), encoding=encoding) as f:
        tmp = f.readline().strip()
        while (tmp):
            tmp = tmp.split(",")
            for i in range(len(tmp)-1, -1, -1):
                if tmp[i] == "" or tmp[i] == "\n":
                    continue
                listsite.append(tmp[i])
                site_feature.append(tmp[:i])
                break
            tmp = f.readline().strip()
    assert len(listsite) == len(site_feature)
    for i in range(len(site_feature)):
        for j in range(len(site_feature[i])):
            site_feature[i][j] = util.remove_non_alphanumeric(
                site_feature[i][j]).replace("__", "")
    return listsite, site_feature
