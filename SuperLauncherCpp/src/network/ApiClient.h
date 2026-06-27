#ifndef APICLIENT_H
#define APICLIENT_H

#include <QObject>
#include <QNetworkAccessManager>
#include <QNetworkReply>
#include <QJsonObject>
#include <QJsonArray>
#include <functional>

class ApiClient : public QObject
{
    Q_OBJECT
public:
    using Callback = std::function<void(bool ok, const QJsonDocument &doc)>;
    using ProgressCallback = std::function<void(qint64 received, qint64 total)>;

    explicit ApiClient(QObject *parent = nullptr);

    void get(const QString &url, Callback cb,
             const QMap<QString, QString> &headers = {});
    void get(const QString &url, Callback cb,
             ProgressCallback prog,
             const QMap<QString, QString> &headers = {});

    void post(const QString &url, const QJsonObject &body, Callback cb,
              const QMap<QString, QString> &headers = {});

    void getRaw(const QString &url,
                std::function<void(bool ok, const QByteArray &data)> cb,
                const QMap<QString, QString> &headers = {});

    void uploadRaw(const QString &url, const QByteArray &data,
                   const QString &contentType, Callback cb);

    void downloadFile(const QString &url, const QString &savePath,
                      Callback cb, ProgressCallback prog = nullptr);

    void setDefaultHeader(const QString &key, const QString &value);

private:
    QNetworkAccessManager *m_manager;
    QMap<QString, QString> m_defaultHeaders;
};

#endif // APICLIENT_H
