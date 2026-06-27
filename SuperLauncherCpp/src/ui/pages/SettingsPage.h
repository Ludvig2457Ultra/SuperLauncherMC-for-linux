#ifndef SETTINGSPAGE_H
#define SETTINGSPAGE_H

#include <QWidget>
#include <QSpinBox>
#include <QLineEdit>
#include <QCheckBox>
#include <QComboBox>
#include <QPushButton>
#include <QVBoxLayout>
#include <QLabel>

class AppConfig;

class SettingsPage : public QWidget
{
    Q_OBJECT
public:
    explicit SettingsPage(AppConfig *config, QWidget *parent = nullptr);

    void loadSettings();
    void saveSettings();

signals:
    void settingsChanged();

private:
    void setupUi();
    QWidget* createGroup(const QString &title);

    AppConfig   *m_config;

    // Minecraft
    QSpinBox    *m_minMem      = nullptr;
    QSpinBox    *m_maxMem      = nullptr;
    QLineEdit   *m_javaArgs    = nullptr;
    QComboBox   *m_language    = nullptr;
    QLineEdit   *m_mcDir       = nullptr;
    QCheckBox   *m_autoLogin   = nullptr;
    QCheckBox   *m_discordRPC  = nullptr;

    // UI
    QCheckBox   *m_darkMode    = nullptr;
    QCheckBox   *m_holidayTheme = nullptr;
};

#endif // SETTINGSPAGE_H
