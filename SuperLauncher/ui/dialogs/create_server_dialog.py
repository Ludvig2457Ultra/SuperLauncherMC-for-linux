import threading
import requests
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel,
                              QPushButton, QLineEdit, QComboBox, QSlider, QMessageBox)
from PyQt6.QtCore import Qt

class CreateServerDialog(QDialog):
    def __init__(self, main):
        super().__init__(main)
        self.main = main
        self.setWindowTitle("Создать сервер")
        self.setFixedSize(400, 350)

        layout = QFormLayout(self)
        self.name = QLineEdit()
        self.name.setPlaceholderText("Имя сервера")
        layout.addRow("Имя:", self.name)

        self.port = QLineEdit("25565")
        layout.addRow("Порт:", self.port)

        self.version = QComboBox()
        self.version.addItem("Загрузка...")
        layout.addRow("Версия:", self.version)

        self.core = QComboBox()
        self.core.addItems(["Paper", "Purpur", "Vanilla", "Fabric", "Quilt"])
        layout.addRow("Ядро:", self.core)

        self.ram = QSlider(Qt.Orientation.Horizontal)
        self.ram.setRange(1, 16)
        self.ram.setValue(4)
        self.ram_lbl = QLabel("4 GB")
        self.ram.valueChanged.connect(lambda v: self.ram_lbl.setText(f"{v} GB"))
        ram_w = QVBoxLayout()
        ram_w.addWidget(self.ram)
        ram_w.addWidget(self.ram_lbl)
        layout.addRow("RAM:", ram_w)

        create_btn = QPushButton("Создать")
        create_btn.clicked.connect(self._create)
        layout.addRow(create_btn)

        self._fetch_versions()

    def _fetch_versions(self):
        def task():
            try:
                r = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json", timeout=10)
                versions = [v["id"] for v in r.json()["versions"] if v["type"] == "release"]
                self.version.clear()
                self.version.addItems(versions)
            except Exception:
                self.version.clear()
                self.version.addItems(["1.20.4", "1.20.1"])
        threading.Thread(target=task, daemon=True).start()

    def _create(self):
        name = self.name.text().strip()
        port = self.port.text().strip()
        if not name or not port.isdigit():
            QMessageBox.warning(self, "Ошибка", "Введите корректное имя и порт")
            return
        path = self.main.servers.create(name, int(port), self.version.currentText(), self.core.currentText())
        servers = self.main.servers.load_servers()
        servers.append({"name": name, "ip": f"localhost:{port}", "managed": True,
                        "ram_gb": self.ram.value(), "version": self.version.currentText(),
                        "core": self.core.currentText()})
        self.main.servers.save_servers(servers)
        self.accept()
