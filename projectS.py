#!/usr/bin/env python
# coding: utf-8

# In[1]:


#-*- coding:utf-8 -*-
from commonTool import *
from config import *

# Parameter 설정
set_enc_param(encParamKey)

print('enc_param', enc_param_value)
print('codeFile', codePathFile)
print('outputFolder', outputRawPath, flush=True)


# https://kind.krx.co.kr/corpgeneral/corpList.do?method=loadInitPage --> 메뉴 중 상장법인 목록
# 위에서 Excel로 내려 받은 파일임
# (code 목록, 업종 목록, 업종별 대표 코드 목록)을 반환.
def getCompanyCodeFromFile():
    codes = []
    types = []
    referCodes = []
    referChecker = {}

    fileCodes = open(codePathFile, 'r', encoding='utf-8')
    line = fileCodes.readline() # Title
    
    while True:
        line = fileCodes.readline()
        if not line:
            break

        line = line.strip()
        if len(line) <= 0:
            continue

        items = line.split('\t')
        
        codes.append(items[1])
        types.append(items[2])
        
        if not items[2] in referChecker:
            referChecker[items[2]] = items[1]
            referCodes.append(items[1])

    fileCodes.close()
    
    return (codes, types, referCodes)



# 데이터명 분석을 위한 데이터 페치
def doFetchDataNames(referenceCodes, outPath, fetchType, funcGet):
    print(fetchType, 'doing...', flush=True)
    deli = '\t'
    # keyNames = ['ACCODE', 'ACC_NM', 'UNT_TYP', 'P_ACCODE', 'DATA1', 'DATA2', 'DATA3', 'DATA4', 'DATA5']
    valueColumns = ['DATA1', 'DATA2', 'DATA3', 'DATA4', 'DATA5']

    out = open(outPath + fetchType + '-accNames.txt', 'w', encoding='utf-8')
    out.write('PCODE' + deli + 'ACCODE' + deli + 'NAME' + deli + 'P_ACCODE\n')

    for code in referenceCodes:
        # print('fetching', code, flush=True)
        resp = funcGet(code)

        if resp.status_code == 200:
            # print(resp.text, flush=True)
            obj = json.loads(resp.text)
            if obj is None: continue
            
            data = obj['DATA']
            if data is None:
                continue

            accodeMap = {}
            
            for rec in data:
                if not rec['ACCODE'] in accodeMap:
                    accNm = rec['ACC_NM'].lstrip('.').lstrip('*')
                    accodeMap[rec['ACCODE']] = { 'name': accNm, 'pCode': rec['P_ACCODE'] }
                    
            # 추출한 데이터 명칭 저장
            
            for key in accodeMap.keys():
                elem = accodeMap[key]
                accNm = elem['name']
                
                out.write(code)
                out.write(deli)
                out.write(key)
                out.write(deli)
                out.write(accNm if elem['pCode'] is None else accodeMap[elem['pCode']]['name'] + '/' + accNm)
                out.write(deli)
                out.write('' if elem['pCode'] is None else elem['pCode'])
                out.write('\n')
            
        else:
            print('fetch error ', code, resp.status_code)

    out.close()
    print(fetchType, 'done...', flush=True)

    
# codeList: 데이터를 가져올 회사 코드 목록
# outFile: 결과를 저장할 파일
# accCheck: 크롤링할 데이터 항목 맵. 항목 코드 --> 컬럼 위치
# accCount: 데이터 항목 개수
# funcGet: 크롤링 함수
def crawlCompFinancials(codeList, outFile, accCheck, accCount, funcGet):
    deli = '\t'
    valueColumns = ['DATA1', 'DATA2', 'DATA3', 'DATA4', 'DATA5']
    
    dataSet = [] # 크롤링 데이터 저장
    for code in codeList:
        print('fetching', code, flush=True)
        resp = funcGet(code)

        if resp.status_code == 200:
            # print(resp.text, flush=True)
            obj = json.loads(resp.text)
            if obj is None: continue
            
            # DATA1 ~ DATA5의 기준 년월
            yearName = [T[0:T.find('<')] for T in obj['YYMM']][0:len(valueColumns)]

            data = obj['DATA']
            if data is None:
                continue

            items = [extendList([code, title], accCount + 2) for title in yearName] # DATA1, ..., DATA4
            
            for rec in data:
                if not rec['ACCODE'] in accCheck:
                    accCheck[rec['ACCODE']] = len(accNames)
                    accNm = rec['ACC_NM'].lstrip('.').lstrip('*')
                    accNames.append(accNm if rec['P_ACCODE'] is None else accNames[accCheck[rec['P_ACCODE']]] + '/' + accNm)
                    accItems.append([rec['ACCODE'], accNames[-1], rec['P_ACCODE']])
                    items = [extendList(T, len(accNames) + 2) for T in items]

                # 저장할 위치
                valCol = accCheck[rec['ACCODE']] + 2
                
                for c in range(0, len(items)):
                    items[c][valCol] = rec[valueColumns[c]]

            # 결과 저장용 배열에 추가
            dataSet.extend(items)
        else:
            print('fetch error ', code, resp.status_code)

    # 추출한 데이터 저장
    for rec in dataSet:
        if rec[2] is None:
            continue

        for i in range(0, len(rec)):
            v = rec[i]
            if i > 0: outFile.write(deli)
            outFile.write('' if v is None else str(v))
        outFile.write('\n')

    # end of crawlCompFinancials
    return True


