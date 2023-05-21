from pathlib import Path
import sqlite3


class cloth:
    """
    服裝本身作為class完成標準規格化
    可置入參數：
    oriprice
    price
    imgcode
    facturer
    color
    name
    star
    path
    sex
    """

    def __init__(self, datas: dict) -> None:
        self.price = datas.get("price", -1)
        self.oriprice = datas.get("oriprice", self.price)
        self.imgcode = datas.get("imgcode", -1)
        self.facturer = datas.get("facturer", "nodata")
        self.feature = datas.get("feature", "nodata")
        self.color = datas.get("color", "nodata")
        self.name = datas.get("name", "nodata")
        self.star = datas.get("star", -1)
        self.path = datas.get("path", ".")
        self.sex = datas.get("sex", -1)
        self.ver = datas.get("ver", 0)

    def discount(self) -> int:
        '''
        計算打折
        '''
        return (self.oriprice-self.price)

    def write(self, path: Path, encoding: str = 'UTF-8') -> None:
        '''
        寫入 csv
        '''
        data = f"{self.name},{self.imgcode},{self.oriprice},{self.price},{self.color},{self.feature},{self.sex},{self.facturer}\n"
        with open(str(path), mode='a+', encoding=encoding) as f:
            f.write(data)

    def writedb(self, db: sqlite3.Cursor, tablename: str) -> None:
        '''
        寫入sqlite3資料庫
        '''
        data = (self.name, self.imgcode, self.oriprice, self.price, self.color,
                self.feature, self.sex, self.facturer, "fabric", self.path,
                self.ver)
        db.execute(
            f"insert into {tablename} values (?,?,?,?,?,?,?,?,?,?,?)", data)
        return


# 測試
if __name__ == "__main__":
    cdata = {"name": "op", "price": 123, "color": 'gr,een',
             "sex": 'woman', "star": 4.5, "oriprice": 145}
    cloth1 = cloth(cdata)
    print(cloth1.discount())
    p = Path('.')
    cloth1.write(p)
