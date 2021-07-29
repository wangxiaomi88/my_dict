import pymysql
import hashlib

#对密码进行加密
def change_passwd(passwd):
    hash=hashlib.md5()
    hash.update(passwd.encode())
    return hash.hexdigest()





class Database:
    def __init__(self):
        self.db=pymysql.connect(host="localhost",
                     port=3306,
                     user="root",
                     password="1234",
                     database="my_dict",
                     charset="utf8")

    def create_cur(self):
        self.cur=self.db.cursor()

    def close(self):
        self.db.close()


    def record(self,name,word):
        try:
            sql = "select count(*) from dict_hist;"
            self.cur.execute(sql)
            temp = self.cur.fetchone()
            n = temp[0] + 1

            sql = "insert into dict_hist (hist_id,user_name,word) values (%s,%s,%s);"
            self.cur.execute(sql, [n, name, word])
            self.db.commit()
            return True

        except Exception as e:
            self.db.rollback()
            return False

    def hist(self,name):
        sql = "select * from dict_hist where user_name=%s order by search_time desc limit 10;"
        self.cur.execute(sql, name)
        r = self.cur.fetchall()
        return r


    def search(self,name,word):
        sql = "select * from dict_E2E where word=%s;"
        self.cur.execute(sql, word)
        r=self.cur.fetchone()
        if r:
            flag=True
            mean=r[2]
            return flag,mean
        else:
            flag=False
            mean=""
            return flag,mean




    def register(self,name,passwd):
        sql="select * from dict_user where name=%s;"
        self.cur.execute(sql,name)
        r=self.cur.fetchone()
        if r:
            return False
        else:
            try:
                sql="select count(*) from dict_user;"
                self.cur.execute(sql)
                temp=self.cur.fetchone()
                n=temp[0]+1

                passwd=change_passwd(passwd)
                sql="insert into dict_user (user_id,name,password) values (%s,%s,%s);"
                self.cur.execute(sql, [n,name,passwd])
                self.db.commit()
                return True

            except Exception as e:
                self.db.rollback()
                return False


    def login(self,name,passwd):
        passwd=change_passwd(passwd)
        sql="select * from dict_user where name=%s and password=%s;"
        self.cur.execute(sql,[name,passwd])
        r=self.cur.fetchone()
        if r:
            return True
        else:
            return False



