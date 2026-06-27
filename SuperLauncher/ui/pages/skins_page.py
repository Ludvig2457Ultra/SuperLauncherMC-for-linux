from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                              QGridLayout, QScrollArea, QMessageBox, QFileDialog, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor

class SkinsPage(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)

        title = QLabel("Скины")
        title.setStyleSheet("font-size: 26px; font-weight: bold; color: white;")
        layout.addWidget(title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        self.grid = QGridLayout(container)
        self.grid.setSpacing(10)

        skins = [
            ("default", "Стандартный", "\U0001F464", True, 0),
            ("santa", "Санта", "\U0001F385", False, 500),
            ("snowman", "Снеговик", "\u26C4", False, 300),
            ("reindeer", "Олень", "\U0001F98C", False, 400),
            ("star", "Звезда", "\u2B50", False, 600),
            ("gift", "Подарок", "\U0001F381", False, 450),
        ]

        for i, (sid, name, icon, unlocked, price) in enumerate(skins):
            card = QFrame()
            card.setStyleSheet("QFrame { background: rgba(255,255,255,0.05); border-radius: 10px; padding: 10px; } QFrame:hover { border: 1px solid #4facfe; }")
            card.setFixedSize(160, 170)
            cl = QVBoxLayout(card)
            icon_lbl = QLabel(icon)
            icon_lbl.setStyleSheet("font-size: 40px;")
            icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            cl.addWidget(icon_lbl)
            name_lbl = QLabel(name)
            name_lbl.setStyleSheet("color: white; font-weight: bold; font-size: 14px;")
            name_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            cl.addWidget(name_lbl)
            btn = QPushButton("Применить" if unlocked else f"{price} XP")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked, s=sid: self._apply(s))
            cl.addWidget(btn)
            self.grid.addWidget(card, i // 3, i % 3)

        scroll.setWidget(container)
        layout.addWidget(scroll, 1)

        upload_btn = QPushButton("Загрузить свой скин")
        upload_btn.clicked.connect(self._upload)
        upload_btn.setStyleSheet("border: 2px dashed #4facfe; padding: 15px; font-size: 14px;")
        layout.addWidget(upload_btn)

    def _apply(self, skin_id):
        user = self.main.account.current_user
        if not user:
            QMessageBox.warning(self, "Ошибка", "Требуется вход")
            return
        ok, msg = self.main.skins.unlock(skin_id, user)
        if ok:
            QMessageBox.information(self, "Успех", msg)
        else:
            status, m = self.main.skins.unlock(skin_id, user)
            QMessageBox.warning(self, "Ошибка", m)

    def _upload(self):
        path, _ = QFileDialog.getOpenFileName(self, "Выберите скин", "", "Images (*.png *.jpg)")
        if path:
            user = self.main.account.current_user
            if not user:
                QMessageBox.warning(self, "Ошибка", "Требуется вход")
                return
            ok, msg = self.main.skins.upload_custom(path, user)
            if ok:
                QMessageBox.information(self, "Успех", f"Скин загружен! ID: {msg}")
            else:
                QMessageBox.warning(self, "Ошибка", msg)
