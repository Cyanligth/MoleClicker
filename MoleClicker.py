import sys
import random
import csv
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import *


time = 0            # 타이머 시간 설정.
fps = 60            # 프레임?
holeList = list()   # 구멍 배열
xLen, yLen = 0, 0   # 구멍 배열과 두더지 구멍 xy 길이 설정
combo = 0           # 콤보
path = "Scoreboard.csv" # 저장 경로
total_score = 0

# 두더지 클래스
class Mole:
    def __init__ (self):
        self.score = 1
        self.image_path = ""
    def Mole_click(self):
        pass
    
class Classic_Mole(Mole):       # 일반 두더지
    def __init__(self):
        super().__init__()
        self.score = 1
        self.image_path = "C:/Users/USER/Documents/GitHub/MoleClicker/classic_mole.jpg"

    def Mole_click(self):
        global total_score
        total_score += self.score 

class Boom_Mole(Mole):          # 폭탄 두더지
    def __init__(self):
        super().__init__()
        self.score = -1
        self.image_path = "C:/Users/USER/Documents/GitHub/MoleClicker/boom_mole.jpg"

    def Mole_click(self):
        global total_score
        total_score += self.score 

class Keyboard_Mole(Mole):      # 특정키 두더지
    def __init__(self):
        super().__init__()
        self.score = 1
        self.image_paths = [
            "C:/Users/USER/Documents/GitHub/MoleClicker/up_mole.jpg",    
            "C:/Users/USER/Documents/GitHub/MoleClicker/down_mole.jpg",  
            "C:/Users/USER/Documents/GitHub/MoleClicker/right_mole.jpg", 
            "C:/Users/USER/Documents/GitHub/MoleClicker/left_mole.jpg"  
       ]
    def Mole_click(self):
        global total_score
        total_score += self.score

class Doubleclick_Mole(Mole):   # 더블클릭 두더지
    def __init__(self):
        super().__init__()
        self.score = 1
        self.image_path = "C:/Users/USER/Documents/GitHub/MoleClicker/Doubleclick_mole.jpg"

    def Mole_click(self):
        global total_score
        total_score += self.score

class Rightclick_Mole(Mole):    # 우클릭 두더지
    def __init__(self):
        super().__init__()
        self.score = 1
        self.image_path = "C:/Users/USER/Documents/GitHub/MoleClicker/Rightclick_mole.jpg"

    def Mole_click(self):
        global total_score
        total_score += self.score

class Bonus_Mole(Mole):         # 보너스 두더지
    def __init__(self):
        super().__init__()
        self.score = 3
        self.image_path = "C:/Users/USER/Documents/GitHub/MoleClicker/bonus_mole.jpg"

    def Mole_click(self):
        global total_score
        total_score += self.score

# 일반, 누르면 안됨, 특정 키와 함꼐 누름, 여러번 누름, 좌클릭, 보너스 두더지
# 잡혔을 때 반응(각 두더지 고유효과), 나와있는 시간,

# 최대 동시 존재 갯수?


# 저장할 점수에 무슨 정보가 들었는가?
# 닉네임, 총점, 최대 콤보, 클릭 수, 잡은 두더지 수, 명중률, 플레이 시간
# csv

saveData = ["", 0, 0, 0, 0, 0.0, 0]

def saveData(name, score, maxCombo, clickCnt, moleCnt, playTime):
    csvList = []
    with open(f"./{path}", "r", encoding="utf-8-sig") as read:
        reader=csv.reader(read) # 읽기
        head=next(reader)   # 헤더 빼오기
        csvList.append(head)# 빼온 헤더 리스트에 추가
        for row in reader:  # 남은 열들 반복하며 리스트에 추가
            csvList.append(row)
        csvList.append([name, score, maxCombo, clickCnt, moleCnt,
                        (moleCnt/clickCnt), playTime])
        with open(f"./{path}", "w", newline='', encoding="utf-8-sig") as write:
            data = list(reader) # 헤더가 빠진 정보들 리스트로 만듬
            data.sort(key=lambda x: x[2])   # 총점 행 기준으로 정렬
            writer = csv.writer(write)  # 쓰기 준비
            writer.writerow(head)  # 헤더 써넣기
            for row in data:    # 반복하며 필요없는 행을 제외한 데이터 써넣기
                writer.writerow(row)

def loadData():
    csvList = []
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
    pass
        


