import sys
import random
import csv
import os

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QGridLayout, QSpacerItem, QSizePolicy, QMessageBox, QInputDialog, QTableWidget, QTableWidgetItem, QHeaderView, QDialog
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, QTimer, QEvent, QPoint


GAMETIME = 5
path = "Scoreboard.csv"
total_score = 0
click_count = 0
mole_hit_count = 0
diff = 0  # 0 이지 1 노말 2 하드


class Mole:
    def __init__(self):
        self.score = 1
        self.image_path = ""
        self.image_paths = []
        self.is_active = False
        self.timer = QTimer()
        self.hide_duration = 1000

    def Mole_click(self, game_gui=None):
        pass

    def set_active(self, active, button=None):
        self.is_active = active
        if button:
            button.current_mole = self
            if active:
                img_to_load = self.image_path
                if not img_to_load and self.image_paths:
                    img_to_load = random.choice(self.image_paths)

                pixmap = QPixmap(img_to_load)
                if pixmap.isNull():
                    print(f"이미지 로드 실패: {img_to_load}")
                    button.setText("ERR")
                    button.setIcon(QIcon())
                else:
                    scaled_pixmap = pixmap.scaled(button.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    button.setIcon(QIcon(scaled_pixmap))
                    button.setIconSize(button.size())
            else:
                empty_hole_path = "C:/Users/USER/Documents/GitHub/MoleClicker/empty_hole.png"
                empty_pixmap = QPixmap(empty_hole_path)
                if empty_pixmap.isNull():
                    print(f"빈 구멍 이미지 로드 실패: {empty_hole_path}")
                    button.setText("O")
                    button.setIcon(QIcon())
                else:
                    scaled_empty_pixmap = empty_pixmap.scaled(button.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    button.setIcon(QIcon(scaled_empty_pixmap))
                    button.setIconSize(button.size())
            button.setEnabled(active)
        else:
            print("경고: 연결된 버튼이 없습니다.")


class MoleButton(QPushButton):
    def __init__(self, r, c, parent=None):
        super().__init__(parent)
        self.row = r
        self.col = c
        self.current_mole = None
        self.setFixedSize(100, 100)
        self.setStyleSheet("QPushButton { background: transparent; border: none; }")
        self.empty_hole_pixmap = QPixmap("C:/Users/USER/Documents/GitHub/MoleClicker/empty_hole.png").scaled(
            self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.setIcon(QIcon(self.empty_hole_pixmap))
        self.setIconSize(self.size())
        self.clicked.connect(self.on_left_click)

        self.setFocusPolicy(Qt.StrongFocus)
        self.last_key_pressed = None
        self.click_timer = QTimer(self)
        self.click_timer.setSingleShot(True)
        self.click_timer.setInterval(250)
        self.click_count_for_double = 0

    def mousePressEvent(self, event):
        if self.current_mole and self.current_mole.is_active:
            if isinstance(self.current_mole, Rightclick_Mole) and event.button() == Qt.RightButton:
                self.on_right_click()
            elif isinstance(self.current_mole, Doubleclick_Mole) and event.button() == Qt.LeftButton:
                self.on_double_click_attempt()
            elif event.button() == Qt.LeftButton:
                if not isinstance(self.current_mole, Keyboard_Mole) and not isinstance(self.current_mole, Doubleclick_Mole):
                    self.on_left_click()
        super().mousePressEvent(event)

    def keyPressEvent(self, event):
        self.last_key_pressed = event.key()
        super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        self.last_key_pressed = None
        super().keyReleaseEvent(event)

    def on_left_click(self):
        global click_count
        click_count += 1
        if self.current_mole and self.current_mole.is_active:
            if isinstance(self.current_mole, Classic_Mole) or isinstance(self.current_mole, Boom_Mole) or isinstance(self.current_mole, Bonus_Mole):
                self.process_mole_hit(self.current_mole)
            elif isinstance(self.current_mole, Keyboard_Mole):
                if self.last_key_pressed == self.current_mole.required_key:
                    self.process_mole_hit(self.current_mole)
                else:
                    print(f"DEBUG: Keyboard_Mole (키: {self.current_mole.required_key}) 클릭 - 잘못된 키 입력")

    def on_right_click(self):
        global click_count
        click_count += 1
        if self.current_mole and self.current_mole.is_active and isinstance(self.current_mole, Rightclick_Mole):
            self.process_mole_hit(self.current_mole)
        else:
            print("DEBUG: 우클릭 두더지가 아니거나 활성화되지 않았습니다.")


    def on_double_click_attempt(self):
        self.click_count_for_double += 1
        global click_count
        click_count += 1

        if self.click_timer.isActive():
            if self.click_count_for_double == 2:
                self.click_timer.stop()
                self.click_count_for_double = 0
                if self.current_mole and self.current_mole.is_active and isinstance(self.current_mole, Doubleclick_Mole):
                    self.process_mole_hit(self.current_mole)
                else:
                    print("DEBUG: 더블클릭 두더지가 아니거나 활성화되지 않았습니다.")
            else:
                self.click_timer.stop()
                self.click_count_for_double = 0
                print("DEBUG: 더블클릭 실패 (클릭 횟수 오류)")
        else:
            self.click_timer.start()
            self.click_count_for_double = 1
            self.click_timer.timeout.connect(self.reset_double_click_count)

    def reset_double_click_count(self):
        if self.click_count_for_double == 1:
            print("DEBUG: 더블클릭 실패 (시간 초과)")
        self.click_count_for_double = 0


    def process_mole_hit(self, mole_obj):
        global mole_hit_count
        mole_obj.Mole_click(game_gui=self.parent().parent())
        mole_hit_count += 1
        self.parent().parent().update_score_display()
        self.parent().parent().show_score_effect(mole_obj.score, self.mapToGlobal(self.rect().center()))
        self.parent().parent().hide_mole(self)


class Classic_Mole(Mole):
    def __init__(self):
        super().__init__()
        self.score = 1
        self.image_path = "C:/Users/USER/Documents/GitHub/MoleClicker/classic_mole.png"

        global diff
        if diff == 0:
            self.hide_duration = 1500
        elif diff == 1:
            self.hide_duration = 1000
        else:
            self.hide_duration = 500

    def Mole_click(self, game_gui=None):
        global total_score
        total_score += self.score
        print(f"DEBUG: 일반 두더지 클릭! 현재 점수: {total_score}")

class Boom_Mole(Mole):
    def __init__(self):
        super().__init__()
        self.score = -5
        self.image_path = "C:/Users/USER/Documents/GitHub/MoleClicker/boom_mole.png"

        global diff
        if diff == 0:
            self.hide_duration = 1200
        elif diff == 1:
            self.hide_duration = 800
        else:
            self.hide_duration = 300

    def Mole_click(self, game_gui=None):
        global total_score
        total_score += self.score
        print(f"DEBUG: 폭탄 두더지 클릭! 현재 점수: {total_score}")

class Keyboard_Mole(Mole):
    def __init__(self):
        super().__init__()
        self.score = 1
        self.image_paths = [
            ("C:/Users/USER/Documents/GitHub/MoleClicker/up_mole.png", Qt.Key_Up),
            ("C:/Users/USER/Documents/GitHub/MoleClicker/down_mole.png", Qt.Key_Down),
            ("C:/Users/USER/Documents/GitHub/MoleClicker/right_mole.png", Qt.Key_Right),
            ("C:/Users/USER/Documents/GitHub/MoleClicker/left_mole.png", Qt.Key_Left)
        ]
        chosen_info = random.choice(self.image_paths)
        self.image_path = chosen_info[0]
        self.required_key = chosen_info[1]

        global diff
        if diff == 0:
            self.hide_duration = 2500
        elif diff == 1:
            self.hide_duration = 1800
        else:
            self.hide_duration = 1200

    def Mole_click(self, game_gui=None):
        global total_score
        total_score += self.score
        print(f"DEBUG: 특정키 두더지 클릭! 현재 점수: {total_score}")

class Doubleclick_Mole(Mole):
    def __init__(self):
        super().__init__()
        self.score = 1
        self.image_path = "C:/Users/USER/Documents/GitHub/MoleClicker/Doubleclick_mole.png"

        global diff
        if diff == 0:
            self.hide_duration = 1500
        elif diff == 1:
            self.hide_duration = 1000
        else:
            self.hide_duration = 700

    def Mole_click(self, game_gui=None):
        global total_score
        total_score += self.score
        print(f"DEBUG: 더블클릭 두더지 클릭! 현재 점수: {total_score}")

class Rightclick_Mole(Mole):
    def __init__(self):
        super().__init__()
        self.score = 1
        self.image_path = "C:/Users/USER/Documents/GitHub/MoleClicker/Rightclick_mole.png"

        global diff
        if diff == 0:
            self.hide_duration = 1500
        elif diff == 1:
            self.hide_duration = 1000
        else:
            self.hide_duration = 300

    def Mole_click(self, game_gui=None):
        global total_score
        total_score += self.score
        print(f"DEBUG: 우클릭 두더지 클릭! 현재 점수: {total_score}")

class Bonus_Mole(Mole):
    def __init__(self):
        super().__init__()
        self.score = 3
        self.image_path = "C:/Users/USER/Documents/GitHub/MoleClicker/bonus_mole.png"

        global diff
        if diff == 0:
            self.hide_duration = 1000
        elif diff == 1:
            self.hide_duration = 700
        else:
            self.hide_duration = 500

    def Mole_click(self, game_gui=None):
        global total_score
        total_score += self.score
        print(f"DEBUG: 보너스 두더지 클릭! 현재 점수: {total_score}")
        if game_gui:
            game_gui.add_time(5)


def save_game_data(name, score, clickCnt, moleCnt, playTime):
    csvList = []
    if not os.path.exists(path):
        with open(path, "w", newline='', encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["닉네임", "총점", "클릭 수", "잡은 두더지 수", "명중률", "플레이 시간"])

    with open(path, "r", encoding="utf-8-sig") as read:
        reader = csv.reader(read)
        head = next(reader)
        csvList.append(head)
        for row in reader:
            csvList.append(row)

    accuracy = (moleCnt / clickCnt * 100) if clickCnt > 0 else 0.0
    csvList.append([name, score, clickCnt, moleCnt, f"{accuracy:.2f}%", playTime])

    sorted_data = sorted(csvList[1:], key=lambda x: int(x[1]), reverse=True)

    with open(path, "w", newline='', encoding="utf-8-sig") as write:
        writer = csv.writer(write)
        writer.writerow(head)
        for row in sorted_data:
            writer.writerow(row)
    print("게임 데이터가 저장되었습니다.")


def loadData():
    csvList = []
    if not os.path.exists(path):
        print("Scoreboard.csv 파일이 존재하지 않습니다.")
        return []

    try:
        with open(f"./{path}", "r", encoding="utf-8-sig") as read:
            reader = csv.reader(read)
            # 첫 번째 줄은 헤더이므로 건너뛰지 않고 포함하여 반환 (랭킹 테이블에서 헤더로 사용하기 위함)
            for row in reader:
                csvList.append(row)
        print("Scoreboard.csv 로드 성공.")
        return csvList
    except Exception as e:
        print(f"CSV 파일 로드 중 오류 발생: {e}")
        return []



# 새로 추가할 랭킹 GUI 클래스
class ScoreBoard_GUI(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("랭킹")
        self.setGeometry(200, 200, 700, 500)
        self.initUI()
        self.loadAndDisplayScores()

    def initUI(self):
        self.main_layout = QVBoxLayout(self)

        self.title_label = QLabel("명예의 전당")
        self.title_label.setFont(QFont("굴림", 24, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.title_label)

        self.table_widget = QTableWidget()
        self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers) # 테이블 편집 불가능
        self.table_widget.setSelectionBehavior(QTableWidget.SelectRows) # 행 단위 선택
        self.main_layout.addWidget(self.table_widget)

        self.close_button = QPushButton("닫기")
        self.close_button.setFont(QFont("굴림", 14))
        self.close_button.clicked.connect(self.accept) # QDialog는 accept()를 호출하여 닫을 수 있습니다.
        self.main_layout.addWidget(self.close_button)

    def loadAndDisplayScores(self):
        data = loadData()
        if not data:
            self.table_widget.setRowCount(0)
            self.table_widget.setColumnCount(0)
            return

        header = data[0]
        rows = data[1:]

        self.table_widget.setColumnCount(len(header))
        self.table_widget.setHorizontalHeaderLabels(header)

        # 헤더 정렬 및 크기 조정
        header_view = self.table_widget.horizontalHeader()
        header_view.setSectionResizeMode(QHeaderView.Stretch) # 모든 컬럼 너비를 테이블 위젯에 맞게 자동 조절

        self.table_widget.setRowCount(len(rows))

        for row_idx, row_data in enumerate(rows):
            for col_idx, item_data in enumerate(row_data):
                self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(item_data)))


class MoleClicker_Start_GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DEBUG더지")
        self.setGeometry(100, 100, 600, 400)
        self.initUI()
        self.game_screen = None

    def initUI(self):
        self.setStyleSheet("background-color: #E0FFFF;")

        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignCenter)

        self.title_label = QLabel("DEBUG더지")
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
            "QPushButton { background-color: #54f254; color: black; border-radius: 10px; transition: background-color 0.3s ease; }"
            "QPushButton:hover { background-color: #3dbe3d; }"
        )
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

        # 랭킹 버튼 추가
        self.score_board_button = QPushButton("랭킹 보기")
        self.score_board_button.setFont(QFont("굴림", 18, QFont.Bold))
        self.score_board_button.setFixedSize(200, 60)
        self.score_board_button.setStyleSheet(
            "QPushButton { background-color: #54f254; color: black; border-radius: 10px; transition: background-color 0.3s ease; }"
            "QPushButton:hover { background-color: #3dbe3d; }"
        )
        self.score_board_button.clicked.connect(self.showScoreBoard)
        main_screen_button_layout.addWidget(self.score_board_button, alignment=Qt.AlignCenter)

        # 게임 종료 버튼 추가
        self.exit_button = QPushButton("게임 종료")
        self.exit_button.setFont(QFont("굴림", 18, QFont.Bold))
        self.exit_button.setFixedSize(200, 60)
        self.exit_button.setStyleSheet(
            "QPushButton { background-color: #FF6347; color: black; border-radius: 10px; transition: background-color 0.3s ease; }"
            "QPushButton:hover { background-color: #FF4500; }"
        )
        self.exit_button.clicked.connect(self.close)  # 윈도우를 닫는 슬롯 연결
        main_screen_button_layout.addWidget(self.exit_button, alignment=Qt.AlignCenter)


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

    def setDifficulty(self, difficulty_name):
        global diff
        if difficulty_name == "쉬움":
            diff = 0
        elif difficulty_name == "보통":
            diff = 1
        elif difficulty_name == "어려움":
            diff = 2
        print(f"난이도 설정: {difficulty_name} (diff: {diff})")
        self.difficulty_buttons_container.hide()
        self.main_screen_button_container.show()
        self.title_label.setText("DEBUG더지")

    def startGame(self):
        self.hide()
        self.game_screen = MoleClicker_Ingame_GUI()
        self.game_screen.show()

    def showScoreBoard(self):
        scoreboard_dialog = ScoreBoard_GUI(self)
        scoreboard_dialog.exec_() # 모달 대화 상자로 띄웁니다.


