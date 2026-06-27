#include "ModsPage.h"
#include "src/backend/ModManager.h"
#include <QHBoxLayout>
#include <QSplitter>
#include <QLabel>

ModsPage::ModsPage(ModManager *modManager, QWidget *parent)
    : QWidget(parent), m_modManager(modManager)
{
    setupUi();
}

void ModsPage::setupUi()
{
    auto *mainLayout = new QVBoxLayout(this);
    mainLayout->setContentsMargins(24, 24, 24, 24);

    auto *title = new QLabel("Моды", this);
    title->setStyleSheet("color: white; font-size: 22px; font-weight: bold;");
    mainLayout->addWidget(title);

    // Search bar
    auto *searchRow = new QHBoxLayout();
    m_sourceCombo = new QComboBox(this);
    m_sourceCombo->addItems({"Modrinth", "CurseForge"});
    m_sourceCombo->setStyleSheet(
        "QComboBox { background: rgba(255,255,255,0.08); color: white; "
        "border: 1px solid rgba(255,255,255,0.15); border-radius: 6px; "
        "padding: 6px; }"
        "QComboBox::drop-down { border: none; }"
        "QComboBox QAbstractItemView { background: #222; color: white; }");

    m_searchInput = new QLineEdit(this);
    m_searchInput->setPlaceholderText("Поиск модов...");
    m_searchInput->setStyleSheet(
        "QLineEdit { background: rgba(255,255,255,0.08); color: white; "
        "border: 1px solid rgba(255,255,255,0.15); border-radius: 6px; "
        "padding: 8px; }");

    m_searchBtn = new QPushButton("Найти", this);
    m_searchBtn->setStyleSheet(
        "QPushButton { background: #7C4DFF; color: white; border: none; "
        "border-radius: 6px; padding: 8px 20px; }"
        "QPushButton:hover { background: #9C6DFF; }");

    connect(m_searchBtn, &QPushButton::clicked, this, [this]() {
        QString query = m_searchInput->text();
        if (query.isEmpty()) return;
        if (m_sourceCombo->currentIndex() == 0)
            m_modManager->searchModrinth(query, 20,
                [this](bool ok, const QList<Mod> &mods) { onSearchResult(ok, mods); });
        else
            m_modManager->searchCurseforge(query, 20,
                [this](bool ok, const QList<Mod> &mods) { onSearchResult(ok, mods); });
    });
    connect(m_searchInput, &QLineEdit::returnPressed, m_searchBtn, &QPushButton::click);

    searchRow->addWidget(m_sourceCombo);
    searchRow->addWidget(m_searchInput, 1);
    searchRow->addWidget(m_searchBtn);
    mainLayout->addLayout(searchRow);

    // Split results / installed
    auto *splitter = new QSplitter(Qt::Horizontal, this);

    // Search results
    auto *resultsWidget = new QWidget(this);
    auto *resLayout = new QVBoxLayout(resultsWidget);
    auto *resLabel = new QLabel("Результаты поиска", this);
    resLabel->setStyleSheet("color: #AAAAAA; font-size: 13px;");
    m_modList = new QListWidget(this);
    m_modList->setStyleSheet(
        "QListWidget { background: rgba(255,255,255,0.03); border: 1px solid "
        "rgba(255,255,255,0.08); border-radius: 8px; color: white; }"
        "QListWidget::item { padding: 8px; }"
        "QListWidget::item:hover { background: rgba(255,255,255,0.05); }");
    resLayout->addWidget(resLabel);
    resLayout->addWidget(m_modList);
    splitter->addWidget(resultsWidget);

    // Installed mods
    auto *instWidget = new QWidget(this);
    auto *instLayout = new QVBoxLayout(instWidget);
    auto *instLabel = new QLabel("Установленные моды", this);
    instLabel->setStyleSheet("color: #AAAAAA; font-size: 13px;");
    m_installedList = new QListWidget(this);
    m_installedList->setStyleSheet(
        "QListWidget { background: rgba(255,255,255,0.03); border: 1px solid "
        "rgba(255,255,255,0.08); border-radius: 8px; color: white; }"
        "QListWidget::item { padding: 8px; }");
    instLayout->addWidget(instLabel);
    instLayout->addWidget(m_installedList);
    splitter->addWidget(instWidget);

    splitter->setStretchFactor(0, 1);
    splitter->setStretchFactor(1, 1);
    mainLayout->addWidget(splitter, 1);
}

void ModsPage::onSearchResult(bool ok, const QList<Mod> &mods)
{
    m_modList->clear();
    if (!ok) return;
    m_searchResults = mods;
    for (const auto &mod : mods) {
        auto *item = new QListWidgetItem(mod.name + " v" + mod.version + " [" + mod.source + "]");
        item->setData(Qt::UserRole, mod.slug);
        m_modList->addItem(item);
    }
}

void ModsPage::onLocalModsLoaded(const QList<Mod> &mods)
{
    m_installedList->clear();
    for (const auto &mod : mods)
        m_installedList->addItem(mod.name + " v" + mod.version);
}

void ModsPage::refreshLocalMods(const QString &modsDir)
{
    auto mods = m_modManager->getInstalledMods(modsDir);
    onLocalModsLoaded(mods);
}
