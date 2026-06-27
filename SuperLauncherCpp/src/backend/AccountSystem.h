#ifndef ACCOUNTSYSTEM_H
#define ACCOUNTSYSTEM_H

#include <QObject>
#include <QString>
#include <QJsonArray>
#include <QJsonObject>
#include "src/models/User.h"

class AccountSystem : public QObject
{
    Q_OBJECT
public:
    explicit AccountSystem(QObject *parent = nullptr);

    bool registerUser(const QString &username, const QString &email,
                      const QString &password);
    bool login(const QString &usernameOrEmail, const QString &password);
    void logout();
    bool isPremium() const;
    QString userFolder() const;

    User* currentUser() { return m_currentUser ? &m_currentUser.value() : nullptr; }
    const User* currentUser() const { return m_currentUser ? &m_currentUser.value() : nullptr; }

    // License
    QString generateLicenseKey(const QString &userId, const QString &tier = "standard", int duration = 365);
    bool activateLicense(const QString &key, const QString &userId, QString &error);

    void saveAccounts();
    void loadAccounts();

signals:
    void loginSuccess(const User &user);
    void logoutDone();
    void errorOccurred(const QString &msg);

private:
    QJsonArray  m_accounts;
    QJsonObject m_licenses;
    std::optional<User> m_currentUser;
};

#endif // ACCOUNTSYSTEM_H
