#ifndef UPDATECHECKER_H
#define UPDATECHECKER_H

#include <QObject>
#include <QString>
#include <functional>

class ApiClient;

class UpdateChecker : public QObject
{
    Q_OBJECT
public:
    explicit UpdateChecker(ApiClient *client, QObject *parent = nullptr);

    void checkForUpdates(const QString &currentVersion,
                         std::function<void(bool hasUpdate, const QString &latestVer,
                                            const QString &url, const QString &changelog)> cb);
    void checkMinecraftUpdates(std::function<void(bool, const QStringList &newVersions)> cb);

signals:
    void updateAvailable(const QString &latestVersion, const QString &url);

private:
    ApiClient *m_client;
};

#endif // UPDATECHECKER_H
