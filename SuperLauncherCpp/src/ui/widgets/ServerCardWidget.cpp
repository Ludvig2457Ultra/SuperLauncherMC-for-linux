#include "ServerCardWidget.h"
#include <QHBoxLayout>
#include <QVBoxLayout>

ServerCardWidget::ServerCardWidget(const Server &server, QWidget *parent)
    : QFrame(parent), m_server(server)
{
    setupUi();
    applyStyle();
}

void ServerCardWidget::setServer(const Server &s)
{
    m_server = s;
    m_nameLabel->setText(s.name);
    m_versionLabel->setText(s.version + " (" + s.type + ")");
}

void ServerCardWidget::setStatusRunning(bool running)
{
    m_server.running = running;
    m_statusLabel->setText(running ? "ONLINE" : "OFFLINE");
    m_statusLabel->setStyleSheet(running
        ? "color: #4CAF50; font-weight: bold;"
        : "color: #888888; font-weight: bold;");
}

void ServerCardWidget::setupUi()
{
    auto *mainLayout = new QVBoxLayout(this);
    mainLayout->setContentsMargins(16, 12, 16, 12);

    // Top row: name + status
    auto *topRow = new QHBoxLayout();
    m_nameLabel = new QLabel(m_server.name, this);
    m_nameLabel->setStyleSheet("color: white; font-size: 14px; font-weight: bold;");
    m_nameLabel->setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Preferred);

    m_statusLabel = new QLabel(m_server.running ? "ONLINE" : "OFFLINE", this);
    setStatusRunning(m_server.running);

    topRow->addWidget(m_nameLabel);
    topRow->addWidget(m_statusLabel);
    mainLayout->addLayout(topRow);

    // Version line
    m_versionLabel = new QLabel(m_server.version + " (" + m_server.type + ")", this);
    m_versionLabel->setStyleSheet("color: #AAAAAA; font-size: 11px;");
    mainLayout->addWidget(m_versionLabel);

    // IP:Port
    auto *ipLabel = new QLabel(m_server.ip + ":" + QString::number(m_server.port), this);
    ipLabel->setStyleSheet("color: #888888; font-size: 10px;");
    mainLayout->addWidget(ipLabel);

    // Buttons
    auto *btnRow = new QHBoxLayout();

    m_startBtn = new QPushButton("Start", this);
    m_startBtn->setStyleSheet(
        "QPushButton { background: #4CAF50; color: white; border: none; "
        "border-radius: 4px; padding: 6px 16px; }"
        "QPushButton:hover { background: #45a049; }");

    m_stopBtn = new QPushButton("Stop", this);
    m_stopBtn->setStyleSheet(
        "QPushButton { background: #f44336; color: white; border: none; "
        "border-radius: 4px; padding: 6px 16px; }"
        "QPushButton:hover { background: #da190b; }");

    m_configBtn = new QPushButton("Config", this);
    m_configBtn->setStyleSheet(
        "QPushButton { background: #2196F3; color: white; border: none; "
        "border-radius: 4px; padding: 6px 16px; }"
        "QPushButton:hover { background: #0b7dda; }");

    m_removeBtn = new QPushButton("X", this);
    m_removeBtn->setFixedSize(28, 28);
    m_removeBtn->setStyleSheet(
        "QPushButton { background: #555; color: #ccc; border: none; "
        "border-radius: 14px; }"
        "QPushButton:hover { background: #f44336; color: white; }");

    btnRow->addWidget(m_startBtn);
    btnRow->addWidget(m_stopBtn);
    btnRow->addWidget(m_configBtn);
    btnRow->addStretch();
    btnRow->addWidget(m_removeBtn);
    mainLayout->addLayout(btnRow);

    // Connections
    connect(m_startBtn, &QPushButton::clicked, this, [this]() {
        emit startClicked(m_server);
    });
    connect(m_stopBtn, &QPushButton::clicked, this, [this]() {
        emit stopClicked(m_server);
    });
    connect(m_configBtn, &QPushButton::clicked, this, [this]() {
        emit configureClicked(m_server);
    });
    connect(m_removeBtn, &QPushButton::clicked, this, [this]() {
        emit removeClicked(m_server);
    });
}

void ServerCardWidget::applyStyle()
{
    setStyleSheet(
        "ServerCardWidget { background: rgba(255,255,255,0.05); "
        "border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); }");
    setFrameShape(QFrame::StyledPanel);
}
