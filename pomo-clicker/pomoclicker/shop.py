from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QSpacerItem, QSizePolicy)

from .data import *
from .styles import *


class ShopWindow(QMainWindow):
    buy_upgrade_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PomoClicker")
        self.setFixedSize(420, 220)  # Увеличили высоту окна для новых кнопок
        
        # Стиль для основного окна
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2C3E50;
            }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15) 
        main_layout.setSpacing(20) 

        clicks = getClicks()
        upgrades = getUpgradesPomo()
        pomo_container = QWidget()
        pomo_layout = QHBoxLayout(pomo_container)
        pomo_layout.setContentsMargins(0, 0, 0, 0)
        pomo_layout.setSpacing(10)
        
        self.ug30btn = QPushButton(f"30min upgrade\ncost: {30*2*upgrades[0]} clicks")
        self.ug30btn.setMinimumSize(120, 60)
        self.ug30btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.ug30btn.setStyleSheet(upgrade_button_style)

        self.ug45btn = QPushButton(f"45min upgrade\ncost: {45*2*upgrades[1]} clicks")
        self.ug45btn.setMinimumSize(120, 60)
        self.ug45btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.ug45btn.setStyleSheet(upgrade_button_style)

        self.ug1hbtn = QPushButton(f"1h upgrade\ncost: {60*2*upgrades[2]} clicks")
        self.ug1hbtn.setMinimumSize(120, 60)
        self.ug1hbtn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.ug1hbtn.setStyleSheet(upgrade_button_style)

        pomo_layout.addWidget(self.ug30btn)
        pomo_layout.addWidget(self.ug45btn)
        pomo_layout.addWidget(self.ug1hbtn)
        
        clicker_container = QWidget()
        clicker_layout = QHBoxLayout(clicker_container)
        clicker_layout.setContentsMargins(0, 0, 0, 0)
        clicker_layout.setSpacing(10)
        
        clicker_layout.addStretch(1)
        
        self.ugCbtn = QPushButton(f"Clicker upgrade\ncost: {getClickerLevel()*20}$")
        self.ugCbtn.setMinimumSize(120, 60)
        self.ugCbtn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.ugCbtn.setStyleSheet(upgrade_button_style)

        self.ugACbtn = QPushButton(f"Auto-Clicker upgrade\ncost: {'НЕ РАБОТАЕТ'}$")
        self.ugACbtn.setMinimumSize(120, 60)
        self.ugACbtn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.ugACbtn.setStyleSheet(upgrade_button_style)
        
        clicker_layout.addWidget(self.ugCbtn)
        clicker_layout.addWidget(self.ugACbtn)
        clicker_layout.addStretch(1)
    
        main_layout.addWidget(pomo_container)
        main_layout.addWidget(clicker_container)
        main_layout.addStretch(1)
        
        self.ug30btn.clicked.connect(lambda: self.__BuyPomoUpgrade(30))
        self.ug45btn.clicked.connect(lambda: self.__BuyPomoUpgrade(45))
        self.ug1hbtn.clicked.connect(lambda: self.__BuyPomoUpgrade(60))
        self.ugCbtn.clicked.connect(self.__buyClickerUpgrade)
    
    def __BuyPomoUpgrade(self, minutes) -> None:
        clicks = getClicks()
        upgrades = getUpgradesPomo()

        if minutes == 30:
            upgrade = upgrades[0]
        if minutes == 45:
            upgrade = upgrades[1]
        if minutes == 60:
            upgrade = upgrades[2]
        
        cost = minutes*2*upgrade

        if clicks < cost:
            return None
        
        addUpgradePomo(minutes)
        setClicks(clicks-cost)
        upgrades = getUpgradesPomo()

        self.buy_upgrade_signal.emit()
        
        # Обновляем текст кнопок
        if minutes == 30:
            self.ug30btn.setText(f"30min upgrade\ncost: {30*2*upgrades[0]} clicks")
        if minutes == 45:
            self.ug45btn.setText(f"45min upgrade\ncost: {45*2*upgrades[1]} clicks")
        if minutes == 60:
            self.ug1hbtn.setText(f"1h upgrade\ncost: {60*2*upgrades[2]} clicks")

    def __buyClickerUpgrade(self) -> None:
        cost = getClickerLevel()*20
        money = getMoney()
        if cost > money:
            return None
        setMoney(money-cost)
        addClickerLevel()
        self.ugCbtn.setText(f"Clicker upgrade\ncost: {cost}$")
        self.buy_upgrade_signal.emit()