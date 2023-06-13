
import pandas as pd
import sqlite3
from datetime import date
import sys
dbname = sys.argv[1]


status = sqlite3.connect(f"images/{dbname}/{dbname}.db")
status.execute(f"drop table if exists {dbname}")
try:
    status.execute(f"create table {dbname}(name text,imgcode text,oriprice int, price int, color int,feature text,gender int ,brand text,fabric text, path text,ver int)")
    print("execute")
except Exception as e:
    print(e)
    print("Already table existed !!")

status = sqlite3.connect(f"{dbname}/{dbname}.db")


# data = ("Classic Down Parka", "parka_001", 199, 179, 1, "waterproof and warm", 1, "Eddie Bauer", "down","crawer\sql.ipynb")

# status.execute(f"insert into {dbname} values (?,?,?,?,?,?,?,?,?,?)",data)
# status.commit()

status.execute("VACUUM;")
status.close()


