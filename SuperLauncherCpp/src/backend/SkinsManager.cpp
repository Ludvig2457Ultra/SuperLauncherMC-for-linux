#include "SkinsManager.h"
#include "src/network/ApiClient.h"
#include <QDir>
#include <QFile>
#include <QFileInfo>
#include <QRandomGenerator>

SkinsManager::SkinsManager(ApiClient *client, QObject *parent)
    : QObject(parent), m_client(client)
{
}

void SkinsManager::fetchSkins(std::function<void(bool, const QList<Skin>&)> cb)
{
    m_client->get("https://api.example.com/skins",
        [cb](bool ok, const QJsonDocument &doc) {
            QList<Skin> skins;
            if (ok && doc.isArray()) {
                for (const auto &v : doc.array()) {
                    QJsonObject o = v.toObject();
                    Skin s;
                    s.id      = o["id"].toString();
                    s.name    = o["name"].toString();
                    s.type    = o["type"].toString();
                    s.imageUrl = o["image_url"].toString();
                    s.colors  = o["colors"].toVariant().toStringList();
                    skins.append(s);
                }
            }
            cb(ok, skins);
        }
    );
}

void SkinsManager::fetchSkinPreview(const QString &skinId, const QString &size,
                                     std::function<void(bool, const QByteArray&)> cb)
{
    QString url = QString("https://api.example.com/skins/%1/preview?size=%2")
                      .arg(skinId, size);
    m_client->getRaw(url, cb);
}

void SkinsManager::applySkin(const QString &skinId, const QString &username)
{
    QJsonObject body;
    body["skin_id"]  = skinId;
    body["username"] = username;
    m_client->post("https://api.example.com/skins/apply", body,
        [this, skinId](bool, const QJsonDocument &) {
            if (skinId != "default")
                emit skinApplied(skinId);
        }
    );
}

void SkinsManager::uploadSkin(const QString &filePath, const QString &username,
                               std::function<void(bool, const QString &)> cb)
{
    QFile f(filePath);
    if (!f.open(QIODevice::ReadOnly)) {
        cb(false, "Cannot open file");
        return;
    }
    QByteArray data = f.readAll();
    f.close();

    QByteArray boundary = "----FormBoundary" + QByteArray::number(QRandomGenerator::global()->generate());
    QByteArray body;
    body.append("--" + boundary + "\r\n");
    body.append("Content-Disposition: form-data; name=\"username\"\r\n\r\n" + username.toUtf8() + "\r\n");
    body.append("--" + boundary + "\r\n");
    body.append("Content-Disposition: form-data; name=\"skin\"; filename=\"" +
                QFileInfo(filePath).fileName().toUtf8() + "\"\r\n");
    body.append("Content-Type: image/png\r\n\r\n");
    body.append(data);
    body.append("\r\n--" + boundary + "--\r\n");

    m_client->uploadRaw("https://api.example.com/skins/upload", body,
        "multipart/form-data; boundary=" + boundary,
        [this, cb](bool ok, const QJsonDocument &doc) {
            if (ok && doc.isObject())
                emit skinUploaded(doc.object()["skin_id"].toString());
            cb(ok, ok ? "" : "Upload failed");
        }
    );
}

QList<Skin> SkinsManager::getLocalSkins(const QString &userDir)
{
    QList<Skin> skins;
    QDir dir(userDir + "/skins");
    if (!dir.exists()) return skins;
    for (const auto &f : dir.entryList({"*.png", "*.jpg"}, QDir::Files)) {
        Skin s;
        s.id   = f;
        s.name = QFileInfo(f).completeBaseName();
        s.localPath = dir.absoluteFilePath(f);
        skins.append(s);
    }
    return skins;
}

bool SkinsManager::removeSkin(const QString &skinPath)
{
    return QFile::remove(skinPath);
}
