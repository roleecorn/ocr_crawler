"""
這是一個實用工具模塊。

模塊功能：
- 提供讀取 CSV 文件的函數 read_csv
- 提供字符串處理函數 remove_non_alphanumeric 和 remove_non_number
- 提供創建新網頁模擬驅動的函數 new_driver
- 提供新建資料夾路徑的函數 check_imgpath
"""


from .readurl import read_csv
from .string_util import remove_non_alphanumeric, remove_non_number
from .new_driver import new_driver
from .check_imgpath import check_imgpath


__all__ = ["read_csv", "new_driver",
           "remove_non_alphanumeric",
           "remove_non_number",
           "check_imgpath"]
__version__ = "0.1"
