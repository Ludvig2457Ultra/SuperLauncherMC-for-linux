#ifndef SKINSMANAGER_H
#define SKINSMANAGER_H

#include <QObject>
#include <QString>
#include <QList>
#include <QJsonArray>
#include <functional>
#include "src/models/Skin.h"

class ApiClient;

class SkinsManager : public QObject
{
    Q_OBJECT
public:
    explicit SkinsManager(ApiClient *client, QObject *parent = nullptr);

    void fetchSkins(std::function<void(bool, const QList<Skin>&)> cb);
    void fetchSkinPreview(const QString &skinId, const QString &size,
                          std::function<void(bool, const QByteArray&)> cb);
    void applySkin(const QString &skinId, const QString &username);
    void uploadSkin(const QString &filePath, const QString &username,
                    std::function<void(bool, const QString &error)> cb);
    QList<Skin> getLocalSkins(const QString &userDir);
    bool removeSkin(const QString &skinPath);

signals:
    void skinApplied(const QString &skinId);
    void skinUploaded(const QString &skinId);

private:
    ApiClient *m_client;
};

#endif // SKINSMANAGER_H
