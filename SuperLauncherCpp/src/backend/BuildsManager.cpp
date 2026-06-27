#include "BuildsManager.h"
#include "src/network/ApiClient.h"
#include "src/network/ModrinthAPI.h"
#include "src/network/CurseForgeAPI.h"
#include "src/core/Utils.h"
#include <QDir>
#include <QFile>
#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonArray>
#include <QDateTime>
#include <QTemporaryDir>
#include <QProcess>

BuildsManager::BuildsManager(ApiClient *client, QObject *parent)
    : QObject(parent), m_client(client)
    , m_modrinth(new ModrinthAPI(client, this))
    , m_curseforge(new CurseForgeAPI(client, this))
{
}

void BuildsManager::searchModrinth(const QString &query, int limit,
                                    std::function<void(bool, const QList<Modpack>&)> cb)
{
    m_modrinth->searchModpacks(query, limit, cb);
}

void BuildsManager::searchCurseforge(const QString &query, int limit,
                                      std::function<void(bool, const QList<Modpack>&)> cb)
{
    m_curseforge->searchModpacks(query, limit, cb);
}

QList<InstalledPack> BuildsManager::getInstalledPacks(const QString &installBase)
{
    QList<InstalledPack> result;
    QDir dir(installBase);
    for (const auto &folder : dir.entryList(QDir::Dirs | QDir::NoDotAndDotDot)) {
        QFile cfg(installBase + "/" + folder + "/superlauncher_config.json");
        if (cfg.open(QIODevice::ReadOnly)) {
            QJsonObject obj = QJsonDocument::fromJson(cfg.readAll()).object();
            cfg.close();
            InstalledPack p;
            p.name          = folder;
            p.mcVersion     = obj["mc_versions"].toArray().isEmpty() ? "?" : obj["mc_versions"].toArray().first().toString();
            p.loader        = obj["loaders"].toArray().isEmpty() ? "?" : obj["loaders"].toArray().first().toString();
            p.source        = obj["source"].toString();
            p.versionId     = obj["version_id"].toString();
            result.append(p);
        }
    }
    return result;
}

void BuildsManager::installPack(const ModpackVersion &version, const QString &source,
                                 const QString &mcDir, ProgressFn prog,
                                 std::function<void(bool, const QString &, const QString &)> cb)
{
    // Simplified installation - downloads the first file
    if (version.files.isEmpty()) {
        cb(false, {}, "No files to download");
        return;
    }
    QString url = version.files.first();
    QString filename = url.mid(url.lastIndexOf('/') + 1);

    backupMods(mcDir);
    if (prog) prog(10);

    m_client->downloadFile(url, mcDir + "/" + filename,
        [this, mcDir, filename, prog, cb](bool ok, const QJsonDocument &) {
            if (!ok) { cb(false, {}, "Download failed"); return; }
            if (prog) prog(100);
            cb(true, filename, {});
        },
        [prog](qint64 recv, qint64 total) {
            if (prog && total > 0)
                prog(int(recv * 100 / total));
        }
    );
}

void BuildsManager::importMrpack(const QString &mrpackPath, const QString &mcDir,
                                  ProgressFn prog,
                                  std::function<void(bool, const QString &, const QString &)> cb)
{
    Q_UNUSED(mcDir)
    backupMods(mcDir);
    if (prog) prog(10);

    // mrpack import via external unzip (QZipReader removed in Qt6)
    cb(false, {}, "mrpack import not yet implemented in C++ version");
}

void BuildsManager::backupMods(const QString &mcDir)
{
    QString modsDir = mcDir + "/mods";
    if (!QDir(modsDir).exists()) return;
    QString backup = mcDir + "/mods_backup_" + QString::number(QDateTime::currentSecsSinceEpoch());
    copyDir(modsDir, backup);
}

bool BuildsManager::restoreMods(const QString &mcDir)
{
    QDir dir(mcDir);
    auto backups = dir.entryList({"mods_backup_*"}, QDir::Dirs, QDir::Time);
    if (backups.isEmpty()) return false;
    QString backup = mcDir + "/" + backups.first();
    QString modsDir = mcDir + "/mods";
    if (QDir(modsDir).exists())
        QDir(modsDir).removeRecursively();
    copyDir(backup, modsDir);
    QDir(backup).removeRecursively();
    return true;
}

void BuildsManager::deduplicateMods(const QString &mcDir)
{
    // TODO: implement mod deduplication
    Q_UNUSED(mcDir)
}
