#include "MainWindow.h"
#include "src/ui/ModernSidebar.h"
#include "src/ui/pages/HomePage.h"
#include "src/ui/pages/AccountPage.h"
#include "src/ui/pages/ModsPage.h"
#include "src/ui/pages/BuildsPage.h"
#include "src/ui/pages/SkinsPage.h"
#include "src/ui/pages/NewsPage.h"
#include "src/ui/pages/UpdatesPage.h"
#include "src/ui/pages/ServersPage.h"
#include "src/ui/pages/SettingsPage.h"
#include "src/ui/pages/MinecraftPage.h"
#include "src/ui/pages/AIAgentPage.h"
#include "src/ui/widgets/GlassFrame.h"
#include "src/ui/dialogs/CreateServerDialog.h"
#include "src/ui/dialogs/ServerControlDialog.h"
#include "src/core/Constants.h"
#include <QHBoxLayout>
#include <QMessageBox>
#include <QApplication>
#include <QProcess>
#include <QStandardPaths>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
{
    setWindowTitle("SuperLauncher");
    setMinimumSize(1100, 700);
    resize(1280, 800);
    setAttribute(Qt::WA_TranslucentBackground);

    // Core singletons
    m_config = &AppConfig::instance();
    m_translations = &Translations::instance();

    // Network
    m_apiClient = new ApiClient(this);

    // Backend services
    m_accountSys     = new AccountSystem(this);
    m_launcher       = new MinecraftLauncher(m_apiClient, this);
    m_buildsMgr      = new BuildsManager(m_apiClient, this);
    m_skinsMgr       = new SkinsManager(m_apiClient, this);
    m_modMgr         = new ModManager(m_apiClient, this);
    m_serverMgr      = new ServerManager(m_apiClient, this);
    m_updateChecker  = new UpdateChecker(m_apiClient, this);
    m_discordRPC     = new DiscordRPC(this);

    applyTheme();
    applyLanguage();
    setupUi();
    setupConnections();
    initServices();
}

MainWindow::~MainWindow()
{
    m_discordRPC->disconnect();
    m_launcher->kill();
    m_serverMgr->stopServer();
    m_serverMgr->stopPlayitTunnel();
}

void MainWindow::initServices()
{
    // Check for updates
    m_updateChecker->checkForUpdates(APP_VERSION,
        [this](bool hasUpdate, const QString &ver, const QString &url,
               const QString &) {
            if (hasUpdate) {
                m_updatesPage->checkNow();
            }
        }
    );

    // Minecraft versions
    m_minecraftPage->refreshVersions();

    // Discord
    setupDiscord();

    // Auto login
    setupAutoLogin();
}

void MainWindow::setupUi()
{
    auto *glass = new GlassFrame(this);
    glass->setTintColor(QColor(25, 25, 35, 220));
    glass->setBorderRadius(16);
    glass->setBorderColor(QColor(255, 255, 255, 30));

    auto *mainLayout = new QHBoxLayout(glass);
    mainLayout->setContentsMargins(12, 12, 12, 12);
    mainLayout->setSpacing(0);

    setupSidebar();
    m_sidebar->setCollapsed(true);
    mainLayout->addWidget(m_sidebar);

    m_pageStack = new QStackedWidget(glass);
    m_pageStack->setStyleSheet(
        "QStackedWidget { background: rgba(30,30,40,0.85); "
        "border: 1px solid rgba(255,255,255,0.08); "
        "border-radius: 14px; }");
    mainLayout->addWidget(m_pageStack, 1);

    setupPages();
    m_pageStack->setCurrentIndex(0);

    setCentralWidget(glass);
}

void MainWindow::setupSidebar()
{
    m_sidebar = new ModernSidebar(this);
    m_sidebar->setFixedWidth(220);

    QStringList icons = {"⌂", "◎", "▣", "⬇", "♠", "≡", "↻", "⬡", "⚙", "▶", "◆"};
    QStringList labels = {"Главная", "Аккаунт", "Моды", "Сборки", "Скины",
                          "Новости", "Обновления", "Серверы", "Настройки",
                          "Minecraft", "AI Агент"};

    for (int i = 0; i < labels.size(); ++i)
        m_sidebar->addItem(icons[i], labels[i], i);

    connect(m_sidebar, &ModernSidebar::itemClicked,
            this, &MainWindow::onSidebarItemClicked);
}

