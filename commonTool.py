#-*- coding:utf-8 -*-

import requests
from requests.structures import CaseInsensitiveDict

import os
import re
import time as tm

import io
import json
from bs4 import BeautifulSoup


enc_param_value = 'UWtSVjg4a0tjL3psTkRScjMzdDFtQT09'

time_checker = {}

def begin(job):
    global time_checker
    time_checker[job] = tm.time()
    
    
def end(job):
    global time_checker
    if job in time_checker:
        print(job, 'done', tm.time() - time_checker[job], flush=True)
    else:
        print(job, 'not defined')
        

def set_enc_param(s):
    global enc_param_value
    enc_param_value = s


def debugOut(resp):
    print(resp.status_code, resp.text[:128], '...', resp.text[-128:])


# 리스트의 크기 확장
def extendList(li, n):
    if len(li) < n:
        for _ in range(0, n - len(li)):
            li.append(None)
            
    return li


def writeResponse(res, dataType, code, path):
    out = open(path + '/' + code + '-' + dataType + '.txt', 'w', encoding='utf8')
    out.write(res.text)
    out.close()

    
# 월단위 주가 정보 가져오기 (매달 말일 데이터 페치)
# 06670, 20160101, 20210430
# returns response(has status_code, text)
def fetchMonthStockData(code, start, end):
    url = 'https://api.finance.naver.com/siseJson.naver?symbol=' + code + '&requestType=1&startTime=' + start + '&endTime=' + end + '&timeframe=month'
    
    headers = CaseInsensitiveDict()
    headers['accept'] = '*/*'
    headers['accept-encoding'] = 'gzip, deflate, br'
    headers['accept-language'] = 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'
    headers['origin'] = 'https://finance.naver.com'
    headers['referer'] = 'https://finance.naver.com/item/fchart.nhn?code=' + code
    headers['sec-ch-ua'] = '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"'
    headers['sec-ch-ua-mobile'] = '?0'
    headers['sec-fetch-dest'] = 'empty'
    headers['sec-fetch-mode'] = 'cors'
    headers['sec-fetch-site'] = 'same-site'
    headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'
    headers['Content-Type'] = 'application/x-www-form-urlencoded'

    data = 'symbol=' + code + '&requestType=1&startTime=' + start + '&endTime=' + end + '&timeframe=month'
    
    return requests.post(url, headers=headers, data=data)


# 일단위 주가 정보 가져오기
# 06670, 20160101, 20210430
# returns response(has status_code, text)
def fetchDailyStockData(code, start, end):
    url = 'https://api.finance.naver.com/siseJson.naver?symbol=' + code + '&requestType=1&startTime=' \
        + start + '&endTime=' + end + '&timeframe=day'
    
    headers = CaseInsensitiveDict()
    headers['accept'] = '*/*'
    headers['accept-encoding'] = 'gzip, deflate, br'
    headers['accept-language'] = 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'
    headers['origin'] = 'https://finance.naver.com'
    headers['referer'] = 'https://finance.naver.com/item/fchart.nhn?code=' + code
    headers['sec-ch-ua'] = '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"'
    headers['sec-ch-ua-mobile'] = '?0'
    headers['sec-fetch-dest'] = 'empty'
    headers['sec-fetch-mode'] = 'cors'
    headers['sec-fetch-site'] = 'same-site'
    headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'
    headers['Content-Type'] = 'application/x-www-form-urlencoded'

    data = 'symbol=' + code + '&requestType=1&startTime=' + start + '&endTime=' + end + '&timeframe=day'
    
    return requests.post(url, headers=headers, data=data)



# 기업 상태 데이터용 페치용 헤더 생성
def makeHeader(code):
    headers = CaseInsensitiveDict()
    headers['accept'] = '*/*'
    headers['accept-encoding'] = 'gzip, deflate, br'
    headers['accept-language'] = 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'
    headers['referer'] = 'https://navercomp.wisereport.co.kr/v2/company/c1030001.aspx?cmp_cd=' + code + '&cn='
    headers['sec-ch-ua'] = '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"'
    headers['sec-ch-ua-mobile'] = '?0'
    headers['sec-fetch-dest'] = 'empty'
    headers['sec-fetch-mode'] = 'cors'
    headers['sec-fetch-site'] = 'same-site'
    headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'
    
    return headers
    
