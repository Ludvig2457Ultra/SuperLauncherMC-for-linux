#include "SettingsPage.h"
#include "src/core/AppConfig.h"
#include <QGroupBox>
#include <QFormLayout>
#include <QFileDialog>
#include <QHBoxLayout>
#include <QStandardPaths>

SettingsPage::SettingsPage(AppConfig *config, QWidget *parent)
    : QWidget(parent), m_config(config)
{
    setupUi();
    loadSettings();
}

void SettingsPage::setupUi()
{
    auto *mainLayout = new QVBoxLayout(this);
    mainLayout->setContentsMargins(24, 24, 24, 24);

    auto *title = new QLabel("Настройки", this);
    title->setStyleSheet("color: white; font-size: 22px; font-weight: bold;");
    mainLayout->addWidget(title);

    auto *scrollContent = new QWidget(this);
    auto *scrollLayout = new QVBoxLayout(scrollContent);
    scrollLayout->setSpacing(8);

    // --- Minecraft ---
    auto *mcGroup = createGroup("Minecraft");
    auto *mcForm = new QFormLayout(mcGroup);
    mcForm->setSpacing(10);
    mcForm->setLabelAlignment(Qt::AlignRight);

    m_minMem = new QSpinBox(mcGroup);
    m_minMem->setRange(256, 32768);
    m_minMem->setSuffix(" MB");

    m_maxMem = new QSpinBox(mcGroup);
    m_maxMem->setRange(512, 65536);
    m_maxMem->setSuffix(" MB");

    m_javaArgs = new QLineEdit(mcGroup);
    m_javaArgs->setPlaceholderText("-XX:+UseG1GC -XX:+UnlockExperimentalVMOptions");

    m_language = new QComboBox(mcGroup);
    m_language->addItems({"Русский", "English"});

    m_mcDir = new QLineEdit(mcGroup);
    auto *browseBtn = new QPushButton("...", mcGroup);
    browseBtn->setFixedWidth(32);
    connect(browseBtn, &QPushButton::clicked, this, [this]() {
        QString dir = QFileDialog::getExistingDirectory(this, "Выберите папку Minecraft");
        if (!dir.isEmpty()) m_mcDir->setText(dir);
    });
    auto *dirRow = new QHBoxLayout();
    dirRow->addWidget(m_mcDir, 1);
    dirRow->addWidget(browseBtn);

    mcForm->addRow("Min RAM:", m_minMem);
    mcForm->addRow("Max RAM:", m_maxMem);
    mcForm->addRow("JVM Аргументы:", m_javaArgs);
    mcForm->addRow("Язык:", m_language);
    mcForm->addRow("Папка Minecraft:", dirRow);
    scrollLayout->addWidget(mcGroup);

    // --- UI ---
    auto *uiGroup = createGroup("Интерфейс");
    auto *uiForm = new QFormLayout(uiGroup);

    m_darkMode = new QCheckBox("Тёмная тема", uiGroup);
    m_holidayTheme = new QCheckBox("Праздничная тема", uiGroup);
    m_autoLogin = new QCheckBox("Автоматический вход", uiGroup);
    m_discordRPC = new QCheckBox("Discord RPC", uiGroup);

    uiForm->addRow("", m_darkMode);
    uiForm->addRow("", m_holidayTheme);
    uiForm->addRow("", m_autoLogin);
    uiForm->addRow("", m_discordRPC);
    scrollLayout->addWidget(uiGroup);

    // --- Save ---
    auto *saveBtn = new QPushButton("Сохранить настройки", this);
    saveBtn->setStyleSheet(
        "QPushButton { background: #7C4DFF; color: white; border: none; "
        "border-radius: 6px; padding: 10px 24px; font-size: 14px; }"
        "QPushButton:hover { background: #9C6DFF; }");
    connect(saveBtn, &QPushButton::clicked, this, [this]() {
        saveSettings();
        emit settingsChanged();
    });
    scrollLayout->addWidget(saveBtn);
    scrollLayout->addStretch();

    mainLayout->addWidget(scrollContent, 1);
}

QWidget* SettingsPage::createGroup(const QString &title)
{
    auto *group = new QWidget(this);
    group->setStyleSheet(
        "QWidget { background: rgba(255,255,255,0.03); border: 1px solid "
        "rgba(255,255,255,0.08); border-radius: 8px; }");
    auto *layout = new QVBoxLayout(group);
    auto *label = new QLabel(title, group);
    label->setStyleSheet("color: white; font-size: 16px; font-weight: bold; "
                          "border: none; padding: 4px 0;");
    layout->addWidget(label);
    return group;
}

void SettingsPage::loadSettings()
{
    m_minMem->setValue(m_config->getInt("min_ram", 1024));
    m_maxMem->setValue(m_config->getInt("max_ram", 4096));
    m_javaArgs->setText(m_config->getString("jvm_args", ""));
    m_language->setCurrentIndex(m_config->getString("language", "ru") == "ru" ? 0 : 1);
    m_mcDir->setText(m_config->getString("mc_dir",
        QStandardPaths::writableLocation(QStandardPaths::AppLocalDataLocation) + "/.minecraft"));
    m_autoLogin->setChecked(m_config->getBool("auto_login", false));
    m_discordRPC->setChecked(m_config->getBool("discord_rpc", true));
    m_darkMode->setChecked(m_config->getBool("dark_mode", true));
    m_holidayTheme->setChecked(m_config->getBool("holiday_theme", false));
}

void SettingsPage::saveSettings()
{
    m_config->setValue("min_ram", m_minMem->value());
    m_config->setValue("max_ram", m_maxMem->value());
    m_config->setValue("jvm_args", m_javaArgs->text());
    m_config->setValue("language", m_language->currentIndex() == 0 ? "ru" : "en");
    m_config->setValue("mc_dir", m_mcDir->text());
    m_config->setValue("auto_login", m_autoLogin->isChecked());
    m_config->setValue("discord_rpc", m_discordRPC->isChecked());
    m_config->setValue("dark_mode", m_darkMode->isChecked());
    m_config->setValue("holiday_theme", m_holidayTheme->isChecked());
    m_config->save();
}
