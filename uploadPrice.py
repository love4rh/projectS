#-*- coding:utf-8 -*-
from commonTool import *


# start main process

jobName = 'upload price info to db'
begin(jobName)

year = today()[0:4]

if len(sys.argv) >= 2 and len(sys.argv[1]) == 4:
    year = sys.argv[1]

scriptPathName = crawlegoScriptPath + 'UPLOAD-PRICE.xml'

parameter = {
    'YEAR': year,
    'ADJ_PATH': outputRawPath + 'adjustPrice' + os.path.sep + 'adjDailyPrice',
    'KRX_PATH': outputRawPath + 'priceDaily' + os.path.sep + year + os.path.sep,
    'DO_SERVER': dataOnServerIP
}

retCode = runDashScript(scriptPathName, parameter)

end(jobName)

