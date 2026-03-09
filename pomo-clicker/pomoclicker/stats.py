from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QMainWindow
from .data import *
from .styles import *


class StatsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PomoClicker - Statistics")
        self.setFixedSize(250, 150)
        self.setStyleSheet(stats_style)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        layout.setSpacing(0)

        sessions = getMileAge()
        sessions30 = sessions[0]
        sessions45 = sessions[1]
        sessions60 = sessions[2]
        allTime = round((sessions30*30 + sessions45*45 + sessions60*60)/60, 1)
        self.sessionsLabel = QLabel(f"Hours (all time): {allTime}\n"
                               f"30min sessions: {sessions30}\n"
                               f"45min sessions: {sessions45}\n"
                               f"60min sessions: {sessions60}")

        self.sessionsLabel.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.sessionsLabel.setMinimumHeight(130)
        self.sessionsLabel.setMinimumWidth(230)

        layout.addWidget(self.sessionsLabel)

    def update_stats(self):
        sessions = getMileAge()
        sessions30 = sessions[0]
        sessions45 = sessions[1]
        sessions60 = sessions[2]
        allTime = round((sessions30*30 + sessions45*45 + sessions60*60)/60, 1)
        self.sessionsLabel.setText(f"Hours (all time): {allTime}\n"
                                   f"30min sessions: {sessions30}\n"
                                   f"45min sessions: {sessions45}\n"
                                   f"60min sessions: {sessions60}")