import datetime
import threading
import requests
from packaging import version as pv
from pathlib import Path
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                              QProgressBar, QSplitter, QListWidget, QTextEdit, QFrame, QMessageBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor

class UpdatesPage(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.dl_url = None
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)

        title = QLabel("Обновления")
        title.setStyleSheet("font-size: 26px; font-weight: bold; color: white;")
        layout.addWidget(title)

        card = QFrame()
        card.setStyleSheet("QFrame { background: rgba(79,172,254,0.1); border: 1px solid rgba(79,172,254,0.3); border-radius: 12px; padding: 15px; }")
        cl = QHBoxLayout(card)
        cl.addWidget(QLabel("Текущая версия:"))
        self.ver_lbl = QLabel("v2.0.0_2026")
        self.ver_lbl.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
        cl.addWidget(self.ver_lbl)
        cl.addStretch()
        self.status_lbl = QLabel("Проверка...")
        self.status_lbl.setStyleSheet("color: #888;")
        cl.addWidget(self.status_lbl)
        layout.addWidget(card)

        self.update_card = QFrame()
        self.update_card.setVisible(False)
        self.update_card.setStyleSheet("QFrame { background: rgba(76,175,80,0.1); border: 1px solid rgba(76,175,80,0.4); border-radius: 12px; padding: 15px; }")
        ucl = QVBoxLayout(self.update_card)
        ucl.addWidget(QLabel("Доступно обновление!", styleSheet="color: #4caf50; font-size: 18px; font-weight: bold;"))
        self.dl_btn = QPushButton("Скачать")
        self.dl_btn.clicked.connect(self.start_dl)
        ucl.addWidget(self.dl_btn)
        self.progress = QProgressBar()
        self.progress.hide()
        ucl.addWidget(self.progress)
        layout.addWidget(self.update_card)

        self.releases = QListWidget()
        self.releases.setStyleSheet("QListWidget::item { padding: 8px; }")
        layout.addWidget(QLabel("История версий:"))
        layout.addWidget(self.releases, 1)

        QTimer.singleShot(1000, self.check)

    def check(self):
        def task():
            try:
                r = requests.get("https://api.github.com/repos/Ludvig2457Ultra/SuperLauncherMC/releases?per_page=10",
                                 headers={"Accept": "application/vnd.github.v3+json"}, timeout=15)
                if r.status_code != 200:
                    return
                current = pv.parse("2.0.0")
                for rel in r.json():
                    try:
                        v = pv.parse(rel.get("tag_name", ""))
                    except Exception:
                        continue
                    if v > current:
                        self.update_card.setVisible(True)
                        self.dl_url = rel.get("assets", [{}])[0].get("browser_download_url", "") if rel.get("assets") else ""
                        break
                self.status_lbl.setText("Актуальная версия")
                for rel in r.json()[:10]:
                    self.releases.addItem(f"{rel.get('tag_name','')}  {rel.get('published_at','')[:10]}")
            except Exception:
                self.status_lbl.setText("Ошибка проверки")
        threading.Thread(target=task, daemon=True).start()

    def start_dl(self):
        if not self.dl_url:
            return
        self.progress.show()
        self.progress.setValue(0)
        def task():
            try:
                r = requests.get(self.dl_url, stream=True, timeout=30)
                total = int(r.headers.get("content-length", 0))
                path = Path("SuperLauncher_update.exe")
                with open(path, "wb") as f:
                    written = 0
                    for chunk in r.iter_content(65536):
                        if chunk:
                            f.write(chunk)
                            written += len(chunk)
                            if total > 0:
                                self.progress.setValue(int(written * 100 / total))
                QMessageBox.information(self, "Готово", f"Скачано в {path}")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))
        threading.Thread(target=task, daemon=True).start()
