#-*- coding:utf-8 -*-
from commonTool import *

saveFolder = resourceDir + 'price' + os.path.sep
mkdir(saveFolder)

scriptPathName = crawlegoScriptPath + 'CACHE-PRICE.xml'
parameter = {
    'YEAR': sys.argv[1],
    'OUT_PATH': saveFolder + (os.path.sep if runServerType == 1 else ''),
    'DO_SERVER': dataOnServerIP 
}

runDashScript(scriptPathName, parameter, False)
    
print('done')

