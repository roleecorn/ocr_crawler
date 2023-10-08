import sqlite3


def sql_add(db_path, cite) -> None:
    status = sqlite3.connect(db_path)
    query = f"""
    CREATE TABLE {cite} (
        name TEXT,
        imgcode TEXT,
        oriprice INT,
        price INT,
        color INT,
        feature TEXT,
        gender INT,
        brand TEXT,
        fabric TEXT,
        path TEXT,
        ver INT
    )
    """
    status.execute(query)
    status.close()
