from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QGridLayout
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QCursor

class HomePage(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = QLabel("SuperLauncher 2026")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #4facfe;")
        layout.addWidget(title)

        info = QFrame()
        info.setStyleSheet("QFrame { background: rgba(255,255,255,0.05); border-radius: 10px; padding: 15px; }")
        info_layout = QHBoxLayout(info)
        avatar = QLabel("\U0001F464")
        avatar.setStyleSheet("font-size: 48px; padding: 10px;")
        info_layout.addWidget(avatar)
        self.name_label = QLabel("Гость")
        self.name_label.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
        info_layout.addWidget(self.name_label)
        layout.addWidget(info)

        actions = QLabel("Быстрые действия")
        actions.setStyleSheet("font-size: 16px; font-weight: bold; color: white; margin-top: 10px;")
        layout.addWidget(actions)

        grid = QGridLayout()
        grid.setSpacing(10)
        btns = [
            ("\u25B6", "Minecraft", lambda: main.navigate_to(9)),
            ("\u2699", "Настройки", lambda: main.navigate_to(8)),
            ("\u25A3", "Моды", lambda: main.navigate_to(2)),
            ("\u2660", "Скины", lambda: main.navigate_to(4)),
            ("\u2B21", "Серверы", lambda: main.navigate_to(7)),
            ("\u25CB", "Аккаунт", lambda: main.navigate_to(1)),
        ]
        for i, (icon, text, cb) in enumerate(btns):
            btn = QPushButton(f"{icon}\n{text}")
            btn.setFixedSize(130, 80)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(cb)
            btn.setStyleSheet(
                "QPushButton { font-size: 14px; background: rgba(79,172,254,0.15); "
                "border: 1px solid rgba(79,172,254,0.3); border-radius: 10px; color: white; }"
                "QPushButton:hover { background: rgba(79,172,254,0.3); }")
            grid.addWidget(btn, i // 3, i % 3)
        layout.addLayout(grid)
        layout.addStretch()
