#-*- coding:utf-8 -*-
from commonTool import *
import glob


resultFolder = outputRawPath + 'highlow' + os.path.sep
mkdir(resultFolder)

scriptPathName = crawlegoScriptPath + 'POC-MOMENTUM.xml'

midSizeComp = resourceDir + 'midSizeComp.txt'

mf = open(midSizeComp, 'r', encoding='utf-8')

while True:
    lineText = mf.readline()
    if not lineText:
        break
        
    lineText = lineText.strip()
    if len(lineText) <= 0:
        continue
        
    # lineText is company code
    
    parameter = {
        'COMP_CODE': lineText,
        'OUT_PATH': resultFolder,
        'DO_SERVER': dataOnServerIP
    }

    retCode = runDashScript(scriptPathName, parameter, False)
    print(lineText, 'returns', retCode)

mf.close()

