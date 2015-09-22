# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 10:08:52 2015

@author: Chong
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

__author__ = "Chong"

import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from time import sleep
import random

def SummaryScrapingFromPage(pth, startPage, interval = 1):
    
    
    # headers of request
    rd = random.randint(1, 2)
    if rd == 1:    
        values = {'User-Agent':'''Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X)
                  AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25'''}
    else:
        values = {'User-Agent':'''Mozilla/5.0 (Windows NT 6.3; Win64; x64)
                  AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36'''}
    
    # Create an empty data frame to store scraping data
    df = pd.DataFrame()
    
    # Scraping certain pages    
    for k in range(startPage, startPage + interval):
        url = 'http://www.microbell.com/microns_1_' + str(k) + '.html'
        print(url + '  Open')
        req = urllib.request.Request(url, headers = values)
        
        # Potential Connection Problem        
        try:
            response = urllib.request.urlopen(req)
        except ConnectionResetError:
            response = urllib.request.urlopen(req)
        except:
            k = k + 1
            continue
        data = response.read()
        
        # Potential Decoding Problem
        try:        
            data = data.decode('gbk')
        except:
            k = k + 1            
            continue
        
        bs = BeautifulSoup(data)
        elms = bs.select('div.class_ul01')
        
        raw_data = []
        
        for tt in elms:
            tt = tt.find_all(['a', 'td'])
            for ss in tt:
                try:    
                    raw_data.append(ss.text)
                    raw_data.append(ss.attrs["title"])
                except:
                    continue

        clean_data = []
        temp_data = []
        for i in range(len(raw_data) - 3):
            j = i % 7    
            if j == 3:
                sl = raw_data[i].split('-')
                tt = sl[4]
                dd = tt[2:4] + '/' + tt[4:] + '/' + '20' + tt[0:2]
                sl[4] = (datetime.strptime(dd,'%m/%d/%Y')).date()
                temp_data.extend(sl)
            elif j == 4:
                temp_data.append(raw_data[i])
            elif j == 5:
                temp_data.append(datetime.strptime(raw_data[i],'%Y-%m-%d').date())
            elif j == 6:
                clean_data.append(temp_data)
                temp_data = []
        
        temp_df = pd.DataFrame(clean_data)
        k = k + 1
        temp_df.columns = ['Broker', 'Stock', 'Ticker', 'Title', 'IssueDate', 'Recommendation', 'PostDate']
        df = df.append(temp_df, ignore_index = True)
        print(url + '  Done')
        sleep(random.randint(1,10)*0.1)
    
    # Write to designated csv file
    df = df[['Ticker', 'Stock',  'Broker', 'Title', 'IssueDate', 'PostDate', 'Recommendation']]
    df['ScrapeDate'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")     
    
    pth = pth + '\\' + str(datetime.today().date()) + '_' + str(startPage) + '.csv'   
    df.to_csv(pth)
    return None
    
if __name__ == '__main__':
    aa = SummaryScrapingFromPage(r'C:\Users\Chong\Desktop\Bamboo Strategy\Summary', 7)