import os
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                              QTextEdit, QLineEdit, QTabWidget, QWidget, QFormLayout,
                              QCheckBox, QSpinBox, QSlider, QListWidget, QMessageBox)
from PyQt6.QtCore import Qt

class ServerControlDialog(QDialog):
    def __init__(self, name, path, main):
        super().__init__(main)
        self.setWindowTitle(f"Сервер: {name}")
        self.resize(700, 500)
        layout = QVBoxLayout(self)
        tabs = QTabWidget()
        layout.addWidget(tabs)

        # Console tab
        console = QWidget()
        cl = QVBoxLayout(console)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setStyleSheet("background: #1a1a2e; color: #00ff00; font-family: monospace;")
        cl.addWidget(self.output)

        cmd_row = QHBoxLayout()
        self.cmd_input = QLineEdit()
        self.cmd_input.setPlaceholderText("Введите команду...")
        self.cmd_input.returnPressed.connect(self._send_cmd)
        cmd_row.addWidget(self.cmd_input)
        send_btn = QPushButton("Отправить")
        send_btn.clicked.connect(self._send_cmd)
        cmd_row.addWidget(send_btn)
        cl.addLayout(cmd_row)

        tabs.addTab(console, "Консоль")

        # Settings tab
        settings = QWidget()
        sl = QFormLayout(settings)
        self.eula = QCheckBox("Принять EULA")
        sl.addRow("EULA:", self.eula)
        self.offline = QCheckBox("Offline mode")
        sl.addRow("Режим:", self.offline)
        self.max_players = QSpinBox()
        self.max_players.setRange(1, 100)
        self.max_players.setValue(20)
        sl.addRow("Макс. игроков:", self.max_players)
        self.motd = QLineEdit("A SuperLauncher Server")
        sl.addRow("MOTD:", self.motd)
        tabs.addTab(settings, "Настройки")

        self.exec()
