# -*- coding: utf-8 -*-
"""
Created on Sat Sep 19 14:12:59 2015
This code will grab stock price data from Yahoo Finance API after given certain parameters,
which includes ticker, time duration, interval varaibles and as such.

startDate and endDate format is yyyymmdd

@author: Chong
"""

from datetime import datetime
import yahoo_finance as yh
import pandas as pd



def GrabStockData(ticker, startDate, endDate): 
    startDate = startDate[0:4] + '-' + startDate[4:6] + '-' + startDate[6:]
    endDate = endDate[0:4] + '-' + endDate[4:6] + '-' + endDate[6:]
    if(ticker[0:2] == '60'):
        ticker = ticker + '.SS'
    elif(ticker[0:2] == '00' or ticker[0:2] == '30'):
        ticker = ticker + ".SZ"
    else:
        return None
    
    ticker = yh.Share(ticker)
    
    dt = ticker.get_historical(startDate, endDate)
    
    df = pd.DataFrame(columns = ('Ticker', 'Date', 'Open', 'High', 'Low', 'Close', 'Vol'))
    i = 0
    for price in dt:
        temp_list = []        
        temp_list.append(price['Symbol'])
        temp_date = price['Date'].split('-')
        temp_date = temp_date[1] + '/' + temp_date[2] + '/' + temp_date[0]
        temp_list.append((datetime.strptime(temp_date,'%m/%d/%Y')).date())
        temp_list.append(price['Open'])
        temp_list.append(price['High'])
        temp_list.append(price['Low'])
        temp_list.append(price['Close'])
        temp_list.append(price['Volume'])
        df.loc[i] = temp_list
        i = i + 1
#    df.to_csv()
    return df


# aa = GrabStockData('601857','20150914', '20150918')
    