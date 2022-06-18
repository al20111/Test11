import sqlite3

def ReferShift(id, date):
    dbname = 'shift.db'
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    #挿入するレコードを指定
    data = ((id, date))
    #?は後で値を受け取るよという意味
    cursor.execute('SELECT * FROM shift WHERE id = ? AND date = ?', data)

    shift = cursor.fetchone()
    if shift is None:
        start = -1
        end = -1
    else:
        start = shift[2]
        end = shift[3]

    cursor.close()
    conn.close()

    return start, end


print(ReferShift(1, 20220801))
