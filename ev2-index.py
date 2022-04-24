#-*- coding:utf-8 -*-
from commonTool import *


# 2. 지표를 계산하여 저장하는 스크립트 실행
cachedDataPath = outputRawPath

workingDataPath = outputRawPath + 'index' + os.path.sep
mkdir(workingDataPath)

scriptPathName = crawlegoScriptPath + 'EVALUATE-INDEX.xml'

bf = open(resourceDir + 'BASIS-DAYS.txt', 'r', encoding='utf-8')

lineText = bf.readline() # 제목

while True:
    lineText = bf.readline()
    if not lineText:
        break
        
    lineText = lineText.strip()
    if len(lineText) <= 0:
        continue

    # 0.YYYYMM, 1.FIRST_DAY, 2.SECOND_DAY, 3.PREV_DAY, 4.LAST_DAY, 5.NEXT_DAY
    dayData = lineText.split('\t')
    if dayData[0] != yyyymm(): continue
    # if dayData[0][0:4] == '2012': continue

    parameter = {
        'IN_PATH': cachedDataPath + (os.path.sep if runServerType == 1 else ''),
        'OUT_PATH': workingDataPath + (os.path.sep if runServerType == 1 else ''),
        'RES_PATH': resourceDir,
        'PERIOD': 'ANNUAL',
        'BASIS_DATE': dayData[3], # 매달 마지막 전날을 기준으로 하자
        'DO_SERVER': dataOnServerIP
    }

    print(dayData[0], 'index ret code', runDashScript(scriptPathName, parameter))

bf.close()

