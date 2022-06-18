import sqlite3
import ReferShift

def ApproveShift(id, date, start, end):
    dbname = 'shift.db'
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    if ReferShift.ReferShift(id, date) == (-1, -1):
        return 0

    #挿入するレコードを指定
    data = ((id, date, start, end))
    #?は後で値を受け取るよという意味
    cursor.execute('UPDATE shift SET b = 1 WHERE id = ? AND date = ? AND start = ? AND end = ?', data)

    conn.commit()

    cursor.close()
    conn.close()

    return 1

dbname = 'shift.db'
conn = sqlite3.connect(dbname)
cursor = conn.cursor()

b = ApproveShift(1, 20220801, 1700, 1800)
cursor.execute('SELECT * FROM shift')

# 中身を全て取得するfetchall()を使って、printする。
print(cursor.fetchall())

cursor.close()
conn.close()