class MoleClicker_Ingame_GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DEBUG더지 - 플레이 중")
        self.setGeometry(100, 100, 800, 600)
        self.active_moles = {}
        self.mole_buttons = {}
        self.game_timer = QTimer(self)
        self.mole_spawn_timer = QTimer(self)
        self.game_duration = GAMETIME
        self.current_game_time = 0
        self.ttt = 0

        global diff
        if diff == 0:
            self.mole_spawn_interval = 1500
        elif diff == 1:
            self.mole_spawn_interval = 1000
        else:
            self.mole_spawn_interval = 700

        self.initUI()
        self.start_game_round()

        self.installEventFilter(self)

    def initUI(self):
        background_image_path = r'C:/Users/USER/Documents/GitHub/MoleClicker/Ingame_bg.png'

        self.background_label = QLabel(self)
        self.update_background_pixmap(self.size())
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        self.background_label.lower()

        self.full_layout = QVBoxLayout(self)

        self.info_bar = QHBoxLayout()
        self.score_label = QLabel(f"점수: {total_score}")
        self.score_label.setFont(QFont("굴림", 16, QFont.Bold))
        self.score_label.setStyleSheet("color: white; background: transparent;")
        self.info_bar.addWidget(self.score_label)
        self.info_bar.addStretch(1)

        self.time_label = QLabel(f"시간: {self.game_duration}초")
        self.time_label.setFont(QFont("굴림", 16, QFont.Bold))
        self.time_label.setStyleSheet("color: white; background: transparent;")
        self.info_bar.addWidget(self.time_label)
        self.full_layout.addLayout(self.info_bar)


        self.foreground_widget = QWidget(self)
        self.foreground_layout = QGridLayout(self.foreground_widget)
        self.foreground_layout.setAlignment(Qt.AlignCenter)
        self.foreground_widget.setStyleSheet("background: transparent;")

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
                    button = MoleButton(r, c, self.foreground_widget)
                    self.foreground_layout.addWidget(button, r, c)
                    self.mole_buttons[(r, c)] = button
                else:
                    spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
                    self.foreground_layout.addItem(spacer, r, c)

        self.full_layout.addWidget(self.foreground_widget)
        self.setLayout(self.full_layout)

    def eventFilter(self, obj, event):
        if obj == self and event.type() == QEvent.Resize:
            self.update_background_pixmap(self.size())
        return super().eventFilter(obj, event)

    def update_background_pixmap(self, size):
        background_image_path = r'C:/Users/USER/Documents/GitHub/MoleClicker/Ingame_bg.png'
        pixmap = QPixmap(background_image_path).scaled(size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        self.background_label.setPixmap(pixmap)
        self.background_label.setGeometry(0, 0, size.width(), size.height())


    def start_game_round(self):
        global total_score, click_count, mole_hit_count, GAMETIME
        total_score = 0
        click_count = 0
        mole_hit_count = 0
        self.current_game_time = GAMETIME # This seems incorrect. It should be initialized to GAMETIME (60).
        self.update_score_display()
        self.time_label.setText(f"시간: {self.current_game_time}초")

        for pos, button in self.mole_buttons.items():
            button.current_mole = None
            button.setIcon(QIcon(button.empty_hole_pixmap))
            button.setIconSize(button.size())
            button.setEnabled(False)

        self.game_timer.timeout.connect(self.update_game_time)
        self.game_timer.start(1000)

        self.mole_spawn_timer.timeout.connect(self.spawn_mole)

        global diff
        if diff == 0:
            self.mole_spawn_interval = 1500
        elif diff == 1:
            self.mole_spawn_interval = 1000
        else:
            self.mole_spawn_interval = 700
        self.mole_spawn_timer.start(self.mole_spawn_interval)

        for button in self.mole_buttons.values():
            button.setEnabled(True)

    def update_score_display(self):
        self.score_label.setText(f"점수: {total_score}")

    def show_score_effect(self, score, position):
        if(score > 0):
            effect_label = QLabel(f"+{score}", self)
        else:
            effect_label = QLabel(f"{score} ", self)
        effect_label.setFont(QFont("Arial", 20, QFont.Bold))
        effect_label.setStyleSheet("color: yellow; background: transparent;" if score > 0 else "color: red; background: transparent;")
        effect_label.adjustSize()

        effect_label.move(position - QPoint(effect_label.width() * 4, effect_label.height() * 4))
        effect_label.show()

        QTimer.singleShot(500, effect_label.deleteLater)

    def update_game_time(self):
        self.current_game_time -= 1
        self.ttt += 1
        self.time_label.setText(f"시간: {self.current_game_time}초")
        if self.current_game_time <= 0:
            self.end_game_round()

    def add_time(self, seconds):
        self.current_game_time += seconds
        self.time_label.setText(f"시간: {self.current_game_time}초")
        print(f"DEBUG: 게임 시간 {seconds}초 추가! 현재 시간: {self.current_game_time}초")

    def end_game_round(self):
        self.game_timer.stop()
        self.mole_spawn_timer.stop()
        for mole_obj in self.active_moles.values():
            mole_obj.timer.stop()
        self.active_moles.clear()

        for button in self.mole_buttons.values():
            button.setEnabled(False)
            button.current_mole = None
            button.setIcon(QIcon(button.empty_hole_pixmap))

        final_play_time = self.ttt # Changed to global GAMETIME

        QMessageBox.information(self, "게임 종료!",
                                f"게임 종료!\n최종 점수: {total_score}\n총 클릭 횟수: {click_count}\n잡은 두더지 수: {mole_hit_count}\n플레이 시간: {final_play_time}초")

        player_name, ok = QInputDialog.getText(self, '게임 결과', '닉네임을 입력하세요:')
        if ok and player_name:
            save_game_data(player_name, total_score, click_count, mole_hit_count, final_play_time)

        self.hide()
        self.game_screen = MoleClicker_Start_GUI()
        self.game_screen.show()
    


    def spawn_mole(self):
        global diff
        max_active_moles = 0
        if diff == 0:
            max_active_moles = 3
        elif diff == 1:
            max_active_moles = 5
        else:
            max_active_moles = 7

        if len(self.active_moles) >= max_active_moles:
            return

        available_holes = [pos for pos, button in self.mole_buttons.items() if not button.current_mole]
        if not available_holes:
            return

        mole_types = [Classic_Mole, Boom_Mole, Keyboard_Mole, Doubleclick_Mole, Rightclick_Mole, Bonus_Mole]

        weights = []
        if diff == 0:
            weights = [60, 5, 10, 10, 10, 5]
        elif diff == 1:
            weights = [50, 10, 15, 10, 10, 5]
        else:
            weights = [40, 15, 15, 10, 10, 10]

        chosen_mole_type = random.choices(mole_types, weights=weights, k=1)[0]
        new_mole = chosen_mole_type()

        spawn_pos = random.choice(available_holes)
        button = self.mole_buttons[spawn_pos]

        new_mole.set_active(True, button)
        self.active_moles[spawn_pos] = new_mole

        new_mole.timer.singleShot(new_mole.hide_duration, lambda: self.hide_mole(button))

    def hide_mole(self, button):
        if button.current_mole:
            if button.current_mole.is_active:
                print(f"DEBUG: 두더지 ({type(button.current_mole).__name__})가 숨었습니다.")

            button.current_mole.set_active(False, button)
            if (button.row, button.col) in self.active_moles:
                del self.active_moles[(button.row, button.col)]
            button.current_mole.timer.stop()
            button.current_mole = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MoleClicker_Start_GUI()
    main_window.show()
    
    sys.exit(app.exec_())
