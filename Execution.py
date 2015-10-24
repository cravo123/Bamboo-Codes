import MySQLdb
from WindPy import w
from datetime import *


def do_trade_sell(record):
   print record
   #trade_result = w.torder(record[0],"Buy",record[1],record[2],"OrderType=LMT;HedgeType=SPEC")  
   if trade_result != 0
       #log this error print "do_trade fail and trade_result is %d" % trade_result
   else
       sold = ...#get sold volume from wind or local ?
       Total_account += sold;


def do_trade_buy(record,volume):
   print record
   #trade_result = w.torder(record[0],"Buy",record[1],record[2],"OrderType=LMT;HedgeType=SPEC")  
   if trade_result != 0
       #log this error print "do_trade fail and trade_result is %d" % trade_result
   else
       #sold = ...#get sold volume from wind or local ?
       Total_account -= sold;
 
def TradeToday():    
    try:
        dictionary=[] 
        Bamboo_db = MySQLdb.connect(host='localhost',user='root',passwd='root',db='Bamboo',port=3306)
        cur = Bamboo_db.cursor()

        sell_count = cur.execute('select * from TradeToday_SellDict')
        print 'there are %d raws record in TradeToday_SellDict' % count

        sell_list = cur.fetchall()
        for r in sell_list:
            do_trade_sell(r)
            try:
                cur.execute('delete from SellDict where Stock = '%s'' % r[1])
                Bamboo_db.commit()
            except:
                Bamboo_db.rollback()
                #log this error
    
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0],e.args[1])


    try:
        buy_count = cur.execute('select * from TradeToday_BuyDict')  
        print 'there are %d raws record in BuyDict' % count

        Account_per_stock = Total_account/buy_count

        buy_list = cur.fetchall()

        for r in buy_list:
            volume = Account_per_stock/r[4]
            do_trade_buy(r,volume)
            try:
                cur.execute('delete from BuyDict where Stock = '%s'' % r[1])
                cur.execute('delete from CurretPosition where Stock = '%s'' % r[1])
                cur.execute('insert into TradeHistory(Ticker,Stock,TradeDate,Broker,Price,Volume,Total Cost) values(r,%d)' % total_cost)#get total_cost from wind or local?
                Bamboo_db.commit()
            except:
                Bamboo_db.rollback()
                #log this error

    finally:
        if Bamboo_db:
            Bamboo_db.close()
