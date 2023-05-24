import re


def formatbig5(name: str) -> str:
    """
    整合非big5的字串
    """
    name = name.encode(encoding="big5", errors='ignore')
    name = name.decode(encoding="big5")
    return name


def remove_non_alphanumeric(string: str) -> str:
    """
    消去非英數字的字元
    """
    tmp = re.sub(r'[^a-zA-Z0-9]', '_', string)
    return tmp.replace("__", "_")


def remove_non_number(string: str) -> float:
    """
    消去非數字或點的字元
    用來過濾掉數字帶文字的類型
    需要注意他可能會留下不該留下的數字
    """
    money = re.sub(r'[^0-9\.]', '', string)
    try:
        return float(money)
    except ValueError:
        print(f"could not convert string to float: {string}")
        return -1


if __name__ == '__main__':
    print(remove_non_number('456dfafe.gaz23.afa'))
