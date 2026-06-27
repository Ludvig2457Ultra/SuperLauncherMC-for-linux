#include "UpdateChecker.h"
#include "src/network/ApiClient.h"
#include "src/core/Constants.h"
#include <QJsonArray>
#include <QJsonDocument>
#include <QJsonObject>

// Simple semver comparison
static bool isNewerVersion(const QString &current, const QString &latest)
{
    auto parts = [](const QString &v) {
        return v.split('.').toVector();
    };
    auto a = parts(current);
    auto b = parts(latest);
    int n = qMax(a.size(), b.size());
    for (int i = 0; i < n; ++i) {
        int va = i < a.size() ? a[i].toInt() : 0;
        int vb = i < b.size() ? b[i].toInt() : 0;
        if (vb > va) return true;
        if (vb < va) return false;
    }
    return false;
}

UpdateChecker::UpdateChecker(ApiClient *client, QObject *parent)
    : QObject(parent), m_client(client)
{
}

void UpdateChecker::checkForUpdates(
    const QString &currentVersion,
    std::function<void(bool, const QString &, const QString &, const QString &)> cb)
{
    m_client->get(LAUNCHER_UPDATE_URL,
        [currentVersion, cb](bool ok, const QJsonDocument &doc) {
            if (!ok || !doc.isObject()) {
                cb(false, {}, {}, {});
                return;
            }
            QJsonObject obj = doc.object();
            QString latest = obj["tag_name"].toString().remove('v');
            if (isNewerVersion(currentVersion, latest)) {
                QString url = obj["html_url"].toString();
                QString body = obj["body"].toString();
                cb(true, latest, url, body);
                return;
            }
            cb(false, {}, {}, {});
        }
    );
}

void UpdateChecker::checkMinecraftUpdates(
    std::function<void(bool, const QStringList &)> cb)
{
    m_client->get("https://piston-meta.mojang.com/mc/game/version_manifest_v2.json",
        [cb](bool ok, const QJsonDocument &doc) {
            if (!ok || !doc.isObject()) {
                cb(false, {});
                return;
            }
            QJsonArray versions = doc.object()["versions"].toArray();
            QStringList latest;
            int count = 0;
            for (const auto &v : versions) {
                if (v.toObject()["type"].toString() == "release") {
                    latest.prepend(v.toObject()["id"].toString());
                    if (++count >= 10) break;
                }
            }
            cb(true, latest);
        }
    );
}
