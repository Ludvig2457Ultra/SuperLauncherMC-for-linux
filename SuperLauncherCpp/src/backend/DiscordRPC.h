#ifndef DISCORDRPC_H
#define DISCORDRPC_H

#include <QObject>
#include <QString>
#include <QTimer>
#include <QJsonObject>

class DiscordRPC : public QObject
{
    Q_OBJECT
public:
    explicit DiscordRPC(QObject *parent = nullptr);
    ~DiscordRPC();

    void connect();
    void disconnect();
    bool isConnected() const;

    void setState(const QString &state, const QString &details,
                  const QString &largeImage = "logo",
                  const QString &largeText = "SuperLauncher",
                  const QString &smallImage = {},
                  const QString &smallText = {});
    void setIdle();
    void setInGame(const QString &version);

signals:
    void connected();
    void disconnected();

private:
    void sendPresence(const QJsonObject &presence);
    void sendFrame(int op, const QJsonObject &data);
    QByteArray encodeFrame(int op, const QJsonObject &data);

    int m_socketFd = -1;
    bool m_connected = false;
    QTimer *m_keepAlive = nullptr;
    QString m_clientId = "1324567890123456789";
};

#endif // DISCORDRPC_H