# 손익계산표 가져오기
# 06670
# returns response(has status_code, text)
def fetchProfitLossData(code):
    url = 'https://navercomp.wisereport.co.kr/v2/company/cF3002.aspx?cmp_cd=' + code + '&frq=0&rpt=0&finGubun=MAIN&frqTyp=0&cn=&encparam=' + enc_param_value
    headers = makeHeader(code)
    return requests.get(url, headers=headers)


# 재무상태표 가져오기
# 06670
# returns response(has status_code, text)
def fetchFinacialData(code):
    url = 'https://navercomp.wisereport.co.kr/v2/company/cF3002.aspx?cmp_cd=' + code + '&frq=0&rpt=1&finGubun=MAIN&frqTyp=0&cn=&encparam=' + enc_param_value
    headers = makeHeader(code)
    return requests.get(url, headers=headers)


# 현금흐름표 가져오기
# 06670
# returns response(has status_code, text)
def fetchCashFlowData(code):
    url = 'https://navercomp.wisereport.co.kr/v2/company/cF3002.aspx?cmp_cd=' + code + '&frq=0&rpt=2&finGubun=MAIN&frqTyp=0&cn=&encparam=' + enc_param_value
    headers = makeHeader(code)
    return requests.get(url, headers=headers)


# 지정한 종목의 모든 데이터를 가져와 파일로 지정한 위치에 저장함.
# 월단위 주가, 손익계산표, 재무제표, 현금흐름표가 각각 다음과 같이 저장됨.
# [code]-stock.txt, [code]-profit.txt, [code]-financial.txt, [code]-cash.txt
# code: 종목코드
# path: 저장위치.
# start, end: 주가 조회 기간. 'YYYYMMDD' 형태
def fetchAndWrite(code, path, start, end):
    r = fetchMonthStockData(code, start, end)
    writeResponse(r, 'stock', code, path)

    tm.sleep(0.35)
    r = fetchProfitLossData(code)
    writeResponse(r, 'profit', code, path)
    
    tm.sleep(0.35)
    r = fetchFinacialData(code)
    writeResponse(r, 'financial', code, path)

    tm.sleep(0.35)
    r = fetchCashFlowData(code)
    writeResponse(r, 'cash', code, path)

    
# 손익계산표 가져오기 (분기)
# 06670
# returns response(has status_code, text)
def fetchQuaterProfitLossData(code):
    url = 'https://navercomp.wisereport.co.kr/v2/company/cF3002.aspx?cmp_cd=' + code + '&frq=1&rpt=0&finGubun=MAIN&frqTyp=1&cn=&encparam=' + enc_param_value
    headers = makeHeader(code)
    return requests.get(url, headers=headers)


# 재무상태표 가져오기 (분기)
# 06670
# returns response(has status_code, text)
def fetchQuaterFinacialData(code):
    url = 'https://navercomp.wisereport.co.kr/v2/company/cF3002.aspx?cmp_cd=' + code + '&frq=1&rpt=1&finGubun=MAIN&frqTyp=1&cn=&encparam=' + enc_param_value
    headers = makeHeader(code)
    return requests.get(url, headers=headers)


# 현금흐름표 가져오기 (분기)
# 06670
# returns response(has status_code, text)
def fetchQuaterCashFlowData(code):
    url = 'https://navercomp.wisereport.co.kr/v2/company/cF3002.aspx?cmp_cd=' + code + '&frq=1&rpt=2&finGubun=MAIN&frqTyp=1&cn=&encparam=' + enc_param_value
    
    headers = makeHeader(code)

    return requests.get(url, headers=headers)


# 전체 회사 기본정보 가져오기
def fetchCompanyInfo():
    url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'

    headers = CaseInsensitiveDict()

    headers["Host"] = "data.krx.co.kr"
    headers["Accept"] = "application/json, text/javascript, */*; q=0.01"
    headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
    headers["Origin"] = "http://data.krx.co.kr"
    headers["Referer"] = "http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020101"
    headers["Accept-Encoding"] = "gzip, deflate"
    headers["Accept-Language"] = "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"
    headers["Content-Type"] = "application/x-www-form-urlencoded"

    data = "bld=dbms/MDC/STAT/standard/MDCSTAT01901&mktId=ALL&share=1&csvxls_isNo=false"

    return requests.post(url, headers=headers, data=data)


