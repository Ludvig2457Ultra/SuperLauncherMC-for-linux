#ifndef ACCOUNTPAGE_H
#define ACCOUNTPAGE_H

#include <QWidget>
#include <QLineEdit>
#include <QPushButton>
#include <QLabel>
#include <QVBoxLayout>
#include <QCheckBox>
#include <QStackedWidget>

class AccountPage : public QWidget
{
    Q_OBJECT
public:
    explicit AccountPage(QWidget *parent = nullptr);

    void setLoggedIn(bool loggedIn, const QString &username = {},
                     const QString &tier = {});
    void setUserInfo(const QString &username, const QString &email,
                     const QString &license, int xp, int level);

signals:
    void loginRequested(const QString &username, const QString &password);
    void registerRequested(const QString &username, const QString &email,
                           const QString &password);
    void logoutRequested();
    void activateLicense(const QString &key);

private:
    void setupUi();
    void showLoginForm();
    void showProfile();

    // Login form
    QWidget    *m_loginForm    = nullptr;
    QLineEdit  *m_loginUsername = nullptr;
    QLineEdit  *m_loginPassword = nullptr;
    QLineEdit  *m_regUsername   = nullptr;
    QLineEdit  *m_regEmail      = nullptr;
    QLineEdit  *m_regPassword   = nullptr;
    QCheckBox  *m_showPassword  = nullptr;

    // Profile
    QWidget    *m_profileWidget = nullptr;
    QLabel     *m_usernameLabel = nullptr;
    QLabel     *m_emailLabel    = nullptr;
    QLabel     *m_licenseLabel  = nullptr;
    QLabel     *m_xpLabel       = nullptr;
    QLabel     *m_levelLabel    = nullptr;
    QLineEdit  *m_licenseKey    = nullptr;

    QStackedWidget *m_stack = nullptr;
};

#endif // ACCOUNTPAGE_H
