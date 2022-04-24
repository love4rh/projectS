#-*- coding:utf-8 -*-
from commonTool import *


# 1. 빠른 실행을 위하여 기초 데이터 로컬에 저장해 놓기
jobName = 'prepare to evaluate index'

begin(jobName)
workingDataPath = outputRawPath
mkdir(workingDataPath)

scriptPathName = crawlegoScriptPath + 'EVALUATE-PREPARE.xml'

parameter = {
    'OUT_PATH': workingDataPath,
    'DO_SERVER': dataOnServerIP
}

print('ret code', runDashScript(scriptPathName, parameter))

end(jobName)