# In[ ]:





# In[2]:


# 1. 데이터를 가져올 회사 정보 가져 오기
jobName = 'setup company codes'
begin(jobName)

(codes, types, referCodes) = getCompanyCodeFromFile()
print('codes', len(codes), len(types), len(referCodes)) # 첫 번째, 두 번째 값 같아야 함.

end(jobName)


# In[ ]:





# In[ ]:


# 2. 업종별 재무 데이터 항목 가져와 파일에 저장하기 (매번 수행할 필요 없음)
# 최종 필요한 파일은 Step 3에서 생성되는 파일로 여기서 crawling하는 데이터는 임시 폴더에 넣음

jobName = 'crawling data name'
begin(jobName)

print('reference codes count: ', len(referCodes))
fetchFunc = { 'annualBS': fetchFinacialData, 'annualCF': fetchCashFlowData, 'annualPL': fetchProfitLossData }

for dataType in fetchFunc.keys():
    doFetchDataNames(referCodes, temporaryPath, dataType, fetchFunc[dataType])

end(jobName)


# In[ ]:





# In[4]:


# 3. 2에서 가져온 재무 항목 정리 (매번 수행할 필요 없음)
# Crawlego 스크립트 실행 (AC-CODE-SAVE.xml)
# ./resource 폴더 내 accCodes-XX.txt 파일 생성 (XX: BS, CF, PL)

jobName = '데이터 항목명 정리 작업'
begin(jobName)

# IN_PATH(temporaryPath), OUT_PATH (resourceDir), TYPE(BS, CF, PL)
scriptPathName = crawlegoScriptPath + 'AC-CODE-SAVE.xml'

for typeStr in ['BS', 'CF', 'PL']:
    cmdStr = 'java -Dfile.encoding=utf8 -Duser.timezone=GMT -jar ' + crawlegoPath + ' ' + scriptPathName         + ' IN_PATH=' + temporaryPath + ' OUT_PATH=' + resourceDir + ' TYPE=' + typeStr
    retCode = os.system(cmdStr)
    print('Type', typeStr, 'processed.', 'return code', retCode, flush=True)

end(jobName)


# In[ ]:





# In[3]:


# 4. 3에서 분석된 재무 항목을 업종별 컬럼목록 객체로 변환하여 반환

jobName = '수집 대상 항목 메모리 로딩'
begin(jobName)

# 데이터 종류별 --> 업종별 --> 데이터 항목 { accMap: 컬럼코드 --> 인덱스, accNames: 컬럼명 목록 }
columnsMap = {}

for typeStr in ['BS', 'CF', 'PL']:
    columnNameFile = resourceDir + 'accCodes-' + typeStr + '.txt'

    file = open(columnNameFile, 'r', encoding='utf-8')
    line = file.readline() # Title

    cMap = {}


    while True:
        line = file.readline()
        if not line:
            break

        line = line.strip()
        if len(line) <= 0:
            continue

        # 업종구분, ACCODE, NAME, P_ACCODE
        items = line.split('\t')

        if not items[0] in cMap:
            cMap[items[0]] = { 'accMap':{}, 'accNames':[] }

        theItem = cMap[items[0]]

        theItem['accMap'][items[1]] = len(theItem['accNames'])
        theItem['accNames'].append(items[2])

    file.close()
    columnsMap[typeStr] = cMap

    print('Type', typeStr, 'processed.', flush=True)

# print(columnsMap)

end(jobName)


# In[ ]:





# In[15]:


# 5. 회사별 재무제표 가져오기 업종에 따라 다른 파일에 저장됨.

# 데이터 페치 함수 정의
fetchFuncMap = { 'annualBS': fetchFinacialData, 'annualCF': fetchCashFlowData, 'annualPL': fetchProfitLossData,
    'quarterBS': fetchQuaterFinacialData, 'quarterCF': fetchQuaterCashFlowData, 'quarterPL': fetchQuaterProfitLossData }

# codes, types --> 업종별 코드 목록
categoricCodes = {}
# for i in range(0, len(codes)):
for i in range(0, 10):
    if not types[i] in categoricCodes:
        categoricCodes[types[i]] = []
    
    categoricCodes[types[i]].append(codes[i])

begin('crawing financial data')
for typeStr in ['BS', 'CF', 'PL']:
    tmpMap = columnsMap[typeStr]

    for typeKey in categoricCodes.keys():
        codeList = categoricCodes[typeKey]
        mapKey = 'BASIC'
        keyIndex = 9
        idx = 0
        for s in tmpMap.keys():
            if -1 != s.find(typeKey + ';'):
                mapKey = s
                keyIndex = idx
                break
            idx += 1

        accMap = tmpMap[mapKey]
    
        for periodStr in ['annual', 'quarter']:
            dataType = periodStr + typeStr
            
            begin(dataType)
            
            deli = '\t'
            outFile = open(outputRawPath + dataType + '-' + str(keyIndex) + '.txt', 'w', encoding='utf-8')
            outFile.write('P_CODE' + deli + 'TERM')
            
            for nn in accMap['accNames']:
                outFile.write(deli)
                outFile.write(nn)

            outFile.write('\n')
            
            crawlCompFinancials(codeList, outFile, accMap['accMap'], len(accMap['accNames']), fetchFuncMap[dataType])

            outFile.close()
            end(dataType)

end('crawing financial data')
# end of category loop


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




