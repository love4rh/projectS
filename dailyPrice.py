#-*- coding:utf-8 -*-
from commonTool import *


def writeDailyPrice(dayNo):
    outputDirPath = outputRawPath + 'priceDaily' + os.path.sep + dayNo[0:4] + os.path.sep
    mkdir(outputDirPath)

    print('Day', dayNo, 'Output Folder:', outputDirPath, flush=True)
    writeDailyPriceFromKRX(dayNo, outputDirPath)
    

jobName = 'get daily price'
begin(jobName)

d = dt.datetime.today()

beginDay = d.strftime('%Y%m%d')
if len(sys.argv) >= 2 and len(sys.argv[1]) == 8:
    beginDay = sys.argv[1]
    d = dt.datetime.strptime(beginDay, '%Y%m%d').date()
    
endDay = beginDay
if len(sys.argv) >= 3 and len(sys.argv[2]) == 8:
    endDay = sys.argv[2]

print('range', beginDay, endDay)

while beginDay <= endDay:
    writeDailyPrice(beginDay)
    d = d + dt.timedelta(days=1)
    beginDay = d.strftime('%Y%m%d')

end(jobName)

