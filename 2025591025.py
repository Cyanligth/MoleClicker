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
path = "./Scoreboard.csv" # 저장 경로
COLUMNS = ["닉네임", "총점", "클릭 수", "잡은 두더지 수", "명중률", "플레이 시간"]
MAX_RANK = 10
total_score = 0



class ScoreBoard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("두더지 랭킹 보드")
        self.setFixedSize(950, 400)
        self.ranking = []
        self.initUI()
        self.loadRank()

    def initUI(self):
        layout = QVBoxLayout()
        title = QLabel("🏆 두더지 잡기 랭킹 🏆", self)
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: purple;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.table = QTableWidget(MAX_RANK, len(COLUMNS))
        self.table.setHorizontalHeaderLabels(COLUMNS)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setStyleSheet("font-size: 15px;")
        layout.addWidget(self.table)
        self.setLayout(layout)

    def loadRank(self):
        self.ranking.clear()
        if os.path.exists(path):
            with open(path, 'r', newline='', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.ranking.append(row)
        self.sortAndCut()
        self.refreshRank()

    def saveRank(self):
        with open(path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=COLUMNS)
            writer.writeheader()
            for row in self.ranking[:MAX_RANK]:
                writer.writerow(row)

    def sortAndCut(self):
        self.ranking.sort(key=lambda x: int(x['총점']), reverse=True)
        self.ranking = self.ranking[:MAX_RANK]

    def refreshRank(self):
        self.table.clearContents()
        for i in range(MAX_RANK):
            if i < len(self.ranking):
                row = self.ranking[i]
                for j, k in enumerate(COLUMNS):
                    self.table.setItem(i, j, QTableWidgetItem(str(row[k])))
            else:
                for j in range(len(COLUMNS)):
                    self.table.setItem(i, j, QTableWidgetItem(""))

    def addNewScore(self, entry):
        self.ranking.append(entry)
        self.sortAndCut()
        self.saveRank()
        self.refreshRank()

class NicknameDialog(QWidget):
    def __init__(self, game_result, on_done_callback):
        super().__init__()
        self.setWindowTitle('닉네임 입력')
        self.setFixedSize(320, 120)
        self.game_result = game_result
        self.on_done_callback = on_done_callback
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        label = QLabel("닉네임을 입력하세요:", self)
        label.setStyleSheet("font-size: 15px;")
        layout.addWidget(label)

        self.nameEdit = QLineEdit()
        self.nameEdit.setMaxLength(8)
        self.nameEdit.setPlaceholderText("닉네임(8글자 이내)")
        self.nameEdit.returnPressed.connect(self.onSubmit)
        layout.addWidget(self.nameEdit)

        btn = QPushButton("OK")
        btn.clicked.connect(self.onSubmit)
        layout.addWidget(btn)
        self.setLayout(layout)

    def onSubmit(self):
        name = self.nameEdit.text().strip() or "NONAME"
        entry = {"닉네임": name}
        entry.update(self.game_result)
        self.close()
        self.on_done_callback(entry)
            
        


# 메인은 이 아래에
