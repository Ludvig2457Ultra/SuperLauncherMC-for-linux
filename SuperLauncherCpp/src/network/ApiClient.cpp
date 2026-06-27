#include "ApiClient.h"
#include <QNetworkRequest>
#include <QFile>
#include <QUrl>

ApiClient::ApiClient(QObject *parent)
    : QObject(parent)
    , m_manager(new QNetworkAccessManager(this))
{
}

void ApiClient::setDefaultHeader(const QString &key, const QString &value)
{
    m_defaultHeaders[key] = value;
}

void ApiClient::get(const QString &url, Callback cb,
                    const QMap<QString, QString> &headers)
{
    QUrl theUrl(url);
    QNetworkRequest req(theUrl);
    req.setRawHeader("User-Agent", "SuperLauncher/2.0");
    req.setTransferTimeout(15000);

    for (auto it = m_defaultHeaders.begin(); it != m_defaultHeaders.end(); ++it)
        req.setRawHeader(it.key().toUtf8(), it.value().toUtf8());
    for (auto it = headers.begin(); it != headers.end(); ++it)
        req.setRawHeader(it.key().toUtf8(), it.value().toUtf8());

    auto *reply = m_manager->get(req);
    connect(reply, &QNetworkReply::finished, this, [reply, cb]() {
        if (reply->error() == QNetworkReply::NoError) {
            QJsonDocument doc = QJsonDocument::fromJson(reply->readAll());
            cb(true, doc);
        } else {
            cb(false, QJsonDocument());
        }
        reply->deleteLater();
    });
}

void ApiClient::get(const QString &url, Callback cb,
                    ProgressCallback prog,
                    const QMap<QString, QString> &headers)
{
    QUrl theUrl(url);
    QNetworkRequest req(theUrl);
    req.setRawHeader("User-Agent", "SuperLauncher/2.0");
    for (auto it = m_defaultHeaders.begin(); it != m_defaultHeaders.end(); ++it)
        req.setRawHeader(it.key().toUtf8(), it.value().toUtf8());
    for (auto it = headers.begin(); it != headers.end(); ++it)
        req.setRawHeader(it.key().toUtf8(), it.value().toUtf8());

    auto *reply = m_manager->get(req);
    if (prog)
        connect(reply, &QNetworkReply::downloadProgress, this, prog);
    connect(reply, &QNetworkReply::finished, this, [reply, cb]() {
        if (reply->error() == QNetworkReply::NoError) {
            QJsonDocument doc = QJsonDocument::fromJson(reply->readAll());
            cb(true, doc);
        } else {
            cb(false, QJsonDocument());
        }
        reply->deleteLater();
    });
}

void ApiClient::post(const QString &url, const QJsonObject &body, Callback cb,
                     const QMap<QString, QString> &headers)
{
    QUrl theUrl(url);
    QNetworkRequest req(theUrl);
    req.setRawHeader("User-Agent", "SuperLauncher/2.0");
    req.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");
    for (auto it = m_defaultHeaders.begin(); it != m_defaultHeaders.end(); ++it)
        req.setRawHeader(it.key().toUtf8(), it.value().toUtf8());
    for (auto it = headers.begin(); it != headers.end(); ++it)
        req.setRawHeader(it.key().toUtf8(), it.value().toUtf8());

    QByteArray payload = QJsonDocument(body).toJson(QJsonDocument::Compact);
    auto *reply = m_manager->post(req, payload);
    connect(reply, &QNetworkReply::finished, this, [reply, cb]() {
        if (reply->error() == QNetworkReply::NoError) {
            QJsonDocument doc = QJsonDocument::fromJson(reply->readAll());
            cb(true, doc);
        } else {
            cb(false, QJsonDocument());
        }
        reply->deleteLater();
    });
}

void ApiClient::getRaw(const QString &url,
                        std::function<void(bool, const QByteArray &)> cb,
                        const QMap<QString, QString> &headers)
{
    QUrl theUrl(url);
    QNetworkRequest req(theUrl);
    req.setRawHeader("User-Agent", "SuperLauncher/2.0");
    for (auto it = m_defaultHeaders.begin(); it != m_defaultHeaders.end(); ++it)
        req.setRawHeader(it.key().toUtf8(), it.value().toUtf8());
    for (auto it = headers.begin(); it != headers.end(); ++it)
        req.setRawHeader(it.key().toUtf8(), it.value().toUtf8());

    auto *reply = m_manager->get(req);
    connect(reply, &QNetworkReply::finished, this, [reply, cb]() {
        if (reply->error() == QNetworkReply::NoError) {
            cb(true, reply->readAll());
        } else {
            cb(false, QByteArray());
        }
        reply->deleteLater();
    });
}

void ApiClient::uploadRaw(const QString &url, const QByteArray &data,
                           const QString &contentType, Callback cb)
{
    QUrl theUrl(url);
    QNetworkRequest req(theUrl);
    req.setRawHeader("User-Agent", "SuperLauncher/2.0");
    req.setRawHeader("Content-Type", contentType.toUtf8());

    auto *reply = m_manager->post(req, data);
    connect(reply, &QNetworkReply::finished, this, [reply, cb]() {
        if (reply->error() == QNetworkReply::NoError) {
            QJsonDocument doc = QJsonDocument::fromJson(reply->readAll());
            cb(true, doc);
        } else {
            cb(false, QJsonDocument());
        }
        reply->deleteLater();
    });
}

void ApiClient::downloadFile(const QString &url, const QString &savePath,
                             Callback cb, ProgressCallback prog)
{
    QUrl theUrl(url);
    QNetworkRequest req(theUrl);
    req.setRawHeader("User-Agent", "SuperLauncher/2.0");

    auto *reply = m_manager->get(req);
    if (prog)
        connect(reply, &QNetworkReply::downloadProgress, this, prog);

    connect(reply, &QNetworkReply::finished, this, [reply, savePath, cb]() {
        if (reply->error() == QNetworkReply::NoError) {
            QFile f(savePath);
            if (f.open(QIODevice::WriteOnly)) {
                f.write(reply->readAll());
                f.close();
                cb(true, QJsonDocument());
            } else {
                cb(false, QJsonDocument());
            }
        } else {
            cb(false, QJsonDocument());
        }
        reply->deleteLater();
    });
}
