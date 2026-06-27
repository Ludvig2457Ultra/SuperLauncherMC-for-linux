#include "ModrinthAPI.h"
#include "ApiClient.h"
#include "src/core/Constants.h"
#include <QUrlQuery>
#include <QJsonDocument>

ModrinthAPI::ModrinthAPI(ApiClient *client, QObject *parent)
    : QObject(parent), m_client(client)
{
}

void ModrinthAPI::searchMods(const QString &query, int limit, ModCallback cb)
{
    QUrlQuery params;
    params.addQueryItem("limit", QString::number(limit));
    params.addQueryItem("index", "relevance");
    if (!query.isEmpty())
        params.addQueryItem("query", query);

    QString url = MODRINTH_API_URL + "/search?" + params.toString();
    m_client->get(url, [cb](bool ok, const QJsonDocument &doc) {
        if (!ok) { cb(false, {}); return; }
        QList<Mod> mods;
        for (const auto &hit : doc.object()["hits"].toArray()) {
            QJsonObject h = hit.toObject();
            if (h["project_type"].toString() != "mod") continue;
            Mod m;
            m.id          = h["project_id"].toString();
            m.slug        = h["slug"].toString();
            m.title       = h["title"].toString();
            m.description = h["description"].toString();
            m.iconUrl     = h["icon_url"].toString();
            m.author      = h["author"].toString();
            m.downloads   = h["downloads"].toInt();
            m.source      = "modrinth";
            mods.append(m);
        }
        cb(true, mods);
    });
}

void ModrinthAPI::searchModpacks(const QString &query, int limit, ModpackCallback cb)
{
    QUrlQuery params;
    params.addQueryItem("limit", QString::number(limit));
    params.addQueryItem("index", "downloads");
    params.addQueryItem("facets", R"([["project_type:modpack"]])");
    if (!query.isEmpty())
        params.addQueryItem("query", query);

    QString url = MODRINTH_API_URL + "/search?" + params.toString();
    m_client->get(url, [cb](bool ok, const QJsonDocument &doc) {
        if (!ok) { cb(false, {}); return; }
        QList<Modpack> packs;
        for (const auto &hit : doc.object()["hits"].toArray()) {
            QJsonObject h = hit.toObject();
            Modpack p;
            p.id          = h["project_id"].toString();
            p.slug        = h["slug"].toString();
            p.name        = h["title"].toString();
            p.description = h["description"].toString();
            p.iconUrl     = h["icon_url"].toString();
            p.author      = h["author"].toString();
            p.downloads   = h["downloads"].toInt();
            p.source      = "modrinth";
            packs.append(p);
        }
        cb(true, packs);
    });
}

void ModrinthAPI::getVersions(const QString &projectId, VersionCallback cb)
{
    QString url = MODRINTH_API_URL + "/project/" + projectId + "/version";
    m_client->get(url, [cb](bool ok, const QJsonDocument &doc) {
        if (!ok) { cb(false, {}); return; }
        QList<ModpackVersion> versions;
        for (const auto &v : doc.array()) {
            QJsonObject vo = v.toObject();
            ModpackVersion mv;
            mv.versionNumber = vo["version_number"].toString();
            mv.id            = vo["id"].toString();
            for (const auto &gv : vo["game_versions"].toArray())
                mv.gameVersions.append(gv.toString());
            for (const auto &l : vo["loaders"].toArray())
                mv.loaders.append(l.toString());
            for (const auto &f : vo["files"].toArray()) {
                mv.files.append(f.toObject()["url"].toString());
            }
            versions.append(mv);
        }
        cb(true, versions);
    });
}
