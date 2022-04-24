#-*- coding:utf-8 -*-
from commonTool import *
import glob


resultFolder = outputRawPath + 'logicResult' + os.path.sep + '4PXX-25-10T-10-M2' + os.path.sep
saveFolder = temporaryPath + 'analMM' + os.path.sep

scriptPathName = crawlegoScriptPath + 'CALC-MOMENTUM.xml'

mmCount = 3
analResult = [f for f in glob.glob(resultFolder + '*-RESULT.txt')]

for selFile in analResult:
    p = selFile.rfind(os.path.sep)
    basisDay = selFile[p+1:p+9]
    
    parameter = {
        'BASIS_DAY': basisDay,
        'IN_PATH': resultFolder + (os.path.sep if runServerType == 1 else ''),
        'OUT_PATH': saveFolder + (os.path.sep if runServerType == 1 else ''),
        'MM_COUNT': str(mmCount),
        'DO_SERVER': dataOnServerIP
    }

    retCode = runDashScript(scriptPathName, parameter, False)
    print(basisDay, 'returns', retCode)


