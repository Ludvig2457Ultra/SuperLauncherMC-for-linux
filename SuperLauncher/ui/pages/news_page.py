from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from PyQt6.QtCore import Qt

class NewsPage(QWidget):
    def __init__(self, main):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)

        title = QLabel("Новости")
        title.setStyleSheet("font-size: 26px; font-weight: bold; color: white;")
        layout.addWidget(title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        cl = QVBoxLayout(container)
        cl.setSpacing(12)

        news = [
            ("2025-08-12 v1.4.0.7", "Добавлен Discord RPC"),
            ("2025-07-24 v1.4.0.5", "Поддержка скачивания модов из Modrinth и настройки лаунчера"),
            ("2025-07-23 v1.4.0.4", "Создание и управление Minecraft-серверами"),
            ("2025-07-23 v1.4.0.3", "Новый дизайн и восстановлен код"),
            ("2025-06-26 v1.4.0.2", "Новый дизайн, но утерян код"),
            ("2025-06-26 v1.3", "Лаунчер выйдет из беты"),
        ]

        for date, text in news:
            lbl = QLabel(f"<b>{date}</b>: {text}")
            lbl.setWordWrap(True)
            lbl.setStyleSheet("font-size: 14px; color: #ccc; padding: 10px; background: rgba(255,255,255,0.03); border-radius: 8px;")
            cl.addWidget(lbl)

        cl.addStretch()
        scroll.setWidget(container)
        layout.addWidget(scroll, 1)
