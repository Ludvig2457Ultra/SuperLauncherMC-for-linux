#include "CurseForgeAPI.h"
#include "ApiClient.h"
#include "src/core/Constants.h"
#include "src/core/AppConfig.h"
#include <QUrlQuery>
#include <QJsonDocument>

CurseForgeAPI::CurseForgeAPI(ApiClient *client, QObject *parent)
    : QObject(parent), m_client(client)
{
}

void CurseForgeAPI::searchMods(const QString &query, int limit, ModCallback cb)
{
    QUrlQuery params;
    params.addQueryItem("gameId", "432");
    params.addQueryItem("classId", "6");
    params.addQueryItem("searchFilter", query);
    params.addQueryItem("pageSize", QString::number(limit));
    params.addQueryItem("sortField", "2");
    params.addQueryItem("sortOrder", "desc");

    QString url = CURSEFORGE_API_URL + "/mods/search?" + params.toString();
    QMap<QString, QString> headers;
    headers["x-api-key"] = AppConfig::instance().cfApiKey();

    m_client->get(url, [cb](bool ok, const QJsonDocument &doc) {
        if (!ok) { cb(false, {}); return; }
        QList<Mod> mods;
        for (const auto &mod : doc.object()["data"].toArray()) {
            QJsonObject m = mod.toObject();
            Mod modData;
            modData.id          = QString::number(m["id"].toInt());
            modData.title       = m["name"].toString();
            modData.description = m["summary"].toString();
            modData.iconUrl     = m["logo"].toObject()["url"].toString();
            modData.author      = m["authors"].toArray().isEmpty() ? "Unknown" :
                                   m["authors"].toArray().first().toObject()["name"].toString();
            modData.downloads   = m["downloadCount"].toInt();
            modData.source      = "curseforge";
            mods.append(modData);
        }
        cb(true, mods);
    }, headers);
}

void CurseForgeAPI::searchModpacks(const QString &query, int limit, ModpackCallback cb)
{
    QUrlQuery params;
    params.addQueryItem("gameId", "432");
    params.addQueryItem("classId", "4471");
    params.addQueryItem("searchFilter", query);
    params.addQueryItem("pageSize", QString::number(limit));
    params.addQueryItem("sortField", "2");
    params.addQueryItem("sortOrder", "desc");

    QString url = CURSEFORGE_API_URL + "/mods/search?" + params.toString();
    QMap<QString, QString> headers;
    headers["x-api-key"] = AppConfig::instance().cfApiKey();

    m_client->get(url, [cb](bool ok, const QJsonDocument &doc) {
        if (!ok) { cb(false, {}); return; }
        QList<Modpack> packs;
        for (const auto &mod : doc.object()["data"].toArray()) {
            QJsonObject m = mod.toObject();
            Modpack p;
            p.id          = QString::number(m["id"].toInt());
            p.name        = m["name"].toString();
            p.description = m["summary"].toString();
            p.iconUrl     = m["logo"].toObject()["url"].toString();
            p.author      = m["authors"].toArray().isEmpty() ? "Unknown" :
                             m["authors"].toArray().first().toObject()["name"].toString();
            p.downloads   = m["downloadCount"].toInt();
            p.source      = "curseforge";
            packs.append(p);
        }
        cb(true, packs);
    }, headers);
}

void CurseForgeAPI::getDownloadUrl(int modId, int fileId,
                                   std::function<void(bool, const QString &)> cb)
{
    QString url = CURSEFORGE_API_URL
        + QString("/mods/%1/files/%2/download-url").arg(modId).arg(fileId);
    QMap<QString, QString> headers;
    headers["x-api-key"] = AppConfig::instance().cfApiKey();

    m_client->get(url, [cb](bool ok, const QJsonDocument &doc) {
        if (ok)
            cb(true, doc.object()["data"].toString());
        else
            cb(false, {});
    }, headers);
}
