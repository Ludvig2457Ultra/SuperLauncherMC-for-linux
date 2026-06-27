import os
import requests
import threading
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QComboBox, QListWidget, QListWidgetItem,
    QProgressBar, QDialog, QMessageBox
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon, QCursor
from ...core.platform import PlatformSupport

class ModsPage(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.mods_dir = os.path.join(PlatformSupport.get_minecraft_path(), 'mods')
        os.makedirs(self.mods_dir, exist_ok=True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)

        title = QLabel("\u25A3   \u041C\u043E\u0434\u044B")
        title.setStyleSheet("font-size: 26px; font-weight: bold; color: white;")
        layout.addWidget(title)

        row = QHBoxLayout()
        self.source = QComboBox()
        self.source.addItems(["Modrinth", "CurseForge"])
        row.addWidget(self.source)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("\u041F\u043E\u0438\u0441\u043A \u043C\u043E\u0434\u0430...")
        self.search_input.returnPressed.connect(self.search)
        row.addWidget(self.search_input, 1)
        search_btn = QPushButton("\u041F\u043E\u0438\u0441\u043A")
        search_btn.clicked.connect(self.search)
        row.addWidget(search_btn)
        layout.addLayout(row)

        self.list = QListWidget()
        self.list.setIconSize(QSize(32, 32))
        self.list.setSpacing(2)
        self.list.itemDoubleClicked.connect(self._install)
        layout.addWidget(self.list, 1)

        btn_row = QHBoxLayout()
        open_btn = QPushButton("\u041E\u0442\u043A\u0440\u044B\u0442\u044C \u043F\u0430\u043F\u043A\u0443")
        open_btn.clicked.connect(lambda: os.startfile(self.mods_dir))
        btn_row.addWidget(open_btn)
        del_btn = QPushButton("\u0423\u0434\u0430\u043B\u0438\u0442\u044C \u0432\u0441\u0451")
        del_btn.setStyleSheet("background: #f44336;")
        del_btn.clicked.connect(self._delete_all)
        btn_row.addWidget(del_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        self._load_featured()

    def _load_featured(self):
        def task():
            try:
                r = requests.get("https://api.modrinth.com/v2/search?limit=20&index=downloads",
                                 headers={"User-Agent": "SuperLauncher/2.0"}, timeout=10)
                for hit in r.json().get("hits", []):
                    item = QListWidgetItem(f"{hit['title']}  \u2B07{hit.get('downloads',0)}  \u2014 {hit.get('description','')[:60]}")
                    item.setData(Qt.ItemDataRole.UserRole, ("modrinth", hit["project_id"]))
                    self.list.addItem(item)
                    if hit.get("icon_url"):
                        self._load_icon(item, hit["icon_url"])
            except Exception:
                pass
        threading.Thread(target=task, daemon=True).start()

    def _load_icon(self, item, url):
        def task():
            try:
                r = requests.get(url, timeout=5)
                if r.status_code == 200:
                    pm = QPixmap()
                    pm.loadFromData(r.content)
                    if not pm.isNull():
                        item.setIcon(QIcon(pm.scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio,
                                                       Qt.TransformationMode.SmoothTransformation)))
            except Exception:
                pass
        threading.Thread(target=task, daemon=True).start()

    def search(self):
        query = self.search_input.text().strip()
        source = self.source.currentText()
        self.list.clear()

        def task():
            try:
                if source == "Modrinth":
                    r = requests.get(f"https://api.modrinth.com/v2/search?query={query}&limit=30",
                                     headers={"User-Agent": "SuperLauncher/2.0"}, timeout=10)
                    for hit in r.json().get("hits", []):
                        if hit.get("project_type") != "mod":
                            continue
                        item = QListWidgetItem(f"{hit['title']}  \u2B07{hit.get('downloads',0)}  \u2014 {hit.get('description','')[:60]}")
                        item.setData(Qt.ItemDataRole.UserRole, ("modrinth", hit["project_id"]))
                        self.list.addItem(item)
                        if hit.get("icon_url"):
                            self._load_icon(item, hit["icon_url"])
                else:
                    params = {"gameId": 432, "classId": 6, "searchFilter": query,
                              "pageSize": 30, "sortField": 2, "sortOrder": "desc"}
                    r = requests.get("https://api.curseforge.com/v1/mods/search", params=params,
                                     headers={"x-api-key": self.main.config.get_cf_api_key(),
                                              "Accept": "application/json"}, timeout=15)
                    for mod in r.json().get("data", []):
                        item = QListWidgetItem(f"{mod.get('name','?')}  \u2B07{mod.get('downloadCount',0)}  \u2014 {mod.get('summary','')[:60]}")
                        item.setData(Qt.ItemDataRole.UserRole, ("curseforge", mod["id"]))
                        self.list.addItem(item)
                        logo = mod.get("logo", {})
                        if logo and logo.get("url"):
                            self._load_icon(item, logo["url"])
                self.list.setCurrentRow(0)
            except Exception as e:
                QMessageBox.critical(self, "\u041E\u0448\u0438\u0431\u043A\u0430", str(e))

        threading.Thread(target=task, daemon=True).start()

    def _install(self, item):
        source, mod_id = item.data(Qt.ItemDataRole.UserRole)
        threading.Thread(target=lambda: self._do_install(source, mod_id), daemon=True).start()

    def _do_install(self, source, mod_id):
        try:
            if source == "modrinth":
                r = requests.get(f"https://api.modrinth.com/v2/project/{mod_id}/version",
                                 headers={"User-Agent": "SuperLauncher/2.0"}, timeout=10)
                versions = r.json()
                for v in versions:
                    for f in v.get("files", []):
                        if f.get("filename", "").endswith(".jar"):
                            url = f["url"]
                            filename = f["filename"]
                            save = os.path.join(self.mods_dir, filename)
                            r2 = requests.get(url, timeout=120, stream=True)
                            with open(save, "wb") as fh:
                                for chunk in r2.iter_content(8192):
                                    if chunk:
                                        fh.write(chunk)
                            QMessageBox.information(self, "\u0413\u043E\u0442\u043E\u0432\u043E",
                                                     f"\u041C\u043E\u0434 \u0443\u0441\u0442\u0430\u043D\u043E\u0432\u043B\u0435\u043D: {filename}")
                            return
            else:
                r = requests.get(f"https://api.curseforge.com/v1/mods/{mod_id}/files",
                                 headers={"x-api-key": self.main.config.get_cf_api_key(),
                                          "Accept": "application/json"}, timeout=10)
                files = r.json().get("data", [])
                if not files:
                    QMessageBox.warning(self, "\u041E\u0448\u0438\u0431\u043A\u0430", "\u041D\u0435\u0442 \u0444\u0430\u0439\u043B\u043E\u0432")
                    return
                # just get download URL
                file_id = files[0]["id"]
                r2 = requests.get(f"https://api.curseforge.com/v1/mods/{mod_id}/files/{file_id}/download-url",
                                  headers={"x-api-key": self.main.config.get_cf_api_key(),
                                           "Accept": "application/json"}, timeout=10)
                dl_url = r2.json().get("data", "")
                if dl_url:
                    filename = files[0].get("fileName", "mod.jar")
                    save = os.path.join(self.mods_dir, filename)
                    r3 = requests.get(dl_url, timeout=120, stream=True)
                    with open(save, "wb") as fh:
                        for chunk in r3.iter_content(8192):
                            if chunk:
                                fh.write(chunk)
                    QMessageBox.information(self, "\u0413\u043E\u0442\u043E\u0432\u043E",
                                             f"\u041C\u043E\u0434 \u0443\u0441\u0442\u0430\u043D\u043E\u0432\u043B\u0435\u043D: {filename}")
        except Exception as e:
            QMessageBox.critical(self, "\u041E\u0448\u0438\u0431\u043A\u0430", str(e))

    def _delete_all(self):
        from PyQt6.QtWidgets import QMessageBox
        reply = QMessageBox.question(self, "\u0423\u0434\u0430\u043B\u0435\u043D\u0438\u0435",
                                      "\u0423\u0434\u0430\u043B\u0438\u0442\u044C \u0432\u0441\u0435 \u043C\u043E\u0434\u044B?",
                                      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            count = 0
            for f in os.listdir(self.mods_dir):
                if f.endswith(".jar"):
                    try:
                        os.remove(os.path.join(self.mods_dir, f))
                        count += 1
                    except Exception:
                        pass
            QMessageBox.information(self, "\u0413\u043E\u0442\u043E\u0432\u043E", f"\u0423\u0434\u0430\u043B\u0435\u043D\u043E: {count}")
