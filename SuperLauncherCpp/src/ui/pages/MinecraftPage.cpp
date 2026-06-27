#include "MinecraftPage.h"
#include "src/backend/MinecraftLauncher.h"
#include "src/core/AppConfig.h"
#include "src/core/Constants.h"
#include <QHBoxLayout>
#include <QSplitter>
#include <QJsonDocument>
#include <QJsonArray>
#include <QJsonObject>
#include <QNetworkAccessManager>
#include <QNetworkReply>

MinecraftPage::MinecraftPage(MinecraftLauncher *launcher, AppConfig *config,
                               QWidget *parent)
    : QWidget(parent), m_launcher(launcher), m_config(config)
{
    setupUi();
}

void MinecraftPage::setupUi()
{
    auto *mainLayout = new QVBoxLayout(this);
    mainLayout->setContentsMargins(24, 24, 24, 24);

    auto *title = new QLabel("Minecraft", this);
    title->setStyleSheet("color: white; font-size: 22px; font-weight: bold;");
    mainLayout->addWidget(title);

    // Version selection
    auto *ctrlRow = new QHBoxLayout();

    auto *verLabel = new QLabel("Версия:", this);
    verLabel->setStyleSheet("color: #AAAAAA;");
    m_versionCombo = new QComboBox(this);
    m_versionCombo->setMinimumWidth(200);
    m_versionCombo->setStyleSheet(
        "QComboBox { background: rgba(255,255,255,0.08); color: white; "
        "border: 1px solid rgba(255,255,255,0.15); border-radius: 6px; "
        "padding: 6px; }");

    auto *loaderLabel = new QLabel("Загрузчик:", this);
    loaderLabel->setStyleSheet("color: #AAAAAA;");
    m_loaderCombo = new QComboBox(this);
    m_loaderCombo->addItems({"Vanilla", "Fabric", "Forge", "Quilt"});
    m_loaderCombo->setStyleSheet(
        "QComboBox { background: rgba(255,255,255,0.08); color: white; "
        "border: 1px solid rgba(255,255,255,0.15); border-radius: 6px; "
        "padding: 6px; }");

    ctrlRow->addWidget(verLabel);
    ctrlRow->addWidget(m_versionCombo);
    ctrlRow->addWidget(loaderLabel);
    ctrlRow->addWidget(m_loaderCombo);
    ctrlRow->addStretch();
    mainLayout->addLayout(ctrlRow);

    // Launch / Kill buttons
    auto *btnRow = new QHBoxLayout();
    m_launchBtn = new QPushButton("Запустить", this);
    m_launchBtn->setStyleSheet(
        "QPushButton { background: #4CAF50; color: white; border: none; "
        "border-radius: 6px; padding: 10px 32px; font-size: 14px; }"
        "QPushButton:hover { background: #45a049; }");
    connect(m_launchBtn, &QPushButton::clicked, this, [this]() {
        emit launchRequested(m_versionCombo->currentText(),
                              m_loaderCombo->currentText().toLower(),
                              m_config->getInt("min_ram", 1024),
                              m_config->getInt("max_ram", 4096),
                              m_config->getString("jvm_args", ""));
    });

    m_killBtn = new QPushButton("Остановить", this);
    m_killBtn->setStyleSheet(
        "QPushButton { background: #f44336; color: white; border: none; "
        "border-radius: 6px; padding: 10px 32px; font-size: 14px; }"
        "QPushButton:hover { background: #da190b; }");
    connect(m_killBtn, &QPushButton::clicked, m_launcher, &MinecraftLauncher::kill);
    m_killBtn->hide();

    btnRow->addWidget(m_launchBtn);
    btnRow->addWidget(m_killBtn);
    btnRow->addStretch();
    mainLayout->addLayout(btnRow);

    // Progress
    m_progressBar = new QProgressBar(this);
    m_progressBar->setRange(0, 0);
    m_progressBar->setStyleSheet(
        "QProgressBar { background: rgba(255,255,255,0.05); border: none; "
        "border-radius: 4px; height: 6px; }"
        "QProgressBar::chunk { background: #7C4DFF; border-radius: 4px; }");
    m_progressBar->hide();
    mainLayout->addWidget(m_progressBar);

    // Console output
    auto *logLabel = new QLabel("Консоль:", this);
    logLabel->setStyleSheet("color: #AAAAAA; font-size: 13px;");
    mainLayout->addWidget(logLabel);

    m_logOutput = new QTextEdit(this);
    m_logOutput->setReadOnly(true);
    m_logOutput->setStyleSheet(
        "QTextEdit { background: rgba(0,0,0,0.3); border: 1px solid "
        "rgba(255,255,255,0.08); border-radius: 8px; color: #00FF00; "
        "font-family: 'Consolas', 'Courier New'; font-size: 11px; "
        "padding: 8px; }");
    mainLayout->addWidget(m_logOutput, 1);

    // Connect launcher signals
    connect(m_launcher, &MinecraftLauncher::launchStarted, this, [this]() {
        m_launchBtn->hide();
        m_killBtn->show();
        m_progressBar->show();
        m_logOutput->clear();
    });
    connect(m_launcher, &MinecraftLauncher::launchFinished, this, [this](int) {
        m_launchBtn->show();
        m_killBtn->hide();
        m_progressBar->hide();
    });
    connect(m_launcher, &MinecraftLauncher::outputReceived, this, [this](const QString &line) {
        m_logOutput->append(line);
    });
}

void MinecraftPage::refreshVersions()
{
    auto *nam = new QNetworkAccessManager(this);
    QNetworkReply *reply = nam->get(
        QNetworkRequest(QUrl("https://piston-meta.mojang.com/mc/game/version_manifest_v2.json")));

    connect(reply, &QNetworkReply::finished, this, [this, reply]() {
        if (reply->error() == QNetworkReply::NoError) {
            QJsonDocument doc = QJsonDocument::fromJson(reply->readAll());
            QJsonArray versions = doc.object()["versions"].toArray();
            QStringList releaseVersions;
            for (const auto &v : versions) {
                if (v.toObject()["type"].toString() == "release")
                    releaseVersions.prepend(v.toObject()["id"].toString());
            }
            m_versionCombo->clear();
            m_versionCombo->addItems(releaseVersions);
            if (!releaseVersions.isEmpty())
                m_versionCombo->setCurrentIndex(0);
        }
        reply->deleteLater();
    });
}
