#!/usr/bin/env python
# coding: utf-8

# In[1]:


#-*- coding:utf-8 -*-
from commonTool import *


# In[2]:


# SP-1. 워킹 데이만 뽑아 저장하는 스크립트 실행
workingDayPath = outputRawPath + 'workingDay' + os.path.sep
mkdir(workingDayPath)

currentYear = today()[0:4]

scriptPathName = crawlegoScriptPath + 'BASIS_DATE.xml'
for year in range(2012, int(currentYear) + 1):
    if year != int(currentYear) and os.path.exists(workingDayPath + 'VD-' + str(year) + '.txt'):
        continue

    parameter = {
        'YEAR': str(year),
        'OUT_PATH': workingDayPath,
        'DO_SERVER': dataOnServerIP
    }

    print(year, 'ret code', runDashScript(scriptPathName, parameter))


# In[3]:


# SP-2. 워킹 데이 중 달별로 기준일 추출하는 스크립트 실행
# 매달 첫 째날, 둘 째날, 마지막 날, 마지막 전날 총 4일을 저장함
# resourceDir에 BASIS_DAYs.txt와 주가 쿼리를 위한 날짜 조건을 담고 있는 BASIS-CONDITION.txt 파일 생성

scriptPathName = crawlegoScriptPath + 'BASIS_DATE_MINMAX.xml'
parameter = {
    'IN_PATH': workingDayPath,
    'OUT_PATH': resourceDir
}

print('ret code', runDashScript(scriptPathName, parameter))


# In[6]:


# SP-3. SP-2의 BASIS-CONDITION.txt 파일을 읽어 해당 날짜의 주가를 쿼리하여 임시폴더에 저장함.

scriptPathName = crawlegoScriptPath + 'BASIS_STOCK_PRICE.xml'

bf = open(resourceDir + 'BASIS-CONDITION.txt', 'r', encoding='utf-8')

lineText = bf.readline() # 제목

while True:
    lineText = bf.readline()
    if not lineText:
        break
        
    lineText = lineText.strip()
    if len(lineText) <= 0:
        continue
        
    dayData = lineText.split('\t')
    
    # 금년만 계산하려면 아래 라인 살리기. 이전 년도는 BASIS가 바뀌지 않는한 변함 없음
    if dayData[0] != currentYear: continue
    
    parameter = {
        'YEAR': dayData[0],
        'OUT_PATH': temporaryPath,
        'COND': dayData[1],
        'DO_SERVER': dataOnServerIP
    }

    print(dayData[0], 'ret code', runDashScript(scriptPathName, parameter))

bf.close()


# In[ ]:





# In[8]:


# SP-4. 기준이 되는 날짜의 주가를 하나로 합쳐 DB에 업로딩.

scriptPathName = crawlegoScriptPath + 'BASIS_MERGE_PRICE.xml'

parameter = {
    'IN_PATH': temporaryPath,
    'DO_SERVER': dataOnServerIP
}

print('ret code', runDashScript(scriptPathName, parameter))


# In[ ]:




