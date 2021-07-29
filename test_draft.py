from dict_db import *

db=Database()
db.create_cur()

# db.register("hehe","456")

r=db.hist("xiaohong")
for line in r:
    msg="条目"+str(line[0])+"，用户名："+line[2]+"，查询单词："+line[3]+"，查询时间："+str(line[4])+"；"+"|"
    print(msg)

print("$".encode())

db.cur.close()
db.close()

