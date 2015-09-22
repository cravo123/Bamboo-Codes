# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 20:56:28 2015
This code will scraping short-term trade of insider management from Shenzhen Exchange website, and save it to a csv file.
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

def GrabInsiderShareChangeSZ(pth, startPage, interval = 5):
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
        url = 'http://www.szse.cn/main/disclosure/jgxxgk/djggfbd/'
        print(url + '  ' + str(k) + '  Open')
        
        # Set post form data to turn to next page        
        Page_data = {'tab1PAGENUM':str(k)}        
        
#        req = urllib.request.Request(url, headers = values)
        req = requests.post(url, headers = values, data = Page_data)        
        
        data = req.content
#        print(data)
        # Potential Decoding Problem
        data = data.decode('gbk')
        
        bs = BeautifulSoup(data)
        elms = bs.select('table.cls-data-table')
        
        raw_data = []
        temp_data = []
        j = 0
        for tt in elms:            
            tt = tt.find_all('td', {'class':'cls-data-td'})
            
            for ss in tt:
                m = j % 12                
                if m != 11:
                    if m == 3:
                        # tranform string to date format                        
                        try:                        
                            temp_str = ss.text.split('-')
                            temp_str = temp_str[1] + '/' + temp_str[2] + '/' + temp_str[0]
                            temp_str = (datetime.strptime(temp_str,'%m/%d/%Y')).date()
                            temp_data.append(temp_str)
                        except:
                            continue
                    else:                        
                        temp_data.append(ss.text)
                    
                elif m == 11:
                    temp_data.append(ss.text)
                    raw_data.append(temp_data)
                    temp_data = []
                j = j + 1
        raw_data = pd.DataFrame(raw_data)
        df = df.append(raw_data, ignore_index = True)
        print(url + '  ' + str(k) + '  Done')        
        
    df.columns = ['Ticker', 'Stock','Management', 'TradeDate', 'NumOfSharesChange', 'Price', 'TradeType', 
                  'PercentageChange', 'TotalShares', 'PersonInAction', 'ManagementLevel', 'Relationship']
    # Align the column order
    df = df[['Ticker', 'Stock', 'TradeDate', 'NumOfSharesChange', 'Price', 'TradeType', 'PercentageChange', 
             'TotalShares', 'Management', 'ManagementLevel', 'PersonInAction', 'Relationship']]
    
    # Add a scraping time stamp    
    df['ScrapeDate'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pth = pth + '\\' + str(datetime.today().date()) + '_' + str(startPage) + '.csv'
    df.to_csv(pth)

if __name__ == '__main__':
    aa = GrabInsiderShareChangeSZ(r'C:\Users\Chong\Desktop\Bamboo Strategy\InsiderShareChange',1)
