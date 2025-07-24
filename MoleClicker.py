import sys
import random
import csv
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer

time = 0            # 타이머 시간 설정.
fps = 60            # 프레임?
holeList = list()   # 구멍 배열
xLen, yLen = 0, 0   # 구멍 배열과 두더지 구멍 xy 길이 설정
combo = 0           # 콤보
path = "Scoreboard.csv" # 저장 경로
csvList = list[]    # 읽고쓰기용 리스트


# 두더지 클래스
# 일반, 누르면 안됨, 특정 키와 함꼐 누름, 여러번 누름, 좌클릭, 보너스 두더지
# 잡혔을 때 반응(각 두더지 고유효과), 나와있는 시간,

# 최대 동시 존재 갯수?


# 저장할 점수에 무슨 정보가 들었는가?
# 닉네임, 총점, 최대 콤보, 클릭 수, 잡은 두더지 수, 명중률, 플레이 시간
# csv

saveData = ["", 0, 0, 0, 0, 0.0, 0]

def saveData(name, score, maxCombo, clickCnt, moleCnt, playTime):
    csvList.clear()
    with open(f"./{path}", "r", encoding="utf-8-sig") as read:
        reader=csv.reader(read) # 읽기
        head=next(reader)   # 헤더 빼오기
        csvList.append(head)# 빼온 헤더 리스트에 추가
        for row in reader:  # 남은 열들 반복하며 리스트에 추가
            csvList.append(row)
        csvList.append([name, score, maxCombo, clivkCnt, moleCnt,
                        (moleCnt/clickCnt), playTime])
        with open(f"./{path}", "w", newline='', encoding="utf-8-sig") as write:
            data = list(reader) # 헤더가 빠진 정보들 리스트로 만듬
            data.sort(key=lambda x: x[2])   # 총점 행 기준으로 정렬
            writer = csv.writer(write)  # 쓰기 준비
            writer.writerow(head)  # 헤더 써넣기
            for row in data:    # 반복하며 필요없는 행을 제외한 데이터 써넣기
                writer.writerow(row)

def loadData():
    csvList.clear()
    with open(f"./{path}", "r", encoding="utf-8-sig") as read:
        reader=csv.reader(read) # 읽기
        head=next(reader)   # 헤더 빼오기
        csvList.append(head)# 빼온 헤더 리스트에 추가
        for row in reader:  # 남은 열들 반복하며 리스트에 추가
            csvList.append(row)
    return csvList # 반환하고, 스코어보드로 출력시키

def scoreBoard():
    # 1. 로드
    # 2. 화면 출력
    # 3. 꺼지기 전에 세이브  
        


# 메인은 이 아래에
