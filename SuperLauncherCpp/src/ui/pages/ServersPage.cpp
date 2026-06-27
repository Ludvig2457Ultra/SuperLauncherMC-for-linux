#include "ServersPage.h"
#include "src/backend/ServerManager.h"
#include <QHBoxLayout>

ServersPage::ServersPage(ServerManager *mgr, QWidget *parent)
    : QWidget(parent), m_mgr(mgr)
{
    setupUi();
}

void ServersPage::setupUi()
{
    auto *mainLayout = new QVBoxLayout(this);
    mainLayout->setContentsMargins(24, 24, 24, 24);

    auto *header = new QHBoxLayout();
    auto *title = new QLabel("Серверы", this);
    title->setStyleSheet("color: white; font-size: 22px; font-weight: bold;");

    auto *createBtn = new QPushButton("+ Создать сервер", this);
    createBtn->setStyleSheet(
        "QPushButton { background: #4CAF50; color: white; border: none; "
        "border-radius: 6px; padding: 8px 20px; font-size: 13px; }"
        "QPushButton:hover { background: #45a049; }");
    connect(createBtn, &QPushButton::clicked, this, [this]() {
        // Will open dialog
    });

    header->addWidget(title);
    header->addStretch();
    header->addWidget(createBtn);
    mainLayout->addLayout(header);

    // Scrollable cards
    m_scrollArea = new QScrollArea(this);
    m_scrollArea->setWidgetResizable(true);
    m_scrollArea->setStyleSheet("QScrollArea { border: none; background: transparent; }");

    auto *scrollContent = new QWidget(m_scrollArea);
    m_cardsLayout = new QVBoxLayout(scrollContent);
    m_cardsLayout->setSpacing(12);
    m_cardsLayout->addStretch();
    m_scrollArea->setWidget(scrollContent);
    mainLayout->addWidget(m_scrollArea, 1);
}

void ServersPage::refreshServers(const QString &serversBase)
{
    m_serversBase = serversBase;
    // Clear existing cards (except stretch)
    QLayoutItem *item;
    while ((item = m_cardsLayout->takeAt(0))) {
        if (item->widget())
            item->widget()->deleteLater();
        delete item;
    }

    auto servers = m_mgr->getServers(serversBase);
    for (const auto &s : servers)
        addServerCard(s);
    m_cardsLayout->addStretch();
}

void ServersPage::addServerCard(const Server &server)
{
    auto *card = new ServerCardWidget(server, this);

    connect(card, &ServerCardWidget::startClicked, this,
            &ServersPage::startServer);
    connect(card, &ServerCardWidget::stopClicked, this,
            &ServersPage::stopServer);
    connect(card, &ServerCardWidget::removeClicked, this,
            [this](const Server &s) { emit removeServer(s.name); });

    m_cardsLayout->insertWidget(m_cardsLayout->count() - 1, card);
}
