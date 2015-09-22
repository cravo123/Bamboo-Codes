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


def SummaryScrapingFromDate(dt, pth):
    dt = dt[0:4] + '/' + dt[4:6] + '/' + dt[6:8]    
    DateSearchFrom = datetime.strptime(dt,'%Y/%m/%d').date()
    # headers of request
    rd = random.randint(1,3)
    if rd == 1:    
        values = {'User-Agent':'''Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X)
                  AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25'''}
    elif rd == 2:
        values = {'User-Agent':'''Mozilla/5.0 (Windows NT 6.3; Win64; x64)
                  AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36'''}
    # Create an empty data frame
    df = pd.DataFrame()
    
    k = 1
    while (True):
        url = 'http://www.microbell.com/microns_1_' + str(k) + '.html'
        print(url + '  Open')
        req = urllib.request.Request(url, headers = values)
        
        try:        
            response = urllib.request.urlopen(req)
        except ConnectionResetError:
            response = urllib.request.urlopen(req)
        except:
            k = k + 1
            continue
        
        data = response.read()
        try:        
            data = data.decode('gb2312')
        except:
            k = k + 1            
            continue
        bs = BeautifulSoup(data)
        elms = bs.select('div.class_ul01')
        elms_string = ""
        for i in elms:
            elms_string = elms_string + str(i)
        
        bs = BeautifulSoup(elms_string) 
        elms_string = bs.find_all(['a','td'])
        
        raw_data = []
        
        for tt in elms_string:
            try:    
                raw_data.append(tt.text)
                raw_data.append(tt.attrs["title"])
            except:
                continue
        
        clean_data = []
        i = 0
        temp_data = []
        for i in range(len(raw_data) - 3):
            j = i%7    
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
        temp_df.columns = ['Broker', 'Stock', 'Ticker', 'Title', 'IssueDate', 'recommendation', 'PostDate']
        df = df.append(temp_df, ignore_index = True)
        print(url + '  Done')
        if(temp_df.PostDate[len(temp_df.PostDate) - 1] < DateSearchFrom):
            df = df[df.PostDate >= DateSearchFrom]
            df.to_csv(pth, encoding = 'utf-8')
            return
        else:
            sleep(random.randint(1,10)*0.1)            
            continue
        
        
     # Add a scraping time stamp    
    df['ScrapeDate'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df.to_csv(pth, encoding = 'utf-8')
    return None

# SummaryScrapingFromDate('20150910', r'C:\Users\Chong\Desktop\Risk Management\a.csv')