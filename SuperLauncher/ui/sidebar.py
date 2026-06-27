from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QLinearGradient, QColor, QPen, QFont


class ModernSidebar(QWidget):
    WIDTH = 210

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(self.WIDTH)
        self._active = 0

        self._items = [
            ("🏠", "Главная"),
            ("👤", "Аккаунт"),
            ("📦", "Моды"),
            ("📥", "Сборки"),
            ("🎨", "Скины"),
            ("📰", "Новости"),
            ("🔄", "Обновления"),
            ("🖥️", "Серверы"),
            ("⚙️", "Настройки"),
            ("⛏️", "Minecraft"),
            ("🤖", "AI Агент"),
        ]
        self._buttons = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        header = QLabel("  SuperLauncher")
        header.setFixedHeight(60)
        header.setStyleSheet("font-size: 15px; font-weight: bold; color: #4facfe; padding-left: 16px; background: rgba(0,0,0,0.2);")
        header.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(header)

        for icon, label in self._items:
            btn = self._create_button(icon, label)
            self._buttons.append(btn)
            layout.addWidget(btn)

        layout.addStretch()

        ver = QLabel("  v2.0.0")
        ver.setFixedHeight(36)
        ver.setStyleSheet("font-size: 11px; color: #555; padding-left: 16px;")
        ver.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(ver)

    def _create_button(self, icon, label):
        btn = QPushButton(f"{icon}  {label}", self)
        btn.setFixedHeight(44)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setCheckable(True)
        btn.setFlat(True)
        font = QFont("Segoe UI", 11)
        font.setLetterSpacing(QFont.SpacingType.PercentageSpacing, 102)
        btn.setFont(font)
        idx = len(self._buttons)
        btn.clicked.connect(lambda checked, i=idx: self._on_click(i))
        return btn

    def _on_click(self, idx):
        self._active = idx
        self._update_buttons()
        parent = self.parent()
        while parent and not hasattr(parent, "navigate_to"):
            parent = parent.parent()
        if parent:
            parent.navigate_to(idx)

    def _update_buttons(self):
        for i, btn in enumerate(self._buttons):
            btn.setChecked(i == self._active)
            if i == self._active:
                btn.setStyleSheet(
                    "QPushButton { background: qlineargradient(x1:0,y1:0,x2:1,y2:1, "
                    "stop:0 rgba(79,172,254,0.25), stop:1 rgba(118,75,162,0.2)); "
                    "color: white; border: none; border-radius: 0px; "
                    "text-align: left; padding: 0 16px; border-left: 3px solid #4facfe; }")
            else:
                btn.setStyleSheet(
                    "QPushButton { background: transparent; color: #999; "
                    "border: none; text-align: left; padding: 0 16px; }"
                    "QPushButton:hover { background: rgba(255,255,255,0.04); color: #ddd; }")

    def paintEvent(self, event):
        rect = self.rect()
        if rect.width() < 1 or rect.height() < 1:
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        grad = QLinearGradient(0, 0, rect.width(), rect.height())
        grad.setColorAt(0.0, QColor(14, 14, 22))
        grad.setColorAt(1.0, QColor(10, 10, 18))
        p.fillRect(rect, grad)
        p.setPen(QPen(QColor(255, 255, 255, 10), 1))
        p.drawLine(rect.width() - 1, 0, rect.width() - 1, rect.height())
