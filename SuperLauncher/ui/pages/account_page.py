from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QGroupBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor

class AccountPage(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = QLabel("\U0001F464 Мой Аккаунт")
        title.setStyleSheet("font-size: 26px; font-weight: bold; color: white;")
        layout.addWidget(title)

        info = QGroupBox("Информация")
        info.setStyleSheet("QGroupBox { color: #4facfe; font-weight: bold; border: 1px solid #4facfe; border-radius: 10px; margin-top: 10px; padding-top: 15px; } QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 8px; }")
        info_layout = QVBoxLayout(info)
        self.name_lbl = QLabel("Имя: Гость")
        self.name_lbl.setStyleSheet("color: white; font-size: 14px; padding: 5px;")
        self.status_lbl = QLabel("Статус: Бесплатная версия")
        self.status_lbl.setStyleSheet("color: white; font-size: 14px; padding: 5px;")
        info_layout.addWidget(self.name_lbl)
        info_layout.addWidget(self.status_lbl)
        layout.addWidget(info)

        license_group = QGroupBox("Лицензия")
        license_group.setStyleSheet("QGroupBox { color: #4facfe; font-weight: bold; border: 1px solid #4facfe; border-radius: 10px; margin-top: 10px; padding-top: 15px; } QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 8px; }")
        lic_layout = QVBoxLayout(license_group)
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Введите ключ лицензии...")
        lic_layout.addWidget(self.key_input)
        activate_btn = QPushButton("Активировать")
        activate_btn.clicked.connect(self._activate)
        activate_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        lic_layout.addWidget(activate_btn)
        layout.addWidget(license_group)

        login_btn = QPushButton("Войти / Зарегистрироваться")
        login_btn.clicked.connect(self._login)
        login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(login_btn)

        self.logout_btn = QPushButton("Выйти")
        self.logout_btn.clicked.connect(self._logout)
        self.logout_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.logout_btn.setStyleSheet("QPushButton { background: #f44336; }")
        self.logout_btn.hide()
        layout.addWidget(self.logout_btn)
        layout.addStretch()

    def _activate(self):
        key = self.key_input.text().strip()
        if not key:
            QMessageBox.warning(self, "Ошибка", "Введите ключ")
            return
        from PyQt6.QtWidgets import QMessageBox
        if not self.main.account.current_user:
            QMessageBox.warning(self, "Ошибка", "Требуется вход")
            return
        ok, msg = self.main.account.activate_license(key, self.main.account.current_user["user_id"])
        if ok:
            QMessageBox.information(self, "Успех", msg)
        else:
            QMessageBox.critical(self, "Ошибка", msg)

    def _login(self):
        from ..dialogs.login_dialog import LoginDialog
        dlg = LoginDialog(self.main.account, self)
        if dlg.exec():
            if dlg.user_data:
                self.name_lbl.setText(f"Имя: {dlg.user_data['username']}")
                self.status_lbl.setText(f"Статус: {dlg.user_data.get('license_tier', 'free').upper()}")
                self.logout_btn.show()

    def _logout(self):
        self.main.account.logout()
        self.name_lbl.setText("Имя: Гость")
        self.status_lbl.setText("Статус: Бесплатная версия")
        self.logout_btn.hide()
