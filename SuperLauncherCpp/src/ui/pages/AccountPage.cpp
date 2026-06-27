#include "AccountPage.h"
#include "src/ui/widgets/AnimatedButton.h"
#include "src/ui/widgets/GlassFrame.h"
#include <QStackedWidget>

AccountPage::AccountPage(QWidget *parent)
    : QWidget(parent)
{
    setupUi();
    showLoginForm();
}

void AccountPage::setupUi()
{
    auto *mainLayout = new QVBoxLayout(this);
    mainLayout->setContentsMargins(40, 40, 40, 40);

    auto *title = new QLabel("Аккаунт", this);
    title->setStyleSheet("color: white; font-size: 24px; font-weight: bold;");
    mainLayout->addWidget(title);

    m_stack = new QStackedWidget(this);
    mainLayout->addWidget(m_stack);

    // --- Login Form ---
    m_loginForm = new QWidget(this);
    auto *loginLayout = new QVBoxLayout(m_loginForm);
    loginLayout->setSpacing(12);

    m_loginForm->setStyleSheet("QLineEdit { background: rgba(255,255,255,0.08); "
                                "color: white; border: 1px solid rgba(255,255,255,0.15); "
                                "border-radius: 6px; padding: 10px; font-size: 14px; }"
                                "QLineEdit:focus { border-color: #7C4DFF; }");

    auto *lk = new QLabel("Вход", m_loginForm);
    lk->setStyleSheet("color: #AAAAAA; font-size: 14px;");

    m_loginUsername = new QLineEdit(m_loginForm);
    m_loginUsername->setPlaceholderText("Логин или Email");

    m_loginPassword = new QLineEdit(m_loginForm);
    m_loginPassword->setPlaceholderText("Пароль");
    m_loginPassword->setEchoMode(QLineEdit::Password);

    m_showPassword = new QCheckBox("Показать пароль", m_loginForm);
    m_showPassword->setStyleSheet("color: #888888;");
    connect(m_showPassword, &QCheckBox::toggled, this, [this](bool checked) {
        m_loginPassword->setEchoMode(checked ? QLineEdit::Normal : QLineEdit::Password);
    });

    auto *loginBtn = new AnimatedButton("Войти", m_loginForm);
    loginBtn->setStyleSheet(
        "QPushButton { background: #7C4DFF; color: white; font-size: 14px; "
        "border-radius: 6px; } QPushButton:hover { background: #9C6DFF; }");
    connect(loginBtn, &QPushButton::clicked, this, [this]() {
        emit loginRequested(m_loginUsername->text(), m_loginPassword->text());
    });

    loginLayout->addWidget(lk);
    loginLayout->addWidget(m_loginUsername);
    loginLayout->addWidget(m_loginPassword);
    loginLayout->addWidget(m_showPassword);
    loginLayout->addWidget(loginBtn);
    loginLayout->addStretch();

    // Registration fields
    auto *regTitle = new QLabel("Регистрация", m_loginForm);
    regTitle->setStyleSheet("color: #AAAAAA; font-size: 14px; margin-top: 20px;");

    m_regUsername = new QLineEdit(m_loginForm);
    m_regUsername->setPlaceholderText("Логин");

    m_regEmail = new QLineEdit(m_loginForm);
    m_regEmail->setPlaceholderText("Email");

    m_regPassword = new QLineEdit(m_loginForm);
    m_regPassword->setPlaceholderText("Пароль");
    m_regPassword->setEchoMode(QLineEdit::Password);

    auto *regBtn = new AnimatedButton("Зарегистрироваться", m_loginForm);
    regBtn->setStyleSheet(
        "QPushButton { background: #448AFF; color: white; font-size: 14px; "
        "border-radius: 6px; } QPushButton:hover { background: #64AAFF; }");
    connect(regBtn, &QPushButton::clicked, this, [this]() {
        emit registerRequested(m_regUsername->text(), m_regEmail->text(),
                                m_regPassword->text());
    });

    loginLayout->addWidget(regTitle);
    loginLayout->addWidget(m_regUsername);
    loginLayout->addWidget(m_regEmail);
    loginLayout->addWidget(m_regPassword);
    loginLayout->addWidget(regBtn);
    m_stack->addWidget(m_loginForm);

    // --- Profile ---
    m_profileWidget = new QWidget(this);
    auto *profLayout = new QVBoxLayout(m_profileWidget);
    profLayout->setSpacing(12);

    m_usernameLabel = new QLabel(m_profileWidget);
    m_usernameLabel->setStyleSheet("color: white; font-size: 20px; font-weight: bold;");

    m_emailLabel = new QLabel(m_profileWidget);
    m_emailLabel->setStyleSheet("color: #AAAAAA; font-size: 13px;");

    m_licenseLabel = new QLabel(m_profileWidget);
    m_licenseLabel->setStyleSheet("color: #FFD700; font-size: 13px;");

    m_levelLabel = new QLabel(m_profileWidget);
    m_levelLabel->setStyleSheet("color: #7C4DFF; font-size: 13px;");

    m_xpLabel = new QLabel(m_profileWidget);
    m_xpLabel->setStyleSheet("color: #888888; font-size: 12px;");

    // License activation
    auto *licTitle = new QLabel("Активация лицензии", m_profileWidget);
    licTitle->setStyleSheet("color: #AAAAAA; font-size: 14px; margin-top: 20px;");

    m_licenseKey = new QLineEdit(m_profileWidget);
    m_licenseKey->setPlaceholderText("XXXXXX-XXXXXX-XXXXXX-XXXXXX");
    m_licenseKey->setStyleSheet("background: rgba(255,255,255,0.08); color: white; "
                                 "border: 1px solid rgba(255,255,255,0.15); "
                                 "border-radius: 6px; padding: 10px;");

    auto *activateBtn = new AnimatedButton("Активировать", m_profileWidget);
    activateBtn->setStyleSheet(
        "QPushButton { background: #FFD700; color: #333; font-size: 14px; "
        "border-radius: 6px; } QPushButton:hover { background: #FFE44D; }");
    connect(activateBtn, &QPushButton::clicked, this, [this]() {
        emit activateLicense(m_licenseKey->text());
    });

    auto *logoutBtn = new AnimatedButton("Выйти", m_profileWidget);
    logoutBtn->setStyleSheet(
        "QPushButton { background: #f44336; color: white; font-size: 14px; "
        "border-radius: 6px; } QPushButton:hover { background: #da190b; }");
    connect(logoutBtn, &QPushButton::clicked, this, &AccountPage::logoutRequested);

    profLayout->addWidget(m_usernameLabel);
    profLayout->addWidget(m_emailLabel);
    profLayout->addWidget(m_licenseLabel);
    profLayout->addWidget(m_levelLabel);
    profLayout->addWidget(m_xpLabel);
    profLayout->addWidget(licTitle);
    profLayout->addWidget(m_licenseKey);
    profLayout->addWidget(activateBtn);
    profLayout->addWidget(logoutBtn);
    profLayout->addStretch();
    m_stack->addWidget(m_profileWidget);
}

void AccountPage::showLoginForm()
{
    m_stack->setCurrentWidget(m_loginForm);
}

void AccountPage::showProfile()
{
    m_stack->setCurrentWidget(m_profileWidget);
}

void AccountPage::setLoggedIn(bool loggedIn, const QString &username,
                               const QString &tier)
{
    if (loggedIn) {
        m_usernameLabel->setText(username);
        m_licenseLabel->setText("Лицензия: " + (tier.isEmpty() ? "free" : tier));
        showProfile();
    } else {
        showLoginForm();
    }
}

void AccountPage::setUserInfo(const QString &username, const QString &email,
                               const QString &license, int xp, int level)
{
    m_usernameLabel->setText(username);
    m_emailLabel->setText(email);
    m_licenseLabel->setText("Лицензия: " + license);
    m_xpLabel->setText("Опыт: " + QString::number(xp));
    m_levelLabel->setText("Уровень: " + QString::number(level));
}
