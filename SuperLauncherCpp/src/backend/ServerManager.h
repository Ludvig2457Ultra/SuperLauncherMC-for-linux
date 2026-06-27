#ifndef SERVERMANAGER_H
#define SERVERMANAGER_H

#include <QObject>
#include <QString>
#include <QProcess>
#include <QList>
#include <functional>
#include "src/models/Server.h"

class ApiClient;

class ServerManager : public QObject
{
    Q_OBJECT
public:
    explicit ServerManager(ApiClient *client, QObject *parent = nullptr);

    void createServer(const QString &name, const QString &version,
                      const QString &type, const QString &mcDir,
                      std::function<void(bool, const QString &error)> cb);
    void startServer(const QString &serverDir, int ramMB,
                     const QString &javaArgs = {},
                     std::function<void(const QString &)> logLine = {});
    void stopServer();
    void restartServer(const QString &serverDir, int ramMB,
                       const QString &javaArgs = {},
                       std::function<void(const QString &)> logLine = {});
    bool isRunning() const;
    void addServer(const Server &server);
    void removeServer(const QString &name);
    QList<Server> getServers(const QString &serversBase);

    // Playit.gg tunnel
    void startPlayitTunnel(const QString &playitPath);
    void stopPlayitTunnel();

signals:
    void serverStarted();
    void serverStopped(int exitCode);
    void serverOutput(const QString &line);
    void tunnelReady(const QString &url);

private:
    void downloadServerJar(const QString &url, const QString &dest,
                           std::function<void(bool)> cb);

    ApiClient *m_client;
    QProcess  *m_serverProcess  = nullptr;
    QProcess  *m_playitProcess  = nullptr;
    QList<Server> m_servers;
};

#endif // SERVERMANAGER_H
