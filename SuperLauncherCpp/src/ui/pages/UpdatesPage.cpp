#include "UpdatesPage.h"
#include "src/backend/UpdateChecker.h"

UpdatesPage::UpdatesPage(UpdateChecker *checker, QWidget *parent)
    : QWidget(parent), m_checker(checker)
{
    setupUi();
}

void UpdatesPage::setupUi()
{
    auto *mainLayout = new QVBoxLayout(this);
    mainLayout->setContentsMargins(24, 24, 24, 24);

    auto *title = new QLabel("Обновления", this);
    title->setStyleSheet("color: white; font-size: 22px; font-weight: bold;");
    mainLayout->addWidget(title);

    m_launcherVersion = new QLabel("Версия лаунчера: 1.0.0", this);
    m_launcherVersion->setStyleSheet("color: #AAAAAA; font-size: 14px;");
    mainLayout->addWidget(m_launcherVersion);

    m_checkBtn = new QPushButton("Проверить обновления", this);
    m_checkBtn->setStyleSheet(
        "QPushButton { background: #7C4DFF; color: white; border: none; "
        "border-radius: 6px; padding: 10px 24px; font-size: 14px; }"
        "QPushButton:hover { background: #9C6DFF; }");
    connect(m_checkBtn, &QPushButton::clicked, this, &UpdatesPage::checkNow);

    m_downloadBtn = new QPushButton("Скачать обновление", this);
    m_downloadBtn->setStyleSheet(
        "QPushButton { background: #4CAF50; color: white; border: none; "
        "border-radius: 6px; padding: 10px 24px; font-size: 14px; }"
        "QPushButton:hover { background: #45a049; }");
    m_downloadBtn->hide();
    connect(m_downloadBtn, &QPushButton::clicked, this, [this]() {
        // will connect to download url
    });

    mainLayout->addWidget(m_checkBtn);
    mainLayout->addWidget(m_downloadBtn);

    // Changelog
    auto *clLabel = new QLabel("Что нового:", this);
    clLabel->setStyleSheet("color: #AAAAAA; font-size: 13px; margin-top: 16px;");
    mainLayout->addWidget(clLabel);

    m_changelogViewer = new QTextBrowser(this);
    m_changelogViewer->setStyleSheet(
        "QTextBrowser { background: rgba(255,255,255,0.03); border: 1px solid "
        "rgba(255,255,255,0.08); border-radius: 8px; color: #CCCCCC; "
        "padding: 12px; }");
    mainLayout->addWidget(m_changelogViewer, 1);
}

void UpdatesPage::checkNow()
{
    m_checker->checkForUpdates("1.0.0",
        [this](bool hasUpdate, const QString &ver, const QString &url,
               const QString &changelog) {
            if (hasUpdate) {
                m_launcherVersion->setText(
                    "Доступна новая версия: " + ver);
                m_downloadBtn->show();
                m_changelogViewer->setText(changelog);
            } else {
                m_launcherVersion->setText("У вас актуальная версия");
                m_downloadBtn->hide();
            }
        }
    );
}
