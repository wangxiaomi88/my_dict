import pymysql

db = pymysql.connect(host="localhost",
                     port=3306,
                     user="root",
                     password="1234",
                     database="my_dict",
                     charset="utf8")

# 生成游标
cur = db.cursor()

# 执行sql语句
# create table dict_E2E(word_id INT NOT NULL ,word VARCHAR(100) NULL, explanation VARCHAR(500) NULL,PRIMARY KEY (word_id));

data=[]
count=0
with open("dict.txt", "r") as f:
    for line in f:
        word, explanation = line.split(" ",1)
        count+=1
        data.append((count,word,explanation.strip()))

print(len(data))

try:

    sql = "insert into dict_E2E values (%s,%s,%s); "
    cur.executemany(sql, data)

    db.commit()  # 将操作提交
except Exception as e:
    print(e)
    db.rollback()

# 关闭游标和数据库
cur.close()
db.close()