void MainWindow::setupPages()
{
    m_homePage      = new HomePage(this);
    m_accountPage   = new AccountPage(this);
    m_modsPage      = new ModsPage(m_modMgr, this);
    m_buildsPage    = new BuildsPage(m_buildsMgr, this);
    m_skinsPage     = new SkinsPage(m_skinsMgr, this);
    m_newsPage      = new NewsPage(m_apiClient, this);
    m_updatesPage   = new UpdatesPage(m_updateChecker, this);
    m_serversPage   = new ServersPage(m_serverMgr, this);
    m_settingsPage  = new SettingsPage(m_config, this);
    m_minecraftPage = new MinecraftPage(m_launcher, m_config, this);
    m_aiAgentPage   = new AIAgentPage(m_apiClient, this);

    // Pages must match sidebar order
    m_pageStack->addWidget(m_homePage);      // 0
    m_pageStack->addWidget(m_accountPage);   // 1
    m_pageStack->addWidget(m_modsPage);      // 2
    m_pageStack->addWidget(m_buildsPage);    // 3
    m_pageStack->addWidget(m_skinsPage);     // 4
    m_pageStack->addWidget(m_newsPage);      // 5
    m_pageStack->addWidget(m_updatesPage);   // 6
    m_pageStack->addWidget(m_serversPage);   // 7
    m_pageStack->addWidget(m_settingsPage);  // 8
    m_pageStack->addWidget(m_minecraftPage); // 9
    m_pageStack->addWidget(m_aiAgentPage);   // 10
}

void MainWindow::setupConnections()
{
    // Home page
    connect(m_homePage, &HomePage::playClicked, this, [this]() {
        onSidebarItemClicked(9); // switch to Minecraft page
    });
    connect(m_homePage, &HomePage::openAccount, this, [this]() {
        onSidebarItemClicked(1);
    });
    connect(m_homePage, &HomePage::openNews, this, [this]() {
        onSidebarItemClicked(5);
    });

    // Account
    connect(m_accountPage, &AccountPage::loginRequested, this,
        [this](const QString &username, const QString &password) {
            if (m_accountSys->login(username, password)) {
                auto *u = m_accountSys->currentUser();
                m_accountPage->setLoggedIn(true, u->username, u->licenseTier);
            } else {
                QMessageBox::warning(this, "Ошибка", "Неверный логин или пароль");
            }
        }
    );
    connect(m_accountPage, &AccountPage::registerRequested, this,
        [this](const QString &username, const QString &email,
               const QString &password) {
            if (!m_accountSys->registerUser(username, email, password)) {
                QMessageBox::warning(this, "Ошибка",
                                     "Пользователь с таким именем или email уже существует");
            }
        }
    );
    connect(m_accountPage, &AccountPage::logoutRequested, this, [this]() {
        m_accountSys->logout();
        m_accountPage->setLoggedIn(false);
    });
    connect(m_accountPage, &AccountPage::activateLicense, this,
        [this](const QString &key) {
            auto *u = m_accountSys->currentUser();
            if (!u) return;
            QString error;
            if (m_accountSys->activateLicense(key, u->userId, error)) {
                QMessageBox::information(this, "Успех", "Лицензия активирована!");
            } else {
                QMessageBox::warning(this, "Ошибка", error);
            }
        }
    );

    // Minecraft launch
    connect(m_minecraftPage, &MinecraftPage::launchRequested,
            this, &MainWindow::onLaunchMinecraft);

    // Server
    connect(m_serversPage, &ServersPage::createServer, this,
        [this](const QString &name, const QString &version,
               const QString &type, const QString &mcDir) {
            m_serverMgr->createServer(name, version, type, mcDir,
                [this](bool ok, const QString &error) {
                    if (!ok)
                        QMessageBox::warning(this, "Ошибка", error);
                }
            );
        }
    );
    connect(m_serversPage, &ServersPage::startServer, this,
        [this](const Server &server) {
            ServerControlDialog dlg(server, this);
            connect(&dlg, &ServerControlDialog::startRequested, this, [&]() {
                m_serverMgr->startServer(server.dirPath, dlg.ramMB(), dlg.javaArgs());
            });
            connect(&dlg, &ServerControlDialog::stopRequested, this, [&]() {
                m_serverMgr->stopServer();
            });
            dlg.exec();
        }
    );
    connect(m_serversPage, &ServersPage::removeServer, this,
        [this](const QString &name) {
            m_serverMgr->removeServer(name);
            m_serversPage->refreshServers(
                m_config->getString("mc_dir", "") + "/servers");
        }
    );

    // Settings changes
    connect(m_settingsPage, &SettingsPage::settingsChanged, this, [this]() {
        applyTheme();
        applyLanguage();
        setupDiscord();
    });

    // Playit tunnel
    connect(m_serverMgr, &ServerManager::tunnelReady,
            this, &MainWindow::onPlayitTunnelReady);

    // Discord RPC
    connect(m_launcher, &MinecraftLauncher::launchStarted, this, [this]() {
        m_discordRPC->setInGame("1.20.4");
    });
    connect(m_launcher, &MinecraftLauncher::launchFinished, this, [this](int) {
        m_discordRPC->setIdle();
    });
}

void MainWindow::onSidebarItemClicked(int index)
{
    if (index >= 0 && index < m_pageStack->count())
        m_pageStack->setCurrentIndex(index);
}

