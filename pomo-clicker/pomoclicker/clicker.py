from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QMainWindow, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy

from .data import *
from .styles import *
from .shop import *


class ClickerWindow(QMainWindow):

    click_update_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clicker!@")
        self.setFixedSize(400, 300)
        self.setStyleSheet(stats_style)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        center_layout = QHBoxLayout()
        main_layout.addLayout(center_layout)
        
        center_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        
        content_layout = QVBoxLayout()
        center_layout.addLayout(content_layout)
        
        center_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.clicks = getClicks()

        self.clickLabel = QLabel(f"{self.clicks}")
        self.clickLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.clickLabel.setMinimumSize(150, 60)
        
        clickButton = QPushButton("Click me!")
        clickButton.setMinimumSize(150, 60)
        clickButton.setCursor(Qt.CursorShape.PointingHandCursor)
        
        content_layout.addWidget(self.clickLabel)
        content_layout.addWidget(clickButton)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        main_layout.insertStretch(0, 1)
        main_layout.addStretch(1)

        clickButton.clicked.connect(self.__Click)

    def __Click(self):
        click_multiplier = getClickerLevel()
        addClicks(click_multiplier)
        self.updateClicksDisplay()  # Используйте новый метод
        self.click_update_signal.emit()

    def updateClicksDisplay(self):
        self.clicks = getClicks()
        self.clickLabel.setText(f"{self.clicks}")
        