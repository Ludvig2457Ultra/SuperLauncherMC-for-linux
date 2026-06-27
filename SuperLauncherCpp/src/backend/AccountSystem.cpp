#include "AccountSystem.h"
#include "src/core/Constants.h"
#include <QFile>
#include <QJsonDocument>
#include <QJsonObject>
#include <QCryptographicHash>
#include <QRandomGenerator>
#include <QDir>
#include <QDateTime>

AccountSystem::AccountSystem(QObject *parent)
    : QObject(parent)
{
    loadAccounts();
    QFile lf(LICENSES_FILE);
    if (lf.open(QIODevice::ReadOnly)) {
        m_licenses = QJsonDocument::fromJson(lf.readAll()).object();
        lf.close();
    }
}

void AccountSystem::loadAccounts()
{
    QFile f(ACCOUNTS_FILE);
    if (f.open(QIODevice::ReadOnly)) {
        m_accounts = QJsonDocument::fromJson(f.readAll()).array();
        f.close();
    } else {
        m_accounts = QJsonArray();
    }
}

void AccountSystem::saveAccounts()
{
    QFile f(ACCOUNTS_FILE);
    if (f.open(QIODevice::WriteOnly)) {
        f.write(QJsonDocument(m_accounts).toJson(QJsonDocument::Indented));
        f.close();
    }
}

bool AccountSystem::registerUser(const QString &username, const QString &email,
                                  const QString &password)
{
    loadAccounts();
    for (const auto &a : m_accounts) {
        QJsonObject o = a.toObject();
        if (o["username"].toString() == username) return false;
        if (o["email"].toString() == email) return false;
    }

    QString userId = QString::number(QRandomGenerator::global()->generate64(), 16);
    QString salt   = QString::number(QRandomGenerator::global()->generate64(), 16);
    QString pwdHash = QString(QCryptographicHash::hash(
        (password + salt).toUtf8(), QCryptographicHash::Sha256).toHex());

    QJsonObject user;
    user["user_id"]       = userId;
    user["username"]      = username;
    user["email"]         = email;
    user["password_hash"] = pwdHash;
    user["salt"]          = salt;
    user["created_at"]    = QDateTime::currentDateTime().toString(Qt::ISODate);
    user["license_tier"]  = "free";
    user["xp"]            = 0;
    user["level"]         = 1;
    user["skins"]         = QJsonArray({"default"});

    m_accounts.append(user);
    saveAccounts();

    QDir().mkpath("user_data/" + userId + "/skins");
    QDir().mkpath("user_data/" + userId + "/configs");

    User u;
    u.userId      = userId;
    u.username    = username;
    u.email       = email;
    u.passwordHash = pwdHash;
    u.salt        = salt;
    u.createdAt   = user["created_at"].toString();
    u.licenseTier = "free";
    m_currentUser = u;
    emit loginSuccess(u);
    return true;
}

bool AccountSystem::login(const QString &usernameOrEmail, const QString &password)
{
    loadAccounts();
    for (const auto &a : m_accounts) {
        QJsonObject o = a.toObject();
        if (o["username"].toString() == usernameOrEmail ||
            o["email"].toString() == usernameOrEmail) {
            QString salt = o["salt"].toString();
            QString hash = QString(QCryptographicHash::hash(
                (password + salt).toUtf8(), QCryptographicHash::Sha256).toHex());
            if (hash == o["password_hash"].toString()) {
                User u;
                u.userId       = o["user_id"].toString();
                u.username     = o["username"].toString();
                u.email        = o["email"].toString();
                u.licenseTier  = o["license_tier"].toString("free");
                u.xp           = o["xp"].toInt();
                u.level        = o["level"].toInt();
                u.skins        = o["skins"].toVariant().toStringList();
                u.currentSkin  = o["current_skin"].toString();
                m_currentUser  = u;
                emit loginSuccess(u);
                return true;
            }
        }
    }
    return false;
}

void AccountSystem::logout()
{
    m_currentUser.reset();
    emit logoutDone();
}

bool AccountSystem::isPremium() const
{
    return m_currentUser.has_value() &&
           m_currentUser->licenseTier != "free";
}

QString AccountSystem::userFolder() const
{
    if (m_currentUser)
        return "user_data/" + m_currentUser->userId;
    return "user_data/guest";
}

QString AccountSystem::generateLicenseKey(const QString &userId,
                                           const QString &tier, int duration)
{
    qint64 ts = QDateTime::currentSecsSinceEpoch();
    QString base = userId + "_" + tier + "_" + QString::number(duration)
                   + "_" + QString::number(ts)
                   + "_" + QString::number(QRandomGenerator::global()->generate64(), 16);
    QString key = QString(QCryptographicHash::hash(
        base.toUtf8(), QCryptographicHash::Sha256).toHex()).left(24).toUpper();

    QString formatted;
    for (int i = 0; i < key.size(); i += 6)
        formatted += (i ? "-" : "") + key.mid(i, 6);

    QJsonObject lic;
    lic["user_id"]      = userId;
    lic["tier"]         = tier;
    lic["duration"]     = duration;
    lic["created_at"]   = ts;
    lic["expires_at"]   = ts + duration * 86400;
    lic["activated"]    = false;
    m_licenses[formatted] = lic;

    QFile lf(LICENSES_FILE);
    if (lf.open(QIODevice::WriteOnly)) {
        lf.write(QJsonDocument(m_licenses).toJson(QJsonDocument::Indented));
        lf.close();
    }
    return formatted;
}

bool AccountSystem::activateLicense(const QString &key, const QString &userId,
                                     QString &error)
{
    if (!m_licenses.contains(key)) {
        error = "Неверный ключ лицензии";
        return false;
    }
    QJsonObject lic = m_licenses[key].toObject();
    if (lic["activated"].toBool()) {
        error = "Лицензия уже активирована";
        return false;
    }
    if (QDateTime::currentSecsSinceEpoch() > lic["expires_at"].toInteger()) {
        error = "Срок действия лицензии истек";
        return false;
    }
    lic["activated"]     = true;
    lic["activated_by"]  = userId;
    lic["activated_at"]  = QDateTime::currentSecsSinceEpoch();
    m_licenses[key] = lic;

    // Update user
    for (auto &&a : m_accounts) {
        QJsonObject o = a.toObject();
        if (o["user_id"].toString() == userId) {
            o["license_tier"] = lic["tier"].toString();
            o["license_expires"] = lic["expires_at"].toInteger();
            a = o;
            break;
        }
    }
    saveAccounts();
    QFile lf(LICENSES_FILE);
    if (lf.open(QIODevice::WriteOnly)) {
        lf.write(QJsonDocument(m_licenses).toJson(QJsonDocument::Indented));
        lf.close();
    }
    if (m_currentUser)
        m_currentUser->licenseTier = lic["tier"].toString();
    error.clear();
    return true;
}
