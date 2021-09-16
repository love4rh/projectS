#-*- coding:utf-8 -*-

# config.py

# True이며, 기업 코드 및 업종별 크롤링 데이터 정리까지 모든 작업을 수행함.
doingAllJob = False

# 네이버 API를 호출하기 위한 암호화 파라미터
# 만료 기간이 지나면 네이버에서 확인 후 수정해야 함.
encParamKey = 'dllGejUrZmdPRkVOSjFiSjVIOXZDUT09'

runServerType = 2 # 1: window, 2: mac, 3: linux

print('running on', ['Windows', 'OS X', 'Linux'][runServerType - 1])


# 기본 폴더 위치
dirBase = 'D:\\work\\jupyter\\krx\\' # for Window
resourceDir = dirBase + 'resource\\'

# 재무제표 크롤링 데이터 저장 위치
outputRawPath = dirBase + 'output\\'

# 임시파일 저장용 폴더
temporaryPath = dirBase + 'intermediate\\'

# Crawlego Jar 경로
crawlegoPath = dirBase + 'jar\\crawlego-1.0.0.jar'

# Pivot용 Jar 파일 경로
pivotPath = dirBase + 'jar\\pivot.jar'

# Crawlego 스크립트 경로
crawlegoScriptPath = dirBase + 'script\\'


if runServerType == 3:
    dirBase = '/home/ec2-user/krx/'
    resourceDir = dirBase + 'resource/'
    outputRawPath = dirBase + 'output/'
    temporaryPath = dirBase + 'intermediate/'
    crawlegoPath = dirBase + 'jar/crawlego-1.0.0.jar'
    pivotPath = dirBase + 'jar/pivot.jar'
    crawlegoScriptPath = dirBase + 'script/'
elif runServerType == 2:
    dirBase = '/Users/TurboK/workspace/krx/'
    resourceDir = dirBase + 'resource/'
    outputRawPath = dirBase + 'output/'
    temporaryPath = dirBase + 'intermediate/'
    crawlegoPath = dirBase + 'jar/crawlego-1.0.0.jar'
    pivotPath = dirBase + 'jar/pivot.jar'
    crawlegoScriptPath = dirBase + 'script/'


# 조회할 기업 코드 목록 파일
# 출처: https://kind.krx.co.kr/corpgeneral/corpList.do?method=loadInitPage --> 메뉴 중 상장법인 목록
codePathFile = resourceDir + 'companyCodes.txt'
