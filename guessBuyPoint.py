#-*- coding:utf-8 -*-
from commonTool import *
import glob


doServer = dataOnServerIP

# doServer = "127.0.0.1"

priceFolder = resourceDir + 'price' + os.path.sep
mkdir(priceFolder)

'''
# 0-1. 최근 가격 준비
jobName = 'cache price'
begin(jobName)

parameter = {
    'YEAR': '2021',
    'OUT_PATH': priceFolder + (os.path.sep if runServerType == 1 else ''),
    'DO_SERVER': doServer
}

runDashScript(crawlegoScriptPath + 'CACHE-PRICE.xml', parameter, False)
end(jobName)

# 0-2. 코드 준비
jobName = 'prepare codes'
begin(jobName)

parameter = {
    'RES_PATH': resourceDir + (os.path.sep if runServerType == 1 else '')
}

runDashScript(crawlegoScriptPath + 'GUESS-BP-PREPARE.xml', parameter, False)
end(jobName)
'''

# 1. 데이터를 가져올 회사 정보 가져 오기
jobName = 'setup company codes'
begin(jobName)

guessBPFile = resourceDir + 'companyCodes.txt' # 'guessBPItem.txt'

codes = []
fileCodes = open(guessBPFile, 'r', encoding='utf-8')
line = fileCodes.readline() # Title

while True:
    line = fileCodes.readline()
    if not line:
        break

    line = line.strip()
    if len(line) <= 0:
        continue

    items = line.split('\t')

    codes.append(items[0])
    
fileCodes.close()
print('codes', len(codes))

end(jobName)


# 2. 계산
# 로직 스크립트
scriptPathName = crawlegoScriptPath + '_POC4_.xml'

# 결과 저장 위치
resultFolder = outputRawPath + '_chartData' + os.path.sep
resultFolder2 = outputRawPath + 'stat' + os.path.sep

mkdir(resultFolder)
mkdir(resultFolder2)

[os.remove(f) for f in glob.glob(resultFolder + '*')]
[os.remove(f) for f in glob.glob(resultFolder2 + 'GS-*.txt')]

count = 0

for code in codes:
    if not code.endswith('0') or code.startswith('9'):
        continue

    count += 1
#    if count < 860:
#        continue

    parameter = {
        'COMP_CODE': code,
        'OUT_PATH': resultFolder + (os.path.sep if runServerType == 1 else ''),
        'OUT_PATH2': resultFolder2 + (os.path.sep if runServerType == 1 else ''),
        'STAT_PATH': resultFolder2 + (os.path.sep if runServerType == 1 else ''),
        'RES_PATH': priceFolder,
        'DO_SERVER': doServer
    }

    print(count, code, 'running...')
    retCode = runDashScript(scriptPathName, parameter, False)
    print(code, 'returns', retCode)

#

print('done')

