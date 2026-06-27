#ifndef BUILDSMANAGER_H
#define BUILDSMANAGER_H

#include <QObject>
#include <QString>
#include <functional>
#include "src/models/Modpack.h"

class ApiClient;
class ModrinthAPI;
class CurseForgeAPI;

class BuildsManager : public QObject
{
    Q_OBJECT
public:
    using ProgressFn = std::function<void(int percent)>;

    explicit BuildsManager(ApiClient *client, QObject *parent = nullptr);

    void searchModrinth(const QString &query, int limit,
                        std::function<void(bool, const QList<Modpack>&)> cb);
    void searchCurseforge(const QString &query, int limit,
                          std::function<void(bool, const QList<Modpack>&)> cb);
    void installPack(const ModpackVersion &version, const QString &source,
                     const QString &mcDir, ProgressFn prog,
                     std::function<void(bool, const QString &name, const QString &error)> cb);
    void importMrpack(const QString &mrpackPath, const QString &mcDir,
                      ProgressFn prog,
                      std::function<void(bool, const QString &name, const QString &error)> cb);

    QList<InstalledPack> getInstalledPacks(const QString &installBase);

signals:
    void installFinished(bool ok, const QString &name);

private:
    void backupMods(const QString &mcDir);
    bool restoreMods(const QString &mcDir);
    void deduplicateMods(const QString &mcDir);

    ApiClient     *m_client;
    ModrinthAPI   *m_modrinth;
    CurseForgeAPI *m_curseforge;
};

#endif // BUILDSMANAGER_H
