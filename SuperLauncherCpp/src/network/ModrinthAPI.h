#ifndef MODRINTHAPI_H
#define MODRINTHAPI_H

#include <QObject>
#include <QJsonArray>
#include <QJsonObject>
#include <functional>
#include "src/models/Mod.h"
#include "src/models/Modpack.h"

class ApiClient;

class ModrinthAPI : public QObject
{
    Q_OBJECT
public:
    using ModCallback   = std::function<void(bool ok, const QList<Mod> &mods)>;
    using ModpackCallback = std::function<void(bool ok, const QList<Modpack> &packs)>;
    using VersionCallback = std::function<void(bool ok, const QList<ModpackVersion> &versions)>;

    explicit ModrinthAPI(ApiClient *client, QObject *parent = nullptr);

    void searchMods(const QString &query, int limit, ModCallback cb);
    void searchModpacks(const QString &query, int limit, ModpackCallback cb);
    void getVersions(const QString &projectId, VersionCallback cb);

private:
    ApiClient *m_client;
};

#endif // MODRINTHAPI_H
