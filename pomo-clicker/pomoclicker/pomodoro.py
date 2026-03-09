from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
                             QHBoxLayout, QWidget, QPushButton)
from PyQt6.QtCore import QTimer, Qt, QUrl
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtGui import QFont

from .stats import *
from .shop import *
from .clicker import *
from .styles import *
from .data import *

import sys


class MainWindow(QMainWindow):

    stats_updated_signal = pyqtSignal()

    def __init__(self) -> None:

        #       BASIC
        super().__init__()
        self.setWindowTitle("PomoClicker")
        self.setFixedSize(400, 350)

        self.stats_window = StatsWindow()
        self.stats_window.hide()
        self.shop_window = ShopWindow()
        self.shop_window.hide()
        self.clicker_window = ClickerWindow()
        self.clicker_window.hide()

        self.clicker_window.click_update_signal.connect(self.__updateClicks)
        self.shop_window.buy_upgrade_signal.connect(self.__upgradePomo)
        self.stats_updated_signal.connect(self.stats_window.update_stats)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.effect = QSoundEffect()
        self.effect.setSource(QUrl.fromLocalFile("pomoclicker/sound.wav"))
        self.effect.setVolume(1)

        self.money = getMoney()
        self.clicks = getClicks()
        self.upgrades = getUpgradesPomo()
        self.mode = None

        #       ELEMENTS
        #money
        money_widget = QWidget()
        money_layout = QHBoxLayout(money_widget)
        self.money_label = QLabel(f"Money: ${self.money}\n"
                                 +f"Clicks: {self.clicks}")
        self.money_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.money_label.setStyleSheet("color: #FFFFFF;")
        self.money_label.setMinimumHeight(50)
        money_layout.addWidget(self.money_label)
        money_layout.addStretch()
        
        layout.addWidget(money_widget)
        layout.addSpacing(10)
        
        # time buttons
        time_buttons_layout = QHBoxLayout()
        self.btn_30min = QPushButton(f"30 min\n(+{10*self.upgrades[0]}$)")
        self.btn_45min = QPushButton(f"45 min\n(+{20*self.upgrades[1]}$)")
        self.btn_1h = QPushButton(f"1h\n(+{30*self.upgrades[2]}$)")
        
        for btn in [self.btn_30min, self.btn_45min, self.btn_1h]:
            btn.setStyleSheet(time_button_style)
        
        time_buttons_layout.addWidget(self.btn_30min)
        time_buttons_layout.addWidget(self.btn_45min)
        time_buttons_layout.addWidget(self.btn_1h)
        layout.addLayout(time_buttons_layout)
        layout.addSpacing(20) 
        
        # timer
        self.timer_label = QLabel("00:00")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_label.setFont(QFont("Arial", 50, QFont.Weight.Bold))
        self.timer_label.setStyleSheet("color: #2C3E50; background-color: #ECF0F1; border-radius: 10px;")
        self.timer_label.setMinimumHeight(52)
        layout.addWidget(self.timer_label)
        layout.addSpacing(20)  

        self.timer = QTimer()
        self.timer.timeout.connect(self.__updateTime)
        self.remaining_time = 0
        self.is_timer_running = False
        self.mode = 0
        
        # start button
        self.start_button = QPushButton("START TIMER")
        self.start_button.setStyleSheet(start_button_style)
        layout.addWidget(self.start_button)
        layout.addSpacing(20)
        
        # bottom buttons
        bottom_buttons_layout = QHBoxLayout()
        self.btn_clicker = QPushButton("Clicker")
        self.btn_shop = QPushButton("Shop")
        self.btn_stats = QPushButton("Stats")

        self.btn_shop.clicked.connect(self.__showShop)
        self.btn_stats.clicked.connect(self.__showStats)
        self.btn_clicker.clicked.connect(self.__showClicker)
        
        for btn in [self.btn_clicker, self.btn_shop, self.btn_stats]:
            btn.setStyleSheet(bottom_button_style)
        
        bottom_buttons_layout.addWidget(self.btn_clicker)
        bottom_buttons_layout.addWidget(self.btn_shop)
        bottom_buttons_layout.addWidget(self.btn_stats)
        layout.addLayout(bottom_buttons_layout)
        
        self.start_button.clicked.connect(self.__toggleTimer)
        self.btn_30min.clicked.connect(lambda: self.__setTime(30))
        self.btn_45min.clicked.connect(lambda: self.__setTime(45))
        self.btn_1h.clicked.connect(lambda: self.__setTime(60))
        self.__updateDisplay()

    def __setTime(self, minutes: int) -> None:
        if self.is_timer_running:
            self.timer.stop()
            self.is_timer_running = False
            self.start_button.setText("START TIMER")
        
        self.mode = minutes
        self.remaining_time = round(minutes * 60)
        self.__updateDisplay()

    def __toggleTimer(self) -> None:
        if self.is_timer_running:
            self.timer.stop()
            self.is_timer_running = False
            self.start_button.setText("START TIMER")
        else:
            if self.remaining_time > 0:
                self.timer.start(1000)
                self.is_timer_running = True
                self.start_button.setText("PAUSE TIMER")

    def __timeEnded(self) -> None:
        self.timer.stop()
        self.is_timer_running = False
        self.start_button.setText("START TIMER")

        upgrades = getUpgradesPomo()
        
        if self.mode == 30:
            self.money += 10 * upgrades[0]

        elif self.mode == 45:
            self.money += 20 * upgrades[1]

        elif self.mode == 60:
            self.money += 30 * upgrades[2]

        setMoney(self.money)
        setMileAge(self.mode)

        self.stats_updated_signal.emit()
        self.money_label.setText(f"Money: ${self.money}\n"
                                +f"Clicks: {self.clicks}")
        self.effect.play()

    def __updateTime(self) -> None:
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.__updateDisplay()
        else:
            self.__timeEnded() 

    def __updateClicks(self) -> None:
        self.clicks = getClicks()
        self.money_label.setText(f"Money: ${self.money}\n"
                                +f"Clicks: {self.clicks}")
        
    def __upgradePomo(self) -> None:
        upgrades = getUpgradesPomo()
        self.clicks = getClicks()
        self.money = getMoney()
        self.money_label.setText(f"Money: ${self.money}\n"
                                +f"Clicks: {self.clicks}")
        self.btn_30min.setText(f"30 min\n(+{10*upgrades[0]})")
        self.btn_45min.setText(f"45 min\n(+{20*upgrades[1]})")
        self.btn_1h.setText(f"1h\n(+{30*upgrades[2]})")
        self.clicker_window.updateClicksDisplay()

    def __updateDisplay(self) -> None:
        minutes = self.remaining_time // 60
        seconds = self.remaining_time % 60
        self.timer_label.setText(f"{minutes:02d}:{seconds:02d}")

    def __showShop(self) -> None: 
        self.shop_window.show()

    def __showStats(self) -> None:
        self.stats_window.update_stats()
        self.stats_window.show()

    def __showClicker(self) -> None:
        self.clicker_window.show()

def startApp() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
