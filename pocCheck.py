#-*- coding:utf-8 -*-
from commonTool import *
import glob


# 1. 데이터를 가져올 회사 정보 가져 오기
jobName = 'setup company codes'
begin(jobName)

guessBPFile = resourceDir + 'guessBPItem.txt'
(codes, types, referCodes) = getCompanyCodeFromFile(guessBPFile)
print('codes', len(codes), len(types), len(referCodes)) # 첫 번째, 두 번째 값 같아야 함.

end(jobName)


# 2. 계산
# 로직 스크립트
scriptPathName = crawlegoScriptPath + 'POC-CHECK.xml'

# 결과 저장 위치
resultFolder = outputRawPath + 'chartData' + os.path.sep
resultFolder2 = outputRawPath + 'stat' + os.path.sep

mkdir(resultFolder)
mkdir(resultFolder2)

[os.remove(f) for f in glob.glob(resultFolder2 + 'ST*.txt')]


for code in codes:
    parameter = {
        'COMP_CODE': code,
        'OUT_PATH': resultFolder + (os.path.sep if runServerType == 1 else ''),
        'OUT_PATH2': resultFolder2 + (os.path.sep if runServerType == 1 else ''),
        'DO_SERVER': dataOnServerIP
    }
    
    print(code, 'running...')
    retCode = runDashScript(scriptPathName, parameter, False)
    print(code, 'returns', retCode)

print('done')

