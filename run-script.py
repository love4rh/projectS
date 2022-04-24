#-*- coding:utf-8 -*-
from commonTool import *


momentumDataPath = outputRawPath + 'momentum' + os.path.sep
scriptPathName = crawlegoScriptPath + 'EVALUATE-MM-UPLOAD.xml'

parameter = {
    'IN_PATH': momentumDataPath,
    'DO_SERVER': dataOnServerIP
}

print('ret code', runDashScript(scriptPathName, parameter))

