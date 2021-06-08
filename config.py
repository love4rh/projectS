#-*- coding:utf-8 -*-

# config.py

# 네이버 API를 호출하기 위한 암호화 파라미터
# 만료 기간이 지나면 네이버에서 확인 후 수정해야 함.
encParamKey = 'MzcxaGJUeEt4blBJQmVmT1hiWnRHUT09'

runServerType = 2 # 1: window, 2: mac, 3: linux

print('running on', ['Window', 'Mac', 'Linux'][runServerType - 1])


# 기본 폴더 위치
dirBase = 'D:\\work\\jupyter\\krx\\' # for Window
resourceDir = dirBase + 'resource\\'

# 재무제표 크롤링 데이터 저장 위치
outputRawPath = dirBase + 'output\\'

# 임시파일 저장용 폴더
temporaryPath = dirBase + 'temporary\\'

# Crawlego 경로
crawlegoPath = '/home/ec2-user/krx/analysis/jar/crawlego-1.0.0.jar'

# Pivot용 Jar 파일 경로
pivotPath = '/home/ec2-user/krx/analysis/jar/pivot.jar'


if runServerType == 3:
    dirBase = '/home/ec2-user/krx/'
    resourceDir = dirBase + 'resource/'
    outputRawPath = dirBase + 'output/'
    temporaryPath = dirBase + 'temporary/'
    crawlegoPath = '/home/ec2-user/krx/analysis/jar/crawlego-1.0.0.jar'
    pivotPath = '/home/ec2-user/krx/analysis/jar/pivot.jar'
elif runServerType == 2:
    dirBase = '/Users/TurboK/workspace/krx/'
    resourceDir = dirBase + 'resource/'
    outputRawPath = dirBase + 'output/'
    temporaryPath = dirBase + 'temporary/'

    
# 조회할 기업 코드 목록 파일
codePathFile = resourceDir + 'companyInfo-20210530.txt'
