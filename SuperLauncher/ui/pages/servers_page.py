import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                              QLineEdit, QScrollArea, QFrame, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor

class ServersPage(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)

        title = QLabel("Серверы")
        title.setStyleSheet("font-size: 26px; font-weight: bold; color: white;")
        layout.addWidget(title)

        create_btn = QPushButton("Создать сервер")
        create_btn.clicked.connect(self._create)
        layout.addWidget(create_btn)

        row = QHBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Имя сервера")
        row.addWidget(self.name_input)
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("IP или домен")
        row.addWidget(self.ip_input)
        add_btn = QPushButton("Добавить")
        add_btn.clicked.connect(self._add)
        row.addWidget(add_btn)
        layout.addLayout(row)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.container = QWidget()
        self.container_layout = QVBoxLayout(self.container)
        scroll.setWidget(self.container)
        layout.addWidget(scroll, 1)

        self._refresh()

    def _refresh(self):
        for i in reversed(range(self.container_layout.count())):
            w = self.container_layout.itemAt(i).widget()
            if w: w.deleteLater()

        servers = self.main.servers.load_servers()
        for s in servers:
            card = QFrame()
            card.setStyleSheet("QFrame { background: rgba(40,40,55,0.9); border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; padding: 10px; margin: 2px; }")
            cl = QHBoxLayout(card)
            cl.addWidget(QLabel(f"<b>{s['name']}</b>", styleSheet="font-size: 15px; color: white;"))
            cl.addWidget(QLabel(s.get('ip',''), styleSheet="color: #4facfe;"))
            cl.addStretch()
            if s.get('managed'):
                console_btn = QPushButton("Консоль")
                console_btn.clicked.connect(lambda checked, n=s['name']: self._console(n))
                cl.addWidget(console_btn)
            del_btn = QPushButton("Удалить")
            del_btn.clicked.connect(lambda checked, n=s['name']: self._delete(n))
            cl.addWidget(del_btn)
            self.container_layout.addWidget(card)
        self.container_layout.addStretch()

    def _add(self):
        name = self.name_input.text().strip()
        ip = self.ip_input.text().strip()
        if not name or not ip:
            QMessageBox.warning(self, "Ошибка", "Заполните поля")
            return
        servers = self.main.servers.load_servers()
        servers.append({"name": name, "ip": ip, "managed": False})
        self.main.servers.save_servers(servers)
        self._refresh()
        self.name_input.clear()
        self.ip_input.clear()

    def _create(self):
        from ..dialogs.create_server_dialog import CreateServerDialog
        dlg = CreateServerDialog(self.main)
        if dlg.exec():
            self._refresh()

    def _console(self, name):
        from ..dialogs.server_control_dialog import ServerControlDialog
        path = os.path.join("servers", name)
        dlg = ServerControlDialog(name, path, self.main)
        dlg.exec()

    def _delete(self, name):
        reply = QMessageBox.question(self, "Удаление", f"Удалить сервер '{name}'?",
                                      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            servers = self.main.servers.load_servers()
            servers = [s for s in servers if s['name'] != name]
            self.main.servers.save_servers(servers)
            path = os.path.join("servers", name)
            if os.path.exists(path):
                import shutil
                shutil.rmtree(path, ignore_errors=True)
            self._refresh()
