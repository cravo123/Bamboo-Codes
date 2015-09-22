# -*- coding: utf-8 -*-
"""
Created on Sat Sep 19 11:27:46 2015

@author: Chong
"""
import gc
from SummaryScrapingFromPage import SummaryScrapingFromPage

for i in range(1, 10):
    
    try:    
        SummaryScrapingFromPage(r'C:\Users\Chong\Desktop\Bamboo Strategy\Summary', i, 1)
        gc.collect()
    except ConnectionResetError:
        i = i - 1        
        continue
    except:
        i = i - 1        
        continue

