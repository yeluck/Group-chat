"""
    聊天室数据操作
"""
import pymysql

class Login:
    def __init__(self):
        self.host='127.0.0.1'
        self.port=3306
        self.user='root'
        self.passwd='123456'
        self.database='udp_server'
        self.table='user'
        self.charset='utf8'
        self.connect_db()

    def connect_db(self):
        self.db=pymysql.connect(host=self.host,
                           port=self.port,
                           user=self.user,
                           passwd=self.passwd,
                           database=self.database,
                           charset=self.charset)

        self.cur=self.db.cursor()

    def login(self,name,pw,addr):
        sql="select * from %s WHERE name='%s' and passwd='%s';"%(self.table,name,pw)
        self.cur.execute(sql)

        if self.cur.fetchone():
            sql='update user set last_date=now() , state=1 , addr="%s" WHERE name="%s"'%(addr,name)
            print(sql)
            try:
                self.cur.execute(sql)
                self.db.commit()
            except Exception as e:
                self.db.rollback()
                print(e)
                return False
            else:
                return True
        else:
            return False

    def register(self,name,pw):
        sql="select * from %s WHERE name='%s'"%(self.table,name)
        self.cur.execute(sql)

        if self.cur.fetchone():
            return False
        else:
            sql="insert into %s(name,passwd,state,join_date) VALUES ('%s','%s','2',curdate());"%(self.table,name,pw)
            try:
                self.cur.execute(sql)
                self.db.commit()
            except Exception as e:
                self.db.rollback()
                print(e)
                return False
            else:
                return True




