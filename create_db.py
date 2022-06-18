import sqlite3

#データベース名.db拡張子で設定
dbname = 'shift.db'

#データベースを作成
conn = sqlite3.connect(dbname)

#データベースへのコネクションを閉じる
conn.close()
