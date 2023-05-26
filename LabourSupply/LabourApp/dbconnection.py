import pymysql 
db=pymysql.connect(user='root',password='',host='localhost',database='laboursupply')
def addrow(sq1):
    cur=db.cursor()
    cur.execute(sq1)
    db.commit()
    
#View One
def singlerow(sq1):
    cur=db.cursor()
    cur.execute(sq1)
    data=cur.fetchone()
    return data 

#View All
def allrow(sq1):
    cur=db.cursor()
    cur.execute(sq1)
    data=cur.fetchall()
    return data
