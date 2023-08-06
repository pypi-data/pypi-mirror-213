#Rules are meant to break by proudest ones.
'''
这是亮天计划的数据库官方API。
'''
import sqlite3,sys,os,datetime,io

tor='DefyDatabase'
version='10.0.0a2'

commands=[
    'SELECT COUNT(*) FROM LIGHTSKY',
    'SELECT UID,BIND FROM BIND WHERE UID = "{}"',
    'SELECT UID, GRADE, JOB ,ABOUT FROM LIGHTSKY WHERE UID = "{}"',
    'SELECT UID, GRADE, JOB ,ABOUT from LIGHTSKY WHERE rowid={}',
    'SELECT COUNT(*) FROM BIND',
    'UPDATE LIGHTSKY SET GRADE=?,JOB=?,ABOUT=? WHERE UID=?',
    'INSERT INTO LIGHTSKY (UID,GRADE,JOB,ABOUT) VALUES (?,?,?,?)',
    'INSERT INTO BIND (UID,BIND) VALUES (?,?)',
    'DELETE FROM LIGHTSKY WHERE UID=?',
    'VACUUM']

new_c={
    'COUNT_MAIN':'SELECT COUNT(*) FROM LIGHTSKY',
    'CHECK_BIND':'SELECT UID,BIND FROM BIND WHERE UID = "{}"',
    'QUERYUID':'SELECT UID, GRADE, JOB ,ABOUT FROM LIGHTSKY WHERE UID = "{}"',
    'QUERYROW':'SELECT UID, GRADE, JOB ,ABOUT from LIGHTSKY WHERE rowid={}',
    'COUNT_BIND':'SELECT COUNT(*) FROM BIND',
    'ATEST_MAIN_2':'UPDATE LIGHTSKY SET GRADE=?,JOB=?,ABOUT=? WHERE UID=?',
    'ATEST_MAIN_1':'INSERT INTO LIGHTSKY (UID,GRADE,JOB,ABOUT) VALUES (?,?,?,?)',
    'ATEST_BIND_2':'UPDATE BIND SET BIND=? WHERE UID=?',
    'ATEST_BIND_1':'INSERT INTO BIND (UID,BIND) VALUES (?,?)',
    'DEL_MAIN':'DELETE FROM LIGHTSKY WHERE UID=?',
    'DEL_BIND':'DELETE FROM BIND WHERE UID=?',
    'CLEAN':'VACUUM'}

tablemaker=[
    """CREATE TABLE "ACTION" (
	"ABOUT"	TEXT
)""",
    """CREATE TABLE "BIND" (
	"UID"	TEXT NOT NULL,
	"BIND"	TEXT NOT NULL,
	PRIMARY KEY("UID")
)""",
    """
CREATE TABLE "LIGHTSKY" (
	"UID"	TEXT NOT NULL,
	"GRADE"	INTEGER,
	"JOB"   INTEGER,
	"ABOUT" TEXT,
	PRIMARY KEY("UID")
)"""]

def add(toadd,adding,back=True,blank=False):
    if back:
        if blank:
            return str(toadd)+' '+str(adding)
        else:
            return str(toadd)+str(adding)
    else:
        if blank:
            return str(adding)+' '+str(toadd)
        else:
            return str(adding)+str(toadd)
        