# 지정한 종목의 월단위 주가 저장. 파일명: [code]-stock.txt, 
# code: 종목코드
# path: 저장위치.
# start, end: 주가 조회 기간. 'YYYYMMDD' 형태
def fetchMonthPrice(code, path, start, end):
    r = fetchMonthStockData(code, start, end)
    writeResponse(r, 'stock', code, path)

    
# 지정한 종목의 모든 데이터를 가져와 파일로 지정한 위치에 저장함.
# 손익계산표, 재무제표, 현금흐름표가 각각 다음과 같이 저장됨.
# [code]-profit.txt, [code]-financial.txt, [code]-cash.txt
# code: 종목코드
# path: 저장위치.
def fetchAndWriteYear(code, path, start, end, year=True):
    tm.sleep(0.35)
    r = fetchProfitLossData(code) if year else fetchQuaterProfitLossData(code)
    writeResponse(r, 'profit', code, path)
    
    tm.sleep(0.35)
    r = fetchFinacialData(code) if year else fetchQuaterFinacialData(code)
    writeResponse(r, 'financial', code, path)

    tm.sleep(0.35)
    r = fetchCashFlowData(code) if year else fetchQuaterCashFlowData(code)
    writeResponse(r, 'cash', code, path)

    
# In[ ]:


def searchSmallSize(dirname):
    dupChecker = {}
    try:
        filenames = os.listdir(dirname)
        for filename in filenames:
            full_filename = os.path.join(dirname, filename)
            if os.path.isdir(full_filename):
                continue
            else:
                fSize = os.path.getsize(full_filename)
                if fSize < 100:
                    code = filename[:6]
                    if not code in dupChecker:
                        dupChecker[code] = True
    except PermissionError:
        pass
    
    return list(dupChecker.keys())



def retryLessSizer(outPath, start, end):
    lessCodes = searchSmallSize(outPath)

    print('less size', len(lessCodes), 'found')

    noLine = 1
    for code in lessCodes:
        sTick = tm.time()
        print(noLine, code,'processing')
        fetchAndWrite(code, outPath, start, end)
        print(noLine, code,'done', tm.time() - sTick)
        noLine += 1

        
        
def writeStockData(code, outFile, resp):
    lrdr = io.StringIO(resp.text)

    lineNo = 0
    while True:
        line = lrdr.readline()

        if not line:
            break

        lineNo += 1
        line = line.strip()

        if len(line) < 1 or not line.startswith('['):
            continue
        
        # 제목 스킵
        if line.startswith('[['):
            continue

        sPos = line.rfind('[')
        ePos = line.rfind(']')

        outFile.write(code)
        outFile.write(', ')
        outFile.write(line[sPos + 1:ePos].replace('"', ''))
        outFile.write('\n');

    lrdr.close()


# basis: Y, Q
def fetchCompanyInformation(code, basis):
    url = 'https://navercomp.wisereport.co.kr/v2/company/ajax/cF1001.aspx?cmp_cd=' + code + '&fin_typ=0&freq_typ=' + basis + '&id=bG05RlB6cn&encparam=' + enc_param_value

    headers = CaseInsensitiveDict()    
    headers['Host'] = 'navercomp.wisereport.co.kr'
    headers['Connection'] = 'keep-alive'
    headers['sec-ch-ua'] = '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"'
    headers['Accept'] = 'text/html, */*; q=0.01'
    headers['sec-ch-ua-mobile'] = '?0'
    headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    headers['Sec-Fetch-Site'] = 'same-origin'
    headers['Sec-Fetch-Mode'] = 'cors'
    headers['Sec-Fetch-Dest'] = 'empty'
    headers['Referer'] = 'https://navercomp.wisereport.co.kr/v2/company/c1010001.aspx?cmp_cd=' + code + '&cn='
    headers['Accept-Encoding'] = 'gzip, deflate, br'
    headers['Accept-Language'] = 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'

    return requests.get(url, headers=headers)


