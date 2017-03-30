
import sqlite3

conn = sqlite3.connect('data.db')
cursor = conn.cursor()
# cursor.execute('CREATE TABLE HOUSE (id INTEGER PRIMARY KEY AUTOINCREMENT ,title varchar(20),loc varchar(20),time varchar(20),url varchar(20))')
# cursor.close()
# conn.commit()
# conn.close()
class Sql:
    @classmethod
    def insert_item(cls,title,time,url):
        sql = "INSERT INTO HOUSE (title,time,url) VALUES (?, ?, ?)"
        value = [title,time,url]
        print(sql)
        cursor.execute(sql,value)
        conn.commit()
    @classmethod
    def select_url(cls,url):
        cursor.execute('SELECT * FROM HOUSE WHERE url=(?)',(url,))
        values = cursor.fetchall()
        return values
    @classmethod
    def close_sql(self):
        cursor.close()
        conn.close()