#数据库管理对象。
class __DefyProject(io.IOBase):   
    def __reset(self):
        self.__con=sqlite3.connect(self.__file)
        self.__cur=self.__con.cursor()
        self.__fro=0
        
    def __run__qe(self,command,inf=None):
        res=False
        try:
            if inf:
                self.__cur.execute(command,inf)
            else:
                self.__cur.execute(command)
            res=self.__cur.fetchall()
        except BaseException as e:
            res=e
        finally:
            return res
        
    def __run__au(self,command,inf=None):
        m=0
        try:
            if inf:
                self.__cur.execute(command,inf)
            else:
                self.__cur.execute(command)
            self.__con.commit()
        except BaseException as e:
            m=e
            self.__con.rollback()
        return m

    def __add(self,n):
        for i in n:
            if i[2] is None:
                if i[3] is None:
                    self.__run__au(commands[6],[i[0],i[1],0,'无'])
                else:
                    self.__run__au(commands[6],[i[0],i[1],0,i3])
            else:
                if i[3] is None:
                    self.__run__au(commands[6],[i[0],i[1],i[2],'无'])
                else:
                    self.__run__au(commands[6],[i[0],i[1],i[2],i[3]])

    def __upd(self,n):
        for i in n:
            if i[2] is None:
                if i[3] is None:
                    self.__run__au(commands[5],[i[1],0,'无',i[0]])
                else:
                    self.__run__au(commands[5],[i[1],0,i[3],i[0]])
            else:
                if i[3] is None:
                    self.__run__au(commands[5],[i[1],i[2],'无',i[0]])
                else:
                    self.__run__au(commands[5],[i[1],i[2],i[3],i[0]])

    def __init__(self,file):
        self.__file=file
        self.__reset()
        m2=self.__run__qe(commands[0])
        m3=self.__run__qe(commands[4])
        if type(m2)!=type('list') or type(m3)!=type('list'):
            for i in tablemaker:
                self.__run__au(i)
                        
    def __repr__(self):
        return '<DefyDatabase {}>'.format(self.__file)

    def fetch(self,uid):
        res=False
        m2=self.__run__qe(commands[1].format(uid))
        if m2!=[]:
            uid=m2[0][1]
        res=self.__run__qe(commands[2].format(uid))
        return res


    def bind(self,main,new):
        if not self.queryuid(main):
            raise OSError('Not written main')
        self.__run__au(commands[-3],[new,main])


    def atest_one(self,a,b,c,d):
        m2=self.__run__qe(commands[1].format(a))
        if m2!=[]:
            a=m2[0][1]
        i=[[a,b,c,d]]
        if not self.queryuid(a):
            self.__add(i)
        else:
            self.__upd(i)
            
    def atest_many(self,n):
        for i in n:
            self.atest_one(i[0],i[1],i[2],i[3])

    def atest_percent(self,uid,p=1):
        m=self.queryuid(uid)
        if m==[]:
            return 0
        self.atest_one(m[0][0],m[0][1]+p,m[0][2],m[0][3])
        del m
    

    def count(self,main=True,bind=True):
        make=0
        if main:
            make+=self.__run__qe(commands[0])[0][0]
        if bind:
            make+=self.__run__qe(commands[4])[0][0]
        return make
        
    def close(self):
        self.__cur.close()
        self.__con.close()


def open(file):
    return __DefyProject(file)

def atest_defy():
    with open('a.db') as a:
        a.atest_many([['1',1,0,'0'],['2',50,0,'0'],['3',62,0,'0']])
        print('应当："1"为1%，"2"为50%,"3"为62%')
        print(a.queryuid('1'))
        print(a.queryuid('2'))
        print(a.queryuid('3'))
        print()
        a.atest_percent('1')
        print('应当："1"为2%')
        print(a.queryuid('1'))
        print()
        a.atest_percent('1',50)
        print('应当："1"为52%')
        print(a.queryuid('1'))
        print()
        a.atest_percent('1',-20)
        print('应当："1"为32%')
        print(a.queryuid('1'))
        a.atest_percent('1',-50)
        print('应当："1"为-18%')
        print(a.queryuid('1'))

def atest_speed(num=1000):
    m=[]
    tr=datetime.datetime.now()
    for i in range(1,num+1):
        m.append([str(i),i,i,str(i)])
    with open('a.db') as a:
        a.atest_many(m)
    print(datetime.datetime.now()-tr)
    del m
    
    a=open('a.db')
    m=[]
    tr=datetime.datetime.now()
    for i in range(1,num+1):
        a.atest_one(str(i),i,i,str(i))
    print(datetime.datetime.now()-tr)
    
    tr=datetime.datetime.now()
    for i in range(1,num+1):
        a5=a.queryuid(str(i))
    print(datetime.datetime.now()-tr)
    a.close()
    del a
