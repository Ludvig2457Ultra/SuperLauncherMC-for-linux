import os
import json
import threading
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                              QLineEdit, QComboBox, QListWidget, QMessageBox, QFileDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor

class BuildsPage(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.mc_dir = os.path.join(os.getenv('APPDATA'), '.minecraft')
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)

        title = QLabel("Сборки")
        title.setStyleSheet("font-size: 26px; font-weight: bold; color: white;")
        layout.addWidget(title)

        row = QHBoxLayout()
        self.source = QComboBox()
        self.source.addItems(["Modrinth", "CurseForge"])
        row.addWidget(self.source)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск сборки...")
        row.addWidget(self.search_input, 1)
        btn_search = QPushButton("Поиск")
        btn_search.clicked.connect(self.search)
        row.addWidget(btn_search)
        btn_import = QPushButton(".mrpack")
        btn_import.clicked.connect(self.import_mrpack)
        row.addWidget(btn_import)
        layout.addLayout(row)

        self.list = QListWidget()
        self.list.setStyleSheet("QListWidget::item { padding: 8px; }")
        layout.addWidget(self.list, 1)

        btn_install = QPushButton("Установить")
        btn_install.clicked.connect(self.install)
        layout.addWidget(btn_install)

    def search(self):
        query = self.search_input.text().strip()
        source = self.source.currentText()
        self.list.clear()

        def task():
            try:
                results = self.main.builds.search_modrinth(query) if source == "Modrinth" else self.main.builds.search_curseforge(query)
                for r in results:
                    from PyQt6.QtWidgets import QListWidgetItem
                    item = QListWidgetItem(f"{r['name']}  ({r.get('downloads',0)} downloads)")
                    item.setData(Qt.ItemDataRole.UserRole, r)
                    self.list.addItem(item)
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
        threading.Thread(target=task, daemon=True).start()

    def install(self):
        item = self.list.currentItem()
        if not item:
            return
        mp = item.data(Qt.ItemDataRole.UserRole)
        source = mp.get("source", "modrinth")
        versions = self.main.builds.get_versions(mp["id"], source)
        if not versions:
            QMessageBox.warning(self, "Ошибка", "Нет версий")
            return
        selected = versions[0]  # pick first
        self.main.builds.download_and_install(selected, source, self.mc_dir)
        QMessageBox.information(self, "Готово", f"Сборка '{mp['name']}' установлена!")

    def import_mrpack(self):
        path, _ = QFileDialog.getOpenFileName(self, "Выберите .mrpack", "", "*.mrpack *.zip")
        if path:
            QMessageBox.information(self, "Импорт", "Импорт .mrpack пока в разработке")
