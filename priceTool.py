#!/usr/bin/env python
# coding: utf-8

# In[1]:


#-*- coding:utf-8 -*-
from commonTool import *
from config import *

import sys


# In[ ]:





# In[2]:


outputDirPath = outputRawPath + 'priceDaily' + os.path.sep
mkdir(outputDirPath)


# In[ ]:





# In[3]:


d = dt.datetime.today()
# d = d - dt.timedelta(days=1)
dayNo = d.strftime('%Y%m%d')

if len(sys.argv) >= 2:
   dayNo = sys.argv[1]

writeDailyPriceFromKRX(dayNo, outputDirPath)


# In[ ]:




