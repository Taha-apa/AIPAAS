
import sqlite3
conn = sqlite3.connect('userData.db')
with open('schema.sql') as sql:
    conn.executescript(sql.read())
conn.commit()
conn.close()