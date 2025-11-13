import sqlite3

conn = sqlite3.connect("censoescolar.db")
cursor = conn.cursor()

cursor.execute("SELECT codigo, nome FROM tb_instituicao_csv LIMIT 5")
print(cursor.fetchall())

conn.close()