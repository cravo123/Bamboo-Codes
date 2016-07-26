# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 20:56:28 2015
This code will scrape short-term trade of insider management from Shenzhen Exchange website, and save it to a csv file.
pth is the savind directory, the format is like 'C:\\Users\\Chong\\Desktop\\Bamboo Strategy\\InsiderTrade'
startPage is where the scraping starts, and interval is how many pages this code will scrape.
so in total this code will scrape [startPage, startPage + interval).

@author: Chong

"""

from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import random
import requests
import json

def GrabInsiderShareChangeSH(pth, startPage, interval = 2):
    # choose a random browser to pretend    
    rd = random.randint(1, 2)
    if rd == 1:    
        values = {'User-Agent':'''Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X)
                  AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25'''}
    else:
        values = {'User-Agent':'''Mozilla/5.0 (Windows NT 6.3; Win64; x64)
                  AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36'''}
    # df is a dataframe to save all the clean-data
    df = pd.DataFrame()    
    
    for k in range(startPage, startPage + interval):
        url = 'http://www.sse.com.cn/disclosure/listedinfo/credibility/change/'
        print(url + '  ' + str(k) + '  Open')
        
        # Set post form data to turn to next page        
        Page_data = {'pageHelp.pageNo': '6'}        
        
#        req = urllib.request.Request(url, headers = values)
        req = requests.post(url, headers = values, params = Page_data)
        print(req.url)
        data = req.content
        print(data)
        # Potential Decoding Problem
        data = data.decode('utf-8')
        
        bs = BeautifulSoup(data)
        elms = bs.select('table.tablestyle')
        
        raw_data = []
        temp_data = []
        j = 0
        for tt in elms: 
                    
            tt = tt.find_all('td', {'class':'nowrap'})
            
            for ss in tt:
                print(ss)
##                raw_data.append(ss.text)
#                m = j % 13                
#                if m in range(6, 10):
#                    # Get rid of the document string                    
#                    temp_str = ss.text.strip()
#                    temp_str = temp_str.split('(')[2]
#                    temp_str = temp_str.split(',')[0]
#                    temp_str = temp_str.strip('\'')
#                    
#                    # Convert string to int or float                    
#                    if m == 8:                  
#                        try:                        
#                            temp_data.append(float(temp_str))
#                        except:
#                            temp_data.append(int(temp_str))
#                    else:
#                        try:                        
#                            temp_data.append(int(temp_str))
#                        except:
#                            temp_data.append(float(temp_str))
#                
#                elif m in range(11, 13):
#                    # tranform string to date format                        
#                    try:                        
#                        temp_str = ss.text.split('-')
#                        temp_str = temp_str[1] + '/' + temp_str[2] + '/' + temp_str[0]
#                        temp_str = (datetime.strptime(temp_str,'%m/%d/%Y')).date()
#                        temp_data.append(temp_str)
#                    except:
#                        continue
#                    
#                    if m == 12:
#                        raw_data.append(temp_data)
#                        temp_data = []
#                else:                        
#                    temp_data.append(ss.text)
#                j = j + 1
#        
#        raw_data = pd.DataFrame(raw_data)
#
#        df = df.append(raw_data, ignore_index = True)
#        print(url + '  ' + str(k) + '  Done')        
#        
#    df.columns = ['Ticker', 'Stock', 'Management', 'ManagementLevel', 'StockType', 'Currency', 'NumOfSharesPrior', 
#                  'NumOfSharesChange', 'Price', 'NumOfSharesPost', 'Reason', 'TradeDate', 'PostDate']
##     Align the column order
#    df = df[['Ticker', 'Stock', 'TradeDate', 'PostDate', 'NumOfSharesChange', 'NumOfSharesPrior', 'NumOfSharesPost', 
#             'Price', 'Management', 'ManagementLevel', 'StockType', 'Reason', 'Currency']]
#    
#    # Add a scraping time stamp    
#    df['ScrapeDate'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#    pth = pth + '\\' + str(datetime.today().date()) + '_' + str(startPage) + '.csv'
##    df.to_csv(pth)
#    return df

if __name__ == '__main__':
    aa = GrabInsiderShareChangeSH(r'C:\Users\Chong\Desktop\Bamboo Strategy\InsiderShareChange',1)
