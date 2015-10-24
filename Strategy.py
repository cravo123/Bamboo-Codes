import MySQLdb
from WindPy import w
from datetime import *
from Execution import *

LogonID = w.tlogon("00000010","","M:1881053498701","******","SHSZ")

try:
    WhiteList=[]
    CurrentPosition=[]
    Bamboo_db = MySQLdb.connect(host='localhost',user='root',passwd='root',db='Bamboo',port=3306)
    cur = Bamboo_db.cursor()

    #Get record in WhiteList table and store them into array WhiteList
    WhiteList_count = cur.execute('select * from WhiteList')
    print 'there are %d raws record in WhiteList' % count

    WhiteList_results = cur.fetchall()
    for r in White_results:
        WhiteList.append(r[0])

    print WhiteList

    #Get record in CurrentPosition table and store them into array CurrentPosition
    CurrentPosition_count = cur.execute('select * from CurrentPosition')
    print 'there are %d raws record in Position' % count

    CurrentPosition_results = cur.fetchall()
    for r in CurrentPosition_results:
        CurrentPosition.append(r[0])
    print CurrentPosition
    
    #Get record in Research table     
    Research_count = cur.execute('select * from Research')
    print 'there are %d raws record in Research' % count

    Research_results = cur.fetchall()
    for record in Research_results:
        if record[0] in CurrentPosition:
           cur.execute('delete Resarch where Stock=%s' % record[0])
        else if record[0] in WhiteList:
           #cur.execute('insert into TradeToday(Ticker,Stock,TradeDate,Broker,Price,Volume,Total Cost) values(r)' )#to be modified
            cur.execute('delete Resarch where Stock=%s' % record[0])

    cur.execute('delete * from Resaerch')
    Bamboo_db.commit()
            
    TradeToday_count = cur.execute('select * from TradeToday')
    print 'there are %s raws record in TradeToday' % TradeToday_count

    Trade_Today() 

except MySQLdb.Error,e:
    print "Mysql Error %d: %s" % (e.args[0],e.args[1])

finally:
    if Bamboo_db:
        Bamboo_db.close()

w.tlogout(LogonID = "0")
