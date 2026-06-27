import requests
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                              QLineEdit, QComboBox, QSlider, QRadioButton, QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt

class SettingsPage(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        def add_row(label, widget):
            row = QHBoxLayout()
            row.addWidget(QLabel(label, styleSheet="color: white; min-width: 150px;"))
            row.addWidget(widget, 1)
            layout.addLayout(row)

        self.theme = QComboBox()
        self.theme.addItems(["dark", "light"])
        self.theme.setCurrentText(self.main.config.get("theme", "dark"))
        add_row("Тема:", self.theme)

        self.lang = QComboBox()
        self.lang.addItems(["ru", "en"])
        self.lang.setCurrentText(self.main.config.get("language", "ru"))
        add_row("Язык:", self.lang)

        self.mode_launcher = QRadioButton("minecraft-launcher-lib")
        self.mode_java = QRadioButton("Java")
        mode = QWidget()
        ml = QVBoxLayout(mode)
        ml.setContentsMargins(0, 0, 0, 0)
        ml.addWidget(self.mode_launcher)
        ml.addWidget(self.mode_java)
        if self.main.config.get("launch_mode") == "java":
            self.mode_java.setChecked(True)
        else:
            self.mode_launcher.setChecked(True)
        add_row("Режим запуска:", mode)

        self.java_path = QLineEdit(self.main.config.get("java_path", ""))
        browse_btn = QPushButton("Обзор")
        browse_btn.clicked.connect(lambda: self.java_path.setText(
            QFileDialog.getOpenFileName(self, "Выберите Java", "", "*.exe")[0]))
        jp = QWidget()
        jl = QHBoxLayout(jp)
        jl.setContentsMargins(0, 0, 0, 0)
        jl.addWidget(self.java_path, 1)
        jl.addWidget(browse_btn)
        add_row("Путь к Java:", jp)

        self.ram = QSlider(Qt.Orientation.Horizontal)
        self.ram.setRange(1024, 32768)
        self.ram.setValue(self.main.config.get("max_ram", 4096))
        self.ram_lbl = QLabel(f"{self.ram.value()} MB", styleSheet="color: white;")
        self.ram.valueChanged.connect(lambda v: self.ram_lbl.setText(f"{v} MB"))
        ram_w = QWidget()
        rl = QHBoxLayout(ram_w)
        rl.setContentsMargins(0, 0, 0, 0)
        rl.addWidget(self.ram, 1)
        rl.addWidget(self.ram_lbl)
        add_row("ОЗУ:", ram_w)

        self.jvm = QLineEdit(self.main.config.get("jvm_args", ""))
        add_row("JVM аргументы:", self.jvm)

        self.cf_key = QLineEdit(self.main.config.get("curseforge_api_key", ""))
        test_btn = QPushButton("Проверить")
        test_btn.clicked.connect(self._test_cf)
        cf_w = QWidget()
        cfl = QHBoxLayout(cf_w)
        cfl.setContentsMargins(0, 0, 0, 0)
        cfl.addWidget(self.cf_key, 1)
        cfl.addWidget(test_btn)
        add_row("CurseForge API Key:", cf_w)

        save_btn = QPushButton("Сохранить")
        save_btn.clicked.connect(self._save)
        layout.addWidget(save_btn)

    def _test_cf(self):
        key = self.cf_key.text().strip()
        if not key:
            QMessageBox.warning(self, "Ошибка", "Введите ключ")
            return
        try:
            r = requests.get("https://api.curseforge.com/v1/mods/search?gameId=432&classId=6&pageSize=1",
                             headers={"x-api-key": key, "Accept": "application/json"}, timeout=10)
            if r.status_code == 200:
                QMessageBox.information(self, "Успех", "Ключ работает!")
            else:
                QMessageBox.critical(self, "Ошибка", f"HTTP {r.status_code}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def _save(self):
        self.main.config.set("theme", self.theme.currentText())
        self.main.config.set("language", self.lang.currentText())
        self.main.config.set("launch_mode", "java" if self.mode_java.isChecked() else "launcher_lib")
        self.main.config.set("java_path", self.java_path.text())
        self.main.config.set("max_ram", self.ram.value())
        self.main.config.set("jvm_args", self.jvm.text())
        self.main.config.set("curseforge_api_key", self.cf_key.text().strip())
        self.main.config.save()
        self.main.config.invalidate_cf_key()
        self.main.theme.set_dark(self.theme.currentText() == "dark")
        self.main.setStyleSheet(self.main.theme.stylesheet())
        QMessageBox.information(self, "Готово", "Настройки сохранены")
