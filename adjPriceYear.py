#-*- coding:utf-8 -*-
from commonTool import *


# Naver에서 수정주가를 년단위로 조회하여 저장

def writeAdjustPrice(codes, year, outFile):
    noLine = 0
    for code in codes:
        sTick = tm.time()
        noLine += 1
        print(noLine, code,'processing', flush=True)
        
        beginDay = year + '0101'
        endDay = year + '1231'

        # resp = fetchMonthStockData(code, beginDay, endDay)
        resp = fetchDailyStockData(code, beginDay, endDay)

        writeStockData(code, outFile, resp)

        print(noLine, code,'done', tm.time() - sTick, flush=True)


jobName = 'get adjust price'
begin(jobName)

(codes, types, referCodes) = getCompanyCodeFromFile(codePathFile)
print('codes', len(codes), len(types), len(referCodes)) # 첫 번째, 두 번째 값 같아야 함.


d = dt.datetime.today()
year = d.strftime('%Y')

if len(sys.argv) >= 2 and len(sys.argv[1]) == 4:
    year = sys.argv[1]

print('Fetching Year', year, flush=True)


outputDirPath = outputRawPath + 'adjustPrice' + os.path.sep
mkdir(outputDirPath)

outputDirPath += 'adjDailyPrice-' + year + '.csv'

outFile = open(outputDirPath, 'w', encoding='utf-8')
outFile.write('종목코드, 날짜, 시가, 고가, 저가, 종가, 거래량, 외국인소진율\n');

writeAdjustPrice(codes, year, outFile)

outFile.close()

end(jobName)

