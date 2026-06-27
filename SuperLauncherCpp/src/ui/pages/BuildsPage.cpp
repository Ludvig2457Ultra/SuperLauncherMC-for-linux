#include "BuildsPage.h"
#include "src/backend/BuildsManager.h"
#include <QHBoxLayout>
#include <QSplitter>
#include <QFileDialog>
#include <QLabel>

BuildsPage::BuildsPage(BuildsManager *builds, QWidget *parent)
    : QWidget(parent), m_builds(builds)
{
    setupUi();
}

void BuildsPage::setupUi()
{
    auto *mainLayout = new QVBoxLayout(this);
    mainLayout->setContentsMargins(24, 24, 24, 24);

    auto *title = new QLabel("Сборки", this);
    title->setStyleSheet("color: white; font-size: 22px; font-weight: bold;");
    mainLayout->addWidget(title);

    // Search
    auto *searchRow = new QHBoxLayout();
    m_sourceCombo = new QComboBox(this);
    m_sourceCombo->addItems({"Modrinth", "CurseForge"});
    m_sourceCombo->setStyleSheet(
        "QComboBox { background: rgba(255,255,255,0.08); color: white; "
        "border: 1px solid rgba(255,255,255,0.15); border-radius: 6px; "
        "padding: 6px; }");

    m_searchInput = new QLineEdit(this);
    m_searchInput->setPlaceholderText("Поиск сборок...");
    m_searchInput->setStyleSheet(
        "QLineEdit { background: rgba(255,255,255,0.08); color: white; "
        "border: 1px solid rgba(255,255,255,0.15); border-radius: 6px; "
        "padding: 8px; }");

    m_searchBtn = new QPushButton("Найти", this);
    m_searchBtn->setStyleSheet(
        "QPushButton { background: #7C4DFF; color: white; border: none; "
        "border-radius: 6px; padding: 8px 20px; }"
        "QPushButton:hover { background: #9C6DFF; }");

    auto *importBtn = new QPushButton("Импорт .mrpack", this);
    importBtn->setStyleSheet(
        "QPushButton { background: #448AFF; color: white; border: none; "
        "border-radius: 6px; padding: 8px 20px; }"
        "QPushButton:hover { background: #64AAFF; }");
    connect(importBtn, &QPushButton::clicked, this, [this]() {
        QString path = QFileDialog::getOpenFileName(this, "Выберите .mrpack",
                                                     {}, "*.mrpack");
        if (!path.isEmpty())
            emit importRequested(path);
    });

    connect(m_searchBtn, &QPushButton::clicked, this, [this]() {
        // similar to ModsPage search
    });

    searchRow->addWidget(m_sourceCombo);
    searchRow->addWidget(m_searchInput, 1);
    searchRow->addWidget(m_searchBtn);
    searchRow->addWidget(importBtn);
    mainLayout->addLayout(searchRow);

    // Progress
    m_progressBar = new QProgressBar(this);
    m_progressBar->setRange(0, 100);
    m_progressBar->setValue(0);
    m_progressBar->setStyleSheet(
        "QProgressBar { background: rgba(255,255,255,0.05); border: none; "
        "border-radius: 4px; height: 8px; text-align: center; color: white; }"
        "QProgressBar::chunk { background: qlineargradient(x1:0,y1:0,x2:1,y2:0, "
        "stop:0 #7C4DFF, stop:1 #448AFF); border-radius: 4px; }");
    m_progressBar->hide();
    mainLayout->addWidget(m_progressBar);

    // Split results / installed
    auto *splitter = new QSplitter(Qt::Horizontal, this);

    auto *resultsW = new QWidget(this);
    auto *resL = new QVBoxLayout(resultsW);
    auto *rl = new QLabel("Результаты", this);
    rl->setStyleSheet("color: #AAAAAA; font-size: 13px;");
    m_resultsList = new QListWidget(this);
    m_resultsList->setStyleSheet(
        "QListWidget { background: rgba(255,255,255,0.03); border: 1px solid "
        "rgba(255,255,255,0.08); border-radius: 8px; color: white; }");
    resL->addWidget(rl);
    resL->addWidget(m_resultsList);
    splitter->addWidget(resultsW);

    auto *instW = new QWidget(this);
    auto *instL = new QVBoxLayout(instW);
    auto *il = new QLabel("Установленные", this);
    il->setStyleSheet("color: #AAAAAA; font-size: 13px;");
    m_installedList = new QListWidget(this);
    m_installedList->setStyleSheet(
        "QListWidget { background: rgba(255,255,255,0.03); border: 1px solid "
        "rgba(255,255,255,0.08); border-radius: 8px; color: white; }");
    instL->addWidget(il);
    instL->addWidget(m_installedList);
    splitter->addWidget(instW);

    mainLayout->addWidget(splitter, 1);
}

void BuildsPage::refreshInstalled(const QString &installBase)
{
    m_installedList->clear();
    auto packs = m_builds->getInstalledPacks(installBase);
    for (const auto &p : packs)
        m_installedList->addItem(p.name + " [" + p.loader + " " + p.mcVersion + "]");
}
