import pymysql

def connect_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="123",
        database="elder_care",
        charset="utf8mb4"
    )
