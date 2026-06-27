#ifndef CURSEFORGEAPI_H
#define CURSEFORGEAPI_H

#include <QObject>
#include <functional>
#include "src/models/Mod.h"
#include "src/models/Modpack.h"

class ApiClient;

class CurseForgeAPI : public QObject
{
    Q_OBJECT
public:
    using ModCallback   = std::function<void(bool ok, const QList<Mod> &mods)>;
    using ModpackCallback = std::function<void(bool ok, const QList<Modpack> &packs)>;

    explicit CurseForgeAPI(ApiClient *client, QObject *parent = nullptr);

    void searchMods(const QString &query, int limit, ModCallback cb);
    void searchModpacks(const QString &query, int limit, ModpackCallback cb);
    void getDownloadUrl(int modId, int fileId,
                        std::function<void(bool ok, const QString &url)> cb);

private:
    ApiClient *m_client;
};

#endif // CURSEFORGEAPI_H