class MoleClicker_Start_GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("두더지잡기 게임") # 타이틀 설정
        self.setGeometry(100, 100, 600, 400) # 화면 크기 조정(창 위치 x, y), 너비 높이   
        self.initUI()


    def initUI(self):
        self.setStyleSheet("background-color: #E0FFFF;") # 배경화면 색깔 설정

        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignCenter)

        self.title_label = QLabel("두더지잡기 게임")
        self.title_label.setFont(QFont("굴림", 36, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: navy; background: transparent;")
        self.main_layout.addWidget(self.title_label)

        self.main_screen_button_container = QWidget()
        main_screen_button_layout = QVBoxLayout(self.main_screen_button_container)
        main_screen_button_layout.setAlignment(Qt.AlignCenter)

        self.start_button = QPushButton("게임 시작")
        self.start_button.setFont(QFont("굴림", 18, QFont.Bold))
        self.start_button.setFixedSize(200, 60)
        self.start_button.setStyleSheet(
            "QPushButton { background-color: #54f254; color: black; border-radius: 10px; transition: background-color 0.3s ease; }" # 바탕색깔, 텍스트 색깔, 꼭짓점 뾰족함정도, 서서히 자연스럽게 색깔 바꾸기 
            "QPushButton:hover { background-color: #3dbe3d; }" # 상호작용 시 바뀌는 색깔 
        )
        # 게임 시작 버튼 클릭 시 게임 화면으로 전환하는 함수연
        self.start_button.clicked.connect(self.startGame)
        main_screen_button_layout.addWidget(self.start_button, alignment=Qt.AlignCenter)

        self.set_difficulty_button = QPushButton("난이도 설정")
        self.set_difficulty_button.setFont(QFont("굴림", 18, QFont.Bold))
        self.set_difficulty_button.setFixedSize(200, 60)
        self.set_difficulty_button.setStyleSheet(
            "QPushButton { background-color: #54f254; color: black; border-radius: 10px; transition: background-color 0.3s ease; }"
            "QPushButton:hover { background-color: #3dbe3d; }"
        )
        self.set_difficulty_button.clicked.connect(self.showDifficultyOptions)
        main_screen_button_layout.addWidget(self.set_difficulty_button, alignment=Qt.AlignCenter)

        self.main_layout.addWidget(self.main_screen_button_container)

        self.difficulty_buttons_container = QWidget()
        difficulty_buttons_layout = QVBoxLayout(self.difficulty_buttons_container)
        difficulty_buttons_layout.setAlignment(Qt.AlignCenter)
        self.difficulty_buttons_container.hide()

        self.easy_button = QPushButton("쉬움")
        self.easy_button.setFont(QFont("굴림", 18, QFont.Bold))
        self.easy_button.setFixedSize(200, 60)
        self.easy_button.setStyleSheet(
            "QPushButton { background-color: #ADD8E6; color: black; border-radius: 10px; transition: background-color 0.3s ease; }"
            "QPushButton:hover { background-color: #87CEEB; }"
        )
        self.easy_button.clicked.connect(lambda: self.setDifficulty("쉬움"))
        difficulty_buttons_layout.addWidget(self.easy_button, alignment=Qt.AlignCenter)

        self.normal_button = QPushButton("보통")
        self.normal_button.setFont(QFont("굴림", 18, QFont.Bold))
        self.normal_button.setFixedSize(200, 60)
        self.normal_button.setStyleSheet(
            "QPushButton { background-color: #FFD700; color: black; border-radius: 10px; transition: background-color 0.3s ease; }"
            "QPushButton:hover { background-color: #DAA520; }"
        )
        self.normal_button.clicked.connect(lambda: self.setDifficulty("보통"))
        difficulty_buttons_layout.addWidget(self.normal_button, alignment=Qt.AlignCenter)

        self.hard_button = QPushButton("어려움")
        self.hard_button.setFont(QFont("굴림", 18, QFont.Bold))
        self.hard_button.setFixedSize(200, 60)
        self.hard_button.setStyleSheet(
            "QPushButton { background-color: #FF6347; color: black; border-radius: 10px; transition: background-color 0.3s ease; }"
            "QPushButton:hover { background-color: #FF4500; }"
        )
        self.hard_button.clicked.connect(lambda: self.setDifficulty("어려움"))
        difficulty_buttons_layout.addWidget(self.hard_button, alignment=Qt.AlignCenter)

        self.main_layout.addWidget(self.difficulty_buttons_container)

        self.setLayout(self.main_layout)

    def showDifficultyOptions(self):
        self.main_screen_button_container.hide()
        self.difficulty_buttons_container.show()
        self.title_label.setText("난이도 선택")

    def setDifficulty(self, difficulty):
        self.difficulty_buttons_container.hide()
        self.main_screen_button_container.show()
        self.title_label.setText("두더지잡기 게임")

    def startGame(self):
        self.hide()
        self.game_screen = MoleClicker_Ingame_GUI() # 인게임 화면 
        self.game_screen.show()

class MoleClicker_Ingame_GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("두더지잡기 게임 - 플레이 중")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        background_image_path = r'C:/Users/USER/Documents/GitHub/MoleClicker/Ingame_bg.png'
        hole_image_path = r'C:/Users/USER/Documents/GitHub/MoleClicker/empty_hole.png'
        hole_image_size = QSize(100, 100)

        self.background_label = QLabel(self)
        self.background_label.setPixmap(QPixmap(background_image_path).scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        self.background_label.lower()  # 배경이 맨 아래로

        self.foreground_widget = QWidget(self)
        self.foreground_layout = QGridLayout(self.foreground_widget)
        self.foreground_layout.setAlignment(Qt.AlignCenter)

        rows, cols = 5, 5
        hole_positions = [
            (1, 0), (1, 2), (1, 4),
            (2, 1), (2, 3),
            (3, 0), (3, 2), (3, 4),
            (4, 1), (4, 3)
        ]

        for r in range(rows):
            for c in range(cols):
                if (r, c) in hole_positions:
                    label = QLabel()
                    pixmap = QPixmap(hole_image_path).scaled(hole_image_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    label.setPixmap(pixmap)
                    label.setAlignment(Qt.AlignCenter)
                    self.foreground_layout.addWidget(label, r, c)
                else:
                    spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
                    self.foreground_layout.addItem(spacer, r, c)

        full_layout = QVBoxLayout(self)
        full_layout.addWidget(self.foreground_widget)
        self.setLayout(full_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MoleClicker_Start_GUI()
    main_window.show()
    sys.exit(app.exec_())

