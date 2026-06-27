#ifndef MODMANAGER_H
#define MODMANAGER_H

#include <QObject>
#include <QString>
#include <QList>
#include "src/models/Mod.h"
#include <functional>

class ApiClient;
class ModrinthAPI;
class CurseForgeAPI;

class ModManager : public QObject
{
    Q_OBJECT
public:
    explicit ModManager(ApiClient *client, QObject *parent = nullptr);

    void searchModrinth(const QString &query, int limit,
                        std::function<void(bool, const QList<Mod>&)> cb);
    void searchCurseforge(const QString &query, int limit,
                          std::function<void(bool, const QList<Mod>&)> cb);
    void downloadMod(const Mod &mod, const QString &mcDir,
                     std::function<void(bool)> cb);
    QList<Mod> getInstalledMods(const QString &modsDir);
    bool removeMod(const QString &modPath);
    void openModsFolder(const QString &modsDir);

signals:
    void modInstalled(const QString &name);
    void modRemoved(const QString &path);

private:
    ApiClient     *m_client;
    ModrinthAPI   *m_modrinth;
    CurseForgeAPI *m_curseforge;
};

#endif // MODMANAGER_H
