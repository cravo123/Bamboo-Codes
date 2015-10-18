import MySQLdb
from WindPy import w
from datetime import *


LogonID = w.tlogon("00000010","","M:1881053498701","******","SHSZ")

def do_trade(record):
   print record
   #w.torder(record[0],"Buy",record[1],record[2],"OrderType=LMT;HedgeType=SPEC")  
    
try:
    dictionary=[]
    dic_conn = MySQLdb.connect(host='localhost',user='root',passwd='root',db='Dictionary',port=3306)
    cur = dic_conn.cursor()

    count = cur.execute('select * from dictionary')
    print 'there are %d raws record' % count

    results = cur.fetchall()
    for r in results:
        dictionary.append(r[0])

    print dictionary
    
except MySQLdb.Error,e:
    print "Mysql Error %d: %s" % (e.args[0],e.args[1])

finally:
    if dic_conn:
        dic_conn.close()
    
try:
    conn = MySQLdb.connect(host='localhost',user='root',passwd='root',db='Bamboo',port=3306)

    cur = conn.cursor()

    count = cur.execute('select * from Summary')
    print 'there are %s raws record in Summary' % count

    results = cur.fetchall()
    for record in results:
        if record[0] in dictionary:
            do_trade(record)

    count = cur.execute('select * from Research')
    print 'there are %s raws record in Research' % count

    results = cur.fetchall()
    for record in results:
        if record[0] in dictionary:
            do_trade(record)
        

except MySQLdb.Error,e:
    print "Mysql Error %d: %s" % (e.args[0],e.args[1])
finally:
    if conn:
        conn.close()
    
   
w.tlogout(LogonID = "0")