def getDataTitles(basis):
    resp = fetchCompanyInformation('066570', basis)
    bs = BeautifulSoup(resp.text, 'html.parser')
    tagBody = bs.findAll('tbody') # len(tagBody) == 2
    records = tagBody[1].findAll('tr')
    
    title = []
    for tag in records:
        titleTag = tag.find('th')
        title.append(titleTag.text.strip())

    tagHead = bs.findAll('thead') # len(tagHead) == 2
    tagFile = tagHead[1].findAll('th')

    yearTitle = [t.text.strip()[0:t.text.strip().find('\r')].replace('/', '-') for t in tagFile][2:]

    return (title, yearTitle)


# 실수 판단
def isReal(str):
    try:
        float(str)
        return True
    except ValueError:
        return False


def getDataArray(code, basis):
    resp = fetchCompanyInformation(code, basis)
    bs = BeautifulSoup(resp.text, 'html.parser')
    
    tagHead = bs.findAll('thead') # len(tagHead) == 2
    if len(tagHead) < 2:
        return None

    tagFile = tagHead[1].findAll('th')

    yearTitle = [t.text.strip()[0:t.text.strip().find('\r')].replace('/', '-') for t in tagFile][2:]
    
    tagBody = bs.findAll('tbody') # len(tagBody) == 2
    records = tagBody[1].findAll('tr')
    
    data = []
    for tag in records:
        tagData = tag.select('td')
        data.append(['' if t is None or not isReal(t.text.replace(',', '')) else t.text.replace(',', '') for t in tagData])
    
    return (data, yearTitle)


# dayNo: 20210514
def fetchDailyStockPrice(dayNo):
    url = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"
    
    headers = CaseInsensitiveDict()

    headers["Host"] = "data.krx.co.kr"
    headers["Accept"] = "application/json, text/javascript, */*; q=0.01"
    headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
    headers["Origin"] = "http://data.krx.co.kr"
    headers["Referer"] = "http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020101"
    headers["Accept-Encoding"] = "gzip, deflate"
    headers["Accept-Language"] = "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"
    headers["Content-Type"] = "application/x-www-form-urlencoded"

    data = "bld=dbms/MDC/STAT/standard/MDCSTAT01501&mktId=ALL&trdDd=" + dayNo + "&share=1&money=1&csvxls_isNo=false"
    
    return requests.post(url, headers=headers, data=data)


# dayNo: 20210514
def writeDailyPriceFromKRX(dayNo, outPath):
    colKeys = ["ISU_SRT_CD", "ISU_ABBRV", "MKT_NM", "SECT_TP_NM", "TDD_CLSPRC", "CMPPREVDD_PRC", "FLUC_RT", "TDD_OPNPRC", "TDD_HGPRC", "TDD_LWPRC", "ACC_TRDVOL", "ACC_TRDVAL", "MKTCAP", "LIST_SHRS"]
    colNames = ["종목코드", "종목명", "시장구분", "소속부", "종가", "대비", "등락률", "시가", "고가", "저가", "거래량", "거래대금", "시가총액", "상장주식수"]

    resp = fetchDailyStockPrice(dayNo)
    
    if not resp.status_code == 200:
        print('http error', resp.status_code, flush=True)
        return
    
    obj = json.loads(resp.text)
    if obj is None:
        print('invalid result', flush=True)
        return
    
    data = obj['OutBlock_1']
    if len(data) < 1:
        print('no data', flush=True)
        return
    
    if data[0]["TDD_CLSPRC"] == "-":
        print('no data', flush=True)
        return
    
    out = open(outPath + "krx-price-" + dayNo + ".txt", "w", encoding="utf-8")
    out.write("날짜\t")
    out.write("\t".join(colNames))
    out.write("\n")
    
    for rec in data:
        out.write(dayNo)
        for kk in colKeys:
            out.write("\t")
            out.write(str(rec[kk]).replace(",", ""))
        out.write("\n")
    
    out.close()
    
    print(dayNo, 'done', flush=True)

