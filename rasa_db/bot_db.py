import sqlite3   #导入sqlite3模块

conn = sqlite3.connect("freshfeast.db")     #建立一个基于硬盘的数据库实例

cur = conn.cursor()         #通过建立数据库游标对象，准备读写操作
cur.execute("CREATE TABLE feedback(taste text, environment text, service text)")
conn.close()        #关闭与数据库的连接

