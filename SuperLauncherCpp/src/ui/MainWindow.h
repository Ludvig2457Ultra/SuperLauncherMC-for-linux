#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QStackedWidget>
#include <QTimer>
#include "src/core/AppConfig.h"
#include "src/core/Translations.h"
#include "src/network/ApiClient.h"
#include "src/backend/AccountSystem.h"
#include "src/backend/BuildsManager.h"
#include "src/backend/SkinsManager.h"
#include "src/backend/MinecraftLauncher.h"
#include "src/backend/ModManager.h"
#include "src/backend/ServerManager.h"
#include "src/backend/UpdateChecker.h"
#include "src/backend/DiscordRPC.h"

class ModernSidebar;
class HomePage;
class AccountPage;
class ModsPage;
class BuildsPage;
class SkinsPage;
class NewsPage;
class UpdatesPage;
class ServersPage;
class SettingsPage;
class MinecraftPage;
class AIAgentPage;

class MainWindow : public QMainWindow
{
    Q_OBJECT
public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

    void initServices();

private slots:
    void onSidebarItemClicked(int index);
    void onLaunchMinecraft(const QString &version, const QString &loader,
                           int minMem, int maxMem, const QString &jvmArgs);
    void onPlayitTunnelReady(const QString &url);

private:
    void setupUi();
    void setupSidebar();
    void setupPages();
    void setupConnections();
    void setupDiscord();
    void setupAutoLogin();
    void applyTheme();
    void applyLanguage();

    // UI
    ModernSidebar  *m_sidebar    = nullptr;
    QStackedWidget *m_pageStack  = nullptr;

    // Pages
    HomePage      *m_homePage      = nullptr;
    AccountPage   *m_accountPage   = nullptr;
    ModsPage      *m_modsPage      = nullptr;
    BuildsPage    *m_buildsPage    = nullptr;
    SkinsPage     *m_skinsPage     = nullptr;
    NewsPage      *m_newsPage      = nullptr;
    UpdatesPage   *m_updatesPage   = nullptr;
    ServersPage   *m_serversPage   = nullptr;
    SettingsPage  *m_settingsPage  = nullptr;
    MinecraftPage *m_minecraftPage = nullptr;
    AIAgentPage   *m_aiAgentPage   = nullptr;

    // Services
    AppConfig       *m_config       = nullptr;
    Translations    *m_translations = nullptr;
    ApiClient       *m_apiClient    = nullptr;
    AccountSystem   *m_accountSys   = nullptr;
    BuildsManager   *m_buildsMgr    = nullptr;
    SkinsManager    *m_skinsMgr     = nullptr;
    MinecraftLauncher *m_launcher   = nullptr;
    ModManager      *m_modMgr       = nullptr;
    ServerManager   *m_serverMgr    = nullptr;
    UpdateChecker   *m_updateChecker = nullptr;
    DiscordRPC      *m_discordRPC   = nullptr;
};

#endif // MAINWINDOW_H
