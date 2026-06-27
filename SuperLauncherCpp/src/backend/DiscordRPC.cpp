#include "DiscordRPC.h"
#include <QJsonDocument>
#include <QDateTime>
#include <QTcpSocket>
#include <QCoreApplication>
#include <QDir>
#ifdef Q_OS_WIN
#include <windows.h>
#include <namedpipeapi.h>
#endif

// Discord IPC uses Unix sockets on macOS/Linux and named pipes on Windows.
// This is a simplified implementation using TCP connections to the Discord IPC.

DiscordRPC::DiscordRPC(QObject *parent)
    : QObject(parent)
{
    m_keepAlive = new QTimer(this);
    QObject::connect(static_cast<QTimer*>(m_keepAlive), &QTimer::timeout, this, [this]() {
        if (m_connected) {
            QJsonObject data;
            data["cmd"] = "PING";
            sendFrame(1, data);
        }
    });
}

DiscordRPC::~DiscordRPC()
{
    disconnect();
}

void DiscordRPC::connect()
{
    // Attempt TCP connection to Discord IPC
    auto *socket = new QTcpSocket(this);
    socket->connectToHost("127.0.0.1", 6463);
    if (socket->waitForConnected(5000)) {
        m_connected = true;
        m_socketFd = socket->socketDescriptor();

        // Handshake
        QJsonObject handshake;
        handshake["v"] = 1;
        handshake["client_id"] = m_clientId;
        sendFrame(0, handshake);

        m_keepAlive->start(15000);
        emit connected();
    } else {
        m_connected = false;
    }
    socket->deleteLater();
}

void DiscordRPC::disconnect()
{
    m_keepAlive->stop();
    if (m_connected) {
        QJsonObject data;
        data["cmd"] = "DISPATCH";
        sendFrame(2, data);
        m_connected = false;
        emit disconnected();
    }
}

bool DiscordRPC::isConnected() const
{
    return m_connected;
}

void DiscordRPC::setState(const QString &state, const QString &details,
                           const QString &largeImage,
                           const QString &largeText,
                           const QString &smallImage,
                           const QString &smallText)
{
    if (!m_connected) return;

    QJsonObject assets;
    assets["large_image"] = largeImage;
    assets["large_text"]  = largeText;
    if (!smallImage.isEmpty())
        assets["small_image"] = smallImage;
    if (!smallText.isEmpty())
        assets["small_text"]  = smallText;

    QJsonObject timestamps;
    timestamps["start"] = QDateTime::currentSecsSinceEpoch();

    QJsonObject presence;
    presence["state"]      = state;
    presence["details"]    = details;
    presence["assets"]     = assets;
    presence["timestamps"] = timestamps;

    sendPresence(presence);
}

void DiscordRPC::setIdle()
{
    setState("В простое", "SuperLauncher");
}

void DiscordRPC::setInGame(const QString &version)
{
    setState("Играет в Minecraft " + version,
             "SuperLauncher",
             "minecraft", "Minecraft " + version);
}

void DiscordRPC::sendPresence(const QJsonObject &presence)
{
    QJsonObject args;
    args["pid"]  = QCoreApplication::applicationPid();
    args["activity"] = presence;

    QJsonObject data;
    data["cmd"]  = "SET_ACTIVITY";
    data["args"] = args;
    data["nonce"] = QString::number(QDateTime::currentMSecsSinceEpoch());

    sendFrame(1, data);
}

void DiscordRPC::sendFrame(int op, const QJsonObject &data)
{
    QByteArray frame = encodeFrame(op, data);
    if (m_socketFd >= 0) {
        // Write to socket
        auto socket = qobject_cast<QTcpSocket*>(sender());
        if (!socket) return;
        socket->write(frame);
        socket->flush();
    }
}

QByteArray DiscordRPC::encodeFrame(int op, const QJsonObject &data)
{
    QByteArray payload = QJsonDocument(data).toJson(QJsonDocument::Compact);
    quint32 len = payload.size();

    QByteArray frame;
    frame.append((op >> 0) & 0xFF);
    frame.append((op >> 8) & 0xFF);
    frame.append((op >> 16) & 0xFF);
    frame.append((op >> 24) & 0xFF);
    frame.append((len >> 0) & 0xFF);
    frame.append((len >> 8) & 0xFF);
    frame.append((len >> 16) & 0xFF);
    frame.append((len >> 24) & 0xFF);
    frame.append(payload);
    return frame;
}
