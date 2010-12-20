import sqlite3 as sql

def create_tables(conn):
    c=conn.cursor()
    c.execute("""
    CREATE TABLE element(
        number ineger primary key,
        name varchar(20) unique,
        symbol varchar(10)
    )""")


def in_mem():
    return sql.connect(":memory:")

def test_create():
    db=in_mem()
    create_tables(db)


if __name__=="__main__":
    test_create()
