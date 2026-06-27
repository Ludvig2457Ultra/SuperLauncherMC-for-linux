#include "NewsPage.h"
#include "src/network/ApiClient.h"
#include <QHBoxLayout>
#include <QLabel>

NewsPage::NewsPage(ApiClient *client, QWidget *parent)
    : QWidget(parent), m_client(client)
{
    setupUi();
}

void NewsPage::setupUi()
{
    auto *mainLayout = new QVBoxLayout(this);
    mainLayout->setContentsMargins(24, 24, 24, 24);

    auto *title = new QLabel("Новости", this);
    title->setStyleSheet("color: white; font-size: 22px; font-weight: bold;");
    mainLayout->addWidget(title);

    // Controls
    auto *ctrlRow = new QHBoxLayout();
    m_langCombo = new QComboBox(this);
    m_langCombo->addItems({"Русский", "English"});
    m_langCombo->setStyleSheet(
        "QComboBox { background: rgba(255,255,255,0.08); color: white; "
        "border: 1px solid rgba(255,255,255,0.15); border-radius: 6px; "
        "padding: 6px; }");

    m_refreshBtn = new QPushButton("Обновить", this);
    m_refreshBtn->setStyleSheet(
        "QPushButton { background: #7C4DFF; color: white; border: none; "
        "border-radius: 6px; padding: 8px 20px; }"
        "QPushButton:hover { background: #9C6DFF; }");

    connect(m_refreshBtn, &QPushButton::clicked, this, [this]() {
        loadNews(m_langCombo->currentIndex() == 0 ? "ru" : "en");
    });

    ctrlRow->addWidget(m_langCombo);
    ctrlRow->addWidget(m_refreshBtn);
    ctrlRow->addStretch();
    mainLayout->addLayout(ctrlRow);

    // News viewer
    m_newsViewer = new QTextBrowser(this);
    m_newsViewer->setOpenExternalLinks(true);
    m_newsViewer->setStyleSheet(
        "QTextBrowser { background: rgba(255,255,255,0.03); border: 1px solid "
        "rgba(255,255,255,0.08); border-radius: 8px; color: #CCCCCC; "
        "padding: 16px; font-size: 14px; }");
    mainLayout->addWidget(m_newsViewer, 1);
}

void NewsPage::loadNews(const QString &lang)
{
    QString url = "https://raw.githubusercontent.com/anomalyco/SuperLauncher/main/"
                  + lang + "_news.html";
    m_client->getRaw(url, [this](bool ok, const QByteArray &data) {
        if (ok)
            renderNews(QString::fromUtf8(data));
        else
            m_newsViewer->setHtml("<p style='color:#888;'>Не удалось загрузить новости</p>");
    });
}

void NewsPage::renderNews(const QString &html)
{
    m_newsViewer->setHtml(html);
}
