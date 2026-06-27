#include "HomePage.h"
#include "src/ui/widgets/GradientLabel.h"
#include "src/ui/widgets/AnimatedButton.h"

HomePage::HomePage(QWidget *parent)
    : QWidget(parent)
{
    setupUi();
}

void HomePage::setupUi()
{
    auto *layout = new QVBoxLayout(this);
    layout->setContentsMargins(40, 40, 40, 40);
    layout->setSpacing(16);

    // Title
    auto *title = new GradientLabel("SuperLauncher", this);
    title->setGradientColors(QColor(180, 130, 255), QColor(100, 200, 255));
    QFont tf = title->font();
    tf.setPointSize(32);
    tf.setBold(true);
    title->setFont(tf);
    title->setFixedHeight(60);
    layout->addWidget(title);

    // Welcome
    m_welcomeLabel = new QLabel("Добро пожаловать в SuperLauncher!", this);
    m_welcomeLabel->setStyleSheet("color: #CCCCCC; font-size: 16px;");
    layout->addWidget(m_welcomeLabel);

    // Status
    m_statusLabel = new QLabel("Загрузите и играйте в Minecraft с лёгкостью", this);
    m_statusLabel->setStyleSheet("color: #888888; font-size: 13px;");
    m_statusLabel->setWordWrap(true);
    layout->addWidget(m_statusLabel);

    // Play button
    m_playBtn = new AnimatedButton("Играть", this);
    m_playBtn->setFixedSize(200, 50);
    m_playBtn->setStyleSheet(
        "QPushButton { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, "
        "stop:0 #7C4DFF, stop:1 #448AFF); color: white; font-size: 16px; "
        "font-weight: bold; border-radius: 8px; border: none; }"
        "QPushButton:hover { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, "
        "stop:0 #8C5DFF, stop:1 #549AFF); }");
    connect(m_playBtn, &QPushButton::clicked, this, &HomePage::playClicked);
    layout->addWidget(m_playBtn);

    layout->addStretch();

    // Quick links
    auto *linksLayout = new QHBoxLayout();
    auto *accBtn = new QPushButton("Аккаунт", this);
    accBtn->setStyleSheet("QPushButton { color: #7C4DFF; background: transparent; "
                          "border: none; font-size: 12px; }"
                          "QPushButton:hover { color: #9C6DFF; }");
    connect(accBtn, &QPushButton::clicked, this, &HomePage::openAccount);

    auto *newsBtn = new QPushButton("Новости", this);
    newsBtn->setStyleSheet("QPushButton { color: #7C4DFF; background: transparent; "
                           "border: none; font-size: 12px; }"
                           "QPushButton:hover { color: #9C6DFF; }");
    connect(newsBtn, &QPushButton::clicked, this, &HomePage::openNews);

    linksLayout->addWidget(accBtn);
    linksLayout->addWidget(newsBtn);
    linksLayout->addStretch();
    layout->addLayout(linksLayout);
}
