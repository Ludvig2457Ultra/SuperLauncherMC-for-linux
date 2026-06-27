import os
import threading
import requests
import subprocess
import json
from uuid import uuid1
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit,
                              QComboBox, QProgressBar, QSpacerItem, QSizePolicy, QMessageBox)
from PyQt6.QtCore import Qt
from ...core.platform import PlatformSupport

class MinecraftPage(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.mc_dir = PlatformSupport.get_minecraft_path()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        layout.addWidget(self.username)

        self.version = QComboBox()
        layout.addWidget(self.version)

        self.loader = QComboBox()
        self.loader.addItems(["Vanilla", "Fabric", "Forge", "Quilt", "NeoForge"])
        layout.addWidget(self.loader)

        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum))

        self.progress = QProgressBar()
        self.progress.hide()
        layout.addWidget(self.progress)

        self.play_btn = QPushButton("Играть")
        self.play_btn.setStyleSheet("font-size: 18px; font-weight: bold; padding: 12px;")
        self.play_btn.clicked.connect(self._launch)
        layout.addWidget(self.play_btn)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self._load_versions()

    def _load_versions(self):
        def task():
            try:
                r = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json", timeout=15)
                data = r.json()
                for v in data.get("versions", []):
                    if v["type"] == "release":
                        self.version.addItem(v["id"])
            except Exception:
                self.version.addItem("1.20.4")
        threading.Thread(target=task, daemon=True).start()

    def _launch(self):
        ver = self.version.currentText()
        username = self.username.text().strip() or "Player"
        loader = self.loader.currentText().lower()
        java = self.main.config.get("java_path", "")
        max_ram = self.main.config.get("max_ram", 4096)

        self.progress.show()
        self.progress.setValue(0)

        def run():
            try:
                # Try minecraft_launcher_lib first
                try:
                    from minecraft_launcher_lib.utils import get_minecraft_directory
                    from minecraft_launcher_lib.install import install_minecraft_version
                    from minecraft_launcher_lib.command import get_minecraft_command

                    install_minecraft_version(ver, self.mc_dir)
                    options = {
                        "username": username, "uuid": str(uuid1()), "token": "",
                        "jvmArguments": [f"-Xmx{max_ram}M"],
                        "launcherName": "SuperLauncher", "launcherVersion": "2.0",
                    }
                    if java and os.path.exists(java):
                        options["executablePath"] = java
                    cmd = get_minecraft_command(ver, self.mc_dir, options)
                    subprocess.Popen(cmd, cwd=self.mc_dir).wait()
                except ImportError:
                    # Fallback: try to run directly
                    versions_dir = os.path.join(self.mc_dir, "versions", ver)
                    jar = os.path.join(versions_dir, f"{ver}.jar")
                    if not os.path.exists(jar):
                        QMessageBox.critical(self, "Ошибка", f"Версия {ver} не установлена")
                        return
                    args = [java or "java", f"-Xmx{max_ram}M", "-jar", jar,
                            "--username", username, "--version", ver]
                    subprocess.Popen(args, cwd=self.mc_dir).wait()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка запуска", str(e))
            finally:
                self.progress.hide()

        threading.Thread(target=run, daemon=True).start()
