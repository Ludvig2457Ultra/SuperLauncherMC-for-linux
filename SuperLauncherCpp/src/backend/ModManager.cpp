#include "ModManager.h"
#include "src/network/ApiClient.h"
#include "src/network/ModrinthAPI.h"
#include "src/network/CurseForgeAPI.h"
#include <QDir>
#include <QFileInfo>
#include <QDesktopServices>
#include <QUrl>

ModManager::ModManager(ApiClient *client, QObject *parent)
    : QObject(parent), m_client(client)
    , m_modrinth(new ModrinthAPI(client, this))
    , m_curseforge(new CurseForgeAPI(client, this))
{
}

void ModManager::searchModrinth(const QString &query, int limit,
                                 std::function<void(bool, const QList<Mod>&)> cb)
{
    m_modrinth->searchMods(query, limit, cb);
}

void ModManager::searchCurseforge(const QString &query, int limit,
                                   std::function<void(bool, const QList<Mod>&)> cb)
{
    m_curseforge->searchMods(query, limit, cb);
}

void ModManager::downloadMod(const Mod &mod, const QString &mcDir,
                              std::function<void(bool)> cb)
{
    if (mod.downloadUrl.isEmpty()) {
        cb(false);
        return;
    }
    QString modsDir = mcDir + "/mods";
    QDir().mkpath(modsDir);
    QString filename = mod.downloadUrl.mid(mod.downloadUrl.lastIndexOf('/') + 1);
    m_client->downloadFile(mod.downloadUrl, modsDir + "/" + filename,
        [this, mod, cb](bool ok, const QJsonDocument &) {
            if (ok) emit modInstalled(mod.name);
            cb(ok);
        }
    );
}

QList<Mod> ModManager::getInstalledMods(const QString &modsDir)
{
    QList<Mod> result;
    QDir dir(modsDir);
    if (!dir.exists()) return result;
    for (const auto &f : dir.entryList({"*.jar", "*.zip"}, QDir::Files)) {
        QFileInfo fi(modsDir + "/" + f);
        Mod mod;
        mod.name = fi.completeBaseName();
        mod.slug = f;
        mod.version = "?";
        mod.downloadUrl = fi.absoluteFilePath();
        mod.source = "local";
        result.append(mod);
    }
    return result;
}

bool ModManager::removeMod(const QString &modPath)
{
    bool ok = QFile::remove(modPath);
    if (ok) emit modRemoved(modPath);
    return ok;
}

void ModManager::openModsFolder(const QString &modsDir)
{
    QDesktopServices::openUrl(QUrl::fromLocalFile(modsDir));
}
