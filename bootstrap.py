import sqlite3
from sqlite3 import Error

DB_PATH = "./data/db.db"
SQL_PATH = "./data/init.sql"
FLAG_PATH = "./data/init.complete"

try:
    con = sqlite3.connect(DB_PATH)
except:
    # Ошибка во время подключения БД
    exit(1)
try:
    cur = con.cursor()
except:
    # Ошибка во время создания курсора
    exit(2)
try:
    with open(SQL_PATH, 'r') as file: 
        sql_query = file.read()
except:
    # Ошибка во время получения SQL структуры из файла
    exit(3)
try:
    for _ in range(sql_query.count(';')):
        res = cur.execute(sql_query[:sql_query.find(';')])
        sql_query = sql_query[sql_query.find(';') + 1:]     
except Error as e:
    print(e)
    # Ошибка во время загрузки SQL структуры в бд
    exit(4)
try:
    con.commit()
except:
    # Ошибка во время совершения SQL запроса в бд
    exit(5)
try:
    con.close()
except:
    # Ошибка во время закрытия бд
    exit(6)
file = open(FLAG_PATH, 'w')
file.write("Init complete")
file.close()
exit(0)