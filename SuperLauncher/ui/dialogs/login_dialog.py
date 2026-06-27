from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                              QLineEdit, QTabWidget, QWidget, QFormLayout, QCheckBox, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor

class LoginDialog(QDialog):
    def __init__(self, account_system, parent=None):
        super().__init__(parent)
        self.account = account_system
        self.user_data = None
        self.setWindowTitle("Вход / Регистрация")
        self.setFixedSize(400, 450)

        layout = QVBoxLayout(self)
        title = QLabel("SuperLauncher Аккаунт")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #4facfe;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        tabs = QTabWidget()

        login_tab = QWidget()
        fl = QFormLayout(login_tab)
        self.login_user = QLineEdit()
        self.login_user.setPlaceholderText("Имя или Email")
        fl.addRow("Логин:", self.login_user)
        self.login_pass = QLineEdit()
        self.login_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_pass.setPlaceholderText("Пароль")
        fl.addRow("Пароль:", self.login_pass)
        tabs.addTab(login_tab, "Вход")

        reg_tab = QWidget()
        rl = QFormLayout(reg_tab)
        self.reg_user = QLineEdit()
        self.reg_user.setPlaceholderText("Имя пользователя")
        rl.addRow("Имя:", self.reg_user)
        self.reg_email = QLineEdit()
        self.reg_email.setPlaceholderText("Email")
        rl.addRow("Email:", self.reg_email)
        self.reg_pass = QLineEdit()
        self.reg_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.reg_pass.setPlaceholderText("Пароль")
        rl.addRow("Пароль:", self.reg_pass)
        self.reg_pass2 = QLineEdit()
        self.reg_pass2.setEchoMode(QLineEdit.EchoMode.Password)
        self.reg_pass2.setPlaceholderText("Повторите пароль")
        rl.addRow("Подтверждение:", self.reg_pass2)
        tabs.addTab(reg_tab, "Регистрация")

        layout.addWidget(tabs)

        btns = QHBoxLayout()
        login_btn = QPushButton("Войти")
        login_btn.clicked.connect(self._login)
        btns.addWidget(login_btn)
        reg_btn = QPushButton("Зарегистрироваться")
        reg_btn.clicked.connect(self._register)
        btns.addWidget(reg_btn)
        cancel_btn = QPushButton("Отмена")
        cancel_btn.clicked.connect(self.reject)
        btns.addWidget(cancel_btn)
        layout.addLayout(btns)

    def _login(self):
        ok, result = self.account.login(self.login_user.text(), self.login_pass.text())
        if ok:
            self.user_data = result
            self.accept()
        else:
            QMessageBox.critical(self, "Ошибка", result)

    def _register(self):
        if self.reg_pass.text() != self.reg_pass2.text():
            QMessageBox.warning(self, "Ошибка", "Пароли не совпадают")
            return
        ok, result = self.account.register(self.reg_user.text(), self.reg_email.text(), self.reg_pass.text())
        if ok:
            self.user_data = result
            self.accept()
        else:
            QMessageBox.critical(self, "Ошибка", result)
