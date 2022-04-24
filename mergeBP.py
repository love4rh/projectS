#-*- coding:utf-8 -*-
from commonTool import *


resultFolder2 = outputRawPath + 'stat' + os.path.sep

print('second step running...')
scriptPathName = crawlegoScriptPath + 'GUESS-BP-MERGE.xml'
parameter = {
    'IN_PATH': resultFolder2 + (os.path.sep if runServerType == 1 else ''),
    'OUT_PATH': resourceDir,
    'DO_SERVER': dataOnServerIP 
}

runDashScript(scriptPathName, parameter, False)
    
print('done')

