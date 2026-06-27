#include "LoginDialog.h"
#include <QMessageBox>

LoginDialog::LoginDialog(QWidget *parent)
    : QDialog(parent)
{
    setupUi();
}

void LoginDialog::setupUi()
{
    setWindowTitle("Вход в аккаунт");
    setFixedSize(380, 300);
    setStyleSheet("QDialog { background: #1E1E2E; }");

    auto *layout = new QVBoxLayout(this);
    layout->setContentsMargins(24, 24, 24, 24);
    layout->setSpacing(12);

    auto *title = new QLabel("Вход", this);
    title->setStyleSheet("color: white; font-size: 20px; font-weight: bold;");
    title->setAlignment(Qt::AlignCenter);
    layout->addWidget(title);

    m_username = new QLineEdit(this);
    m_username->setPlaceholderText("Логин или Email");
    m_username->setStyleSheet(
        "QLineEdit { background: rgba(255,255,255,0.08); color: white; "
        "border: 1px solid rgba(255,255,255,0.15); border-radius: 6px; "
        "padding: 10px; font-size: 13px; }");

    m_password = new QLineEdit(this);
    m_password->setPlaceholderText("Пароль");
    m_password->setEchoMode(QLineEdit::Password);
    m_password->setStyleSheet(
        "QLineEdit { background: rgba(255,255,255,0.08); color: white; "
        "border: 1px solid rgba(255,255,255,0.15); border-radius: 6px; "
        "padding: 10px; font-size: 13px; }");

    m_remember = new QCheckBox("Запомнить меня", this);
    m_remember->setStyleSheet("color: #AAAAAA;");

    m_loginBtn = new QPushButton("Войти", this);
    m_loginBtn->setStyleSheet(
        "QPushButton { background: #7C4DFF; color: white; border: none; "
        "border-radius: 6px; padding: 10px; font-size: 14px; }"
        "QPushButton:hover { background: #9C6DFF; }");
    connect(m_loginBtn, &QPushButton::clicked, this, [this]() {
        if (m_username->text().isEmpty() || m_password->text().isEmpty()) {
            QMessageBox::warning(this, "Ошибка", "Заполните все поля");
            return;
        }
        accept();
    });

    auto *cancelBtn = new QPushButton("Отмена", this);
    cancelBtn->setStyleSheet(
        "QPushButton { background: #555; color: white; border: none; "
        "border-radius: 6px; padding: 10px; font-size: 14px; }"
        "QPushButton:hover { background: #666; }");
    connect(cancelBtn, &QPushButton::clicked, this, &QDialog::reject);

    layout->addWidget(m_username);
    layout->addWidget(m_password);
    layout->addWidget(m_remember);
    layout->addWidget(m_loginBtn);
    layout->addWidget(cancelBtn);
}

QString LoginDialog::username() const { return m_username->text(); }
QString LoginDialog::password() const { return m_password->text(); }
bool LoginDialog::rememberMe() const { return m_remember->isChecked(); }
