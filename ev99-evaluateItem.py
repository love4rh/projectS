#-*- coding:utf-8 -*-
from commonTool import *
import glob


# 로직 적용한 결과 정리
def makeAnalysisReport(resultFolder, initialCash, period, feeRate = 0.015, withProcess = True):
    statResult = [f for f in glob.glob(resultFolder + '*-STAT.txt')]
    
    if len(statResult) == 0:
        print('no result file')
        return
    
    statResult.sort()
    
    m = 0
    y = 0
    cash = initialCash
    maxV = initialCash
    maxMdd = 0
    cagr = 0
    
    if withProcess:
        print('\t'.join(['Year', '매수일', '매도일', '손익', '투자금', '수익률', 'CAGR', 'MDD']))
    
    for statPath in statResult:
        m += period
        
        sf = open(statPath, 'r', encoding='utf-8')
        lineText = sf.readline() # 제목: --> 매수일, 매도일, R_SUM
        lineText = sf.readline() # 결과
        
        rec = lineText.split('\t')
        profitLoss = int(rec[2])

        newCash = round((cash + profitLoss) * (1.0 - feeRate))

        maxV = max(maxV, newCash)
        if newCash < cash:
            mdd = (newCash - maxV) / maxV
            maxMdd = min(mdd, maxMdd)

        y = m / 12
        cagr = pow(newCash / initialCash, 1 / y) - 1
        cagr = round(cagr * 100, 2)
        
        if withProcess:
            print('\t'.join([str(y), rec[0], rec[1],
                format(profitLoss, ',d').rjust(12), format(newCash, ',d').rjust(15),
                str(round(profitLoss / cash * 100, 2)).rjust(9), str(cagr).rjust(9), str(round(maxMdd * -100, 2))]))

        sf.close()
        cash = newCash

    if withProcess: print('')
    print('Year:', y, '  Invest:', format(initialCash, ',d'), '  Cash:', format(cash, ',d'),
        '  CAGR:', cagr, '%', '  Max MDD:', round(maxMdd * -100, 2), '%\n\n')

################################################################################


# 기준일 로딩

bf = open(resourceDir + 'BASIS-DAYS.txt', 'r', encoding='utf-8')

# 0.YYYYMM, 1.FIRST_DAY, 2.SECOND_DAY, 3.PREV_DAY, 4.LAST_DAY, 5.NEXT_DAY
lineText = bf.readline() # 제목

basisDays = []
quaterBasisDays = []

while True:
    lineText = bf.readline()
    if not lineText:
        break
        
    lineText = lineText.strip()
    if len(lineText) <= 0:
        continue

    dayData = lineText.split('\t')
    
    if dayData[0][0:4] == '2012' or dayData[0] == '201301': continue # 데이터 부족
        
    basisDays.append([dayData[0], dayData[3], dayData[4]])
    
    if dayData[0] > '202001':
        quaterBasisDays.append([dayData[0], dayData[3], dayData[4]])

bf.close()


# Evaluation
# 년간 재무 데이터를 이용한 분석

analId = '4PXX'  # 로직명: 4PXX, MAGIC, %PXR, RND
calcDate = yyyymm() # 로직 실행할 대상 월 '202107'

# sys.argv[0] 은 python 파일

if len(sys.argv) > 1:
    analId = sys.argv[1]
    
if len(sys.argv) > 2:
    calcDate = sys.argv[2]

print('running', analId, calcDate)

cash = 10000000  # 초기 투자금
period = 6  # 리밸런싱 기간 (월)
buyCount = 10  # 매수 종목 개수
totalAmount = 25 # 25 # 시가총액 하위 퍼센트 조건
volumeLimit = 10000 # 10000 # 거래량 조건
startMonth = 2

analTitle = analId + '-' + str(totalAmount) + '-' + str(round(volumeLimit / 1000)) + 'T-' + str(buyCount) \
    + '-M' + str(startMonth) + ('-P' + str(period) if period != 6 else '')

# 로직 스크립트
scriptPathName = crawlegoScriptPath + 'ANAL-' + analId + '.xml'

# 결과 저장 위치
resultFolder = outputRawPath + 'logicResult' + os.path.sep + analTitle + os.path.sep
# [os.remove(f) for f in glob.glob(resultFolder + '*.txt')]
mkdir(resultFolder)


done = False
for basis in basisDays:
    if basis[0] != calcDate: continue
    
    parameter = {
        'BASIS_DAY': basis[1],
        'BUY_DAY': basis[2],
        'SELL_DAY': basis[2],
        'CASH': str(cash),
        'TOP_N': str(buyCount),
        'PERIOD': 'ANNUAL',
        'IN_PATH': outputRawPath + 'index' + os.path.sep + (os.path.sep if runServerType == 1 else ''),
        'OUT_PATH': resultFolder + (os.path.sep if runServerType == 1 else ''),
        'TOTAL_AMOUNT': str(totalAmount),
        'VOL_LIMIT': str(volumeLimit),
        'DO_SERVER': dataOnServerIP
    }
    
    print(basis, 'running...')
    retCode = runDashScript(scriptPathName, parameter, False)
    print(basis, 'returns', retCode)
    done = True
    break

if not done:
    print('invalid argument', analId, calcDate)
else:
    print('result folder:', resultFolder)