void MainWindow::onLaunchMinecraft(const QString &version, const QString &loader,
                                    int minMem, int maxMem, const QString &jvmArgs)
{
    QString mcDir = m_config->getString("mc_dir",
        QStandardPaths::writableLocation(QStandardPaths::AppLocalDataLocation) + "/.minecraft");

    // Install version if needed
    m_launcher->installVersion(mcDir, version, loader,
        [this, mcDir, version, loader, minMem, maxMem, jvmArgs](bool ok) {
            if (!ok) {
                QMessageBox::warning(this, "Ошибка",
                                     "Не удалось установить версию " + version);
                return;
            }

            // Get username
            QString username = "Player";
            if (m_accountSys->currentUser())
                username = m_accountSys->currentUser()->username;

            m_launcher->launch(mcDir, username, version, loader,
                               minMem, maxMem, jvmArgs,
                               [this](const QString &line) {
                                   // Log from launcher
                               });
        }
    );
}

void MainWindow::onPlayitTunnelReady(const QString &url)
{
    QMessageBox::information(this, "Playit.gg Tunnel",
                             "Туннель готов!\nСервер доступен по адресу:\n" + url);
}

void MainWindow::setupDiscord()
{
    if (m_config->getBool("discord_rpc", true)) {
        if (!m_discordRPC->isConnected()) {
            m_discordRPC->connect();
            m_discordRPC->setIdle();
        }
    } else {
        m_discordRPC->disconnect();
    }
}

void MainWindow::setupAutoLogin()
{
    if (m_config->getBool("auto_login", false)) {
        // Last session restore
        QString lastUser = m_config->getString("last_username", "");
        if (!lastUser.isEmpty()) {
            // Attempt auto-login (simplified)
        }
    }
}

void MainWindow::applyTheme()
{
    bool dark = m_config->getBool("dark_mode", true);
    bool holiday = m_config->getBool("holiday_theme", false);

    QString fg = "#cdd6f4";
    QString accent = "#4facfe";
    QString border = "#313244";

    QString style = QString(R"(
        QWidget {
            font-family: 'Segoe UI';
            font-size: 13px;
        }
        QPushButton {
            background-color: %2;
            color: white;
            border-radius: 8px;
            padding: 8px 16px;
            font-weight: bold;
            border: none;
        }
        QPushButton:hover {
            background-color: #6db8ff;
        }
        QPushButton:pressed {
            background-color: #3d8fd4;
        }
        QLineEdit {
            background: rgba(255,255,255,0.08);
            color: white;
            border: 1px solid %3;
            border-radius: 6px;
            padding: 8px;
        }
        QLineEdit:focus {
            border-color: %2;
        }
        QComboBox {
            background: rgba(255,255,255,0.08);
            color: white;
            border: 1px solid %3;
            border-radius: 6px;
            padding: 6px;
        }
        QComboBox::drop-down {
            border: none;
            background: transparent;
        }
        QComboBox QAbstractItemView {
            background: #2a2a3a;
            color: white;
            selection-background-color: %2;
            border: 1px solid %3;
        }
        QListWidget {
            background: rgba(255,255,255,0.03);
            border: 1px solid %3;
            border-radius: 8px;
            color: %1;
            outline: none;
        }
        QListWidget::item {
            padding: 8px;
        }
        QListWidget::item:hover {
            background: rgba(255,255,255,0.05);
        }
        QListWidget::item:selected {
            background: rgba(79,172,254,0.2);
        }
        QScrollBar:vertical {
            background: transparent;
            width: 8px;
        }
        QScrollBar::handle:vertical {
            background: rgba(255,255,255,0.15);
            border-radius: 4px;
            min-height: 30px;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: transparent;
        }
        QProgressBar {
            background: rgba(255,255,255,0.05);
            border: none;
            border-radius: 4px;
            text-align: center;
            color: white;
            height: 8px;
        }
        QProgressBar::chunk {
            background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                stop:0 #7C4DFF, stop:1 #448AFF);
            border-radius: 4px;
        }
        QTextEdit, QTextBrowser {
            background: rgba(0,0,0,0.3);
            border: 1px solid %3;
            border-radius: 8px;
            color: %1;
            padding: 8px;
        }
        QGroupBox {
            color: white;
            font-size: 14px;
            font-weight: bold;
            border: 1px solid %3;
            border-radius: 8px;
            margin-top: 12px;
            padding-top: 16px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 12px;
            padding: 0 4px;
        }
        QCheckBox {
            color: %1;
        }
        QCheckBox::indicator {
            width: 16px;
            height: 16px;
        }
        QSpinBox {
            background: rgba(255,255,255,0.08);
            color: white;
            border: 1px solid %3;
            border-radius: 4px;
            padding: 4px;
        }
    )").arg(fg, accent, border);

    setStyleSheet(style);
}

void MainWindow::applyLanguage()
{
    QString lang = m_config->getString("language", "ru");
    m_translations->load(lang);
}
