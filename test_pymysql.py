import pymysql
db = pymysql.connect(host="localhost",
                     port=3306,
                     user="root",
                     password="1234",
                     database="sanguo",
                     charset="utf8")

# 生成游标
cur=db.cursor()



# 执行sql语句
# print(cur)


# 写数据库

# id="32"
# name="'王平'" #注意，要额外加引号
# gender="'m'"
# country="'蜀'" #注意，要额外加引号
# attack="132"
# defense="77"


sql_read="select count(*) from person_info;"
cur.execute(sql_read)
id_start=cur.fetchone()[0]
print(type(id_start))
print(id_start)



id=id_start+1
name="未知" #注意，要额外加引号
gender="m"
country="蜀" #注意，要额外加引号
attack="132"
defense="77"

data=[("50","未知","m","蜀","100","100"),
      ("51","未知","m","蜀","100","100"),
      ("52","未知","m","蜀","100","100")]

try:
    # sql="insert into person_info values (%s,%s,%s,%s,%s,%s); " % (id,name,gender,country,attack,defense)
    # cur.execute(sql)

    sql = "insert into person_info values (%s,%s,%s,%s,%s,%s); "
    cur.execute(sql,[id, name, gender, country, attack, defense])
    # cur.executemany(sql, data)

    sql="update person_info set attack=112 where id=1;"
    cur.execute(sql)

    sql_read = "select * from person_info;"
    cur.execute(sql_read)

    for i in cur:
        print(i)


    db.commit() #将操作提交
except Exception as e:
    print(e)
    db.rollback()




# 关闭游标和数据库
cur.close()
db.close()