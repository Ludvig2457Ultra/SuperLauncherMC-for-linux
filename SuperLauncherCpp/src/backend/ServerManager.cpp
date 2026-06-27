#include "ServerManager.h"
#include "src/network/ApiClient.h"
#include "src/backend/MinecraftLauncher.h"
#include "src/core/Constants.h"
#include <QDir>
#include <QFile>
#include <QJsonArray>
#include <QJsonDocument>
#include <QJsonObject>
#include <QProcessEnvironment>
#include <QRegularExpression>
#include <QThread>

ServerManager::ServerManager(ApiClient *client, QObject *parent)
    : QObject(parent), m_client(client)
{
}

void ServerManager::createServer(const QString &name, const QString &version,
                                  const QString &type, const QString &mcDir,
                                  std::function<void(bool, const QString &)> cb)
{
    QString serverDir = mcDir + "/servers/" + name;
    QDir().mkpath(serverDir);

    // Build EULA
    QFile eula(serverDir + "/eula.txt");
    if (eula.open(QIODevice::WriteOnly | QIODevice::Text)) {
        eula.write("#By changing the setting below to TRUE you are indicating your agreement to our EULA\n");
        eula.write("eula=true\n");
        eula.close();
    }

    // Download server jar
    QString jarUrl;
    if (type == "vanilla") {
        jarUrl = "https://piston-data.mojang.com/v1/objects/"
                 + version + "/server.jar";
    } else if (type == "fabric") {
        // Fabric installer API
        jarUrl = "https://meta.fabricmc.net/v2/versions/loader/"
                 + version + "/0.15.11/1.0.1/server/jar";
    } else if (type == "forge") {
        jarUrl = "https://maven.minecraftforge.net/net/minecraftforge/forge/"
                 + version + "-forge-" + version + "/forge-" + version + "-server.jar";
    } else if (type == "paper") {
        jarUrl = "https://api.papermc.io/v2/projects/paper/versions/" + version
                 + "/builds/latest/downloads/paper-" + version + "-latest.jar";
    }

    downloadServerJar(jarUrl, serverDir + "/server.jar",
        [this, name, version, type, serverDir, cb](bool ok) {
            if (!ok) { cb(false, "Failed to download server jar"); return; }

            // Create start script
            QFile bat(serverDir + "/start.bat");
            if (bat.open(QIODevice::WriteOnly | QIODevice::Text)) {
                bat.write("@echo off\r\n");
                bat.write("java -Xmx2G -jar server.jar nogui\r\n");
                bat.write("pause\r\n");
                bat.close();
            }

            QString ip = "127.0.0.1";
            int port = 25565 + (name.length() % 100); // unique port per server name

            Server s;
            s.name     = name;
            s.version  = version;
            s.type     = type;
            s.dirPath  = serverDir;
            s.ip       = ip;
            s.port     = port;
            s.running  = false;
            s.pid      = -1;
            addServer(s);

            // Save servers list
            QString serversFile = QFileInfo(serverDir).absolutePath() + "/servers_config.json";
            QFile sf(serversFile);
            if (sf.open(QIODevice::WriteOnly)) {
                QJsonArray arr;
                for (const auto &sv : m_servers) {
                    QJsonObject o;
                    o["name"]    = sv.name;
                    o["version"] = sv.version;
                    o["type"]    = sv.type;
                    o["dir"]     = sv.dirPath;
                    o["ip"]      = sv.ip;
                    o["port"]    = sv.port;
                    arr.append(o);
                }
                QJsonObject root;
                root["servers"] = arr;
                sf.write(QJsonDocument(root).toJson(QJsonDocument::Indented));
                sf.close();
            }

            cb(true, {});
        }
    );
}

void ServerManager::addServer(const Server &server)
{
    m_servers.append(server);
}

void ServerManager::removeServer(const QString &name)
{
    m_servers.erase(
        std::remove_if(m_servers.begin(), m_servers.end(),
                       [&](const Server &s) { return s.name == name; }),
        m_servers.end()
    );
}

QList<Server> ServerManager::getServers(const QString &serversBase)
{
    QList<Server> list;
    QString serversFile = serversBase + "/servers_config.json";
    QFile sf(serversFile);
    if (sf.open(QIODevice::ReadOnly)) {
        QJsonObject root = QJsonDocument::fromJson(sf.readAll()).object();
        for (const auto &v : root["servers"].toArray()) {
            QJsonObject o = v.toObject();
            Server s;
            s.name    = o["name"].toString();
            s.version = o["version"].toString();
            s.type    = o["type"].toString();
            s.dirPath = o["dir"].toString();
            s.ip      = o["ip"].toString();
            s.port    = o["port"].toInt();
            s.running = false;
            list.append(s);
        }
        sf.close();
    }
    return list;
}

void ServerManager::startServer(const QString &serverDir, int ramMB,
                                 const QString &javaArgs,
                                 std::function<void(const QString &)> logLine)
{
    if (m_serverProcess && m_serverProcess->state() != QProcess::NotRunning) {
        if (logLine) logLine("Server already running");
        return;
    }

    QString jarPath = serverDir + "/server.jar";
    if (!QFile::exists(jarPath)) {
        if (logLine) logLine("server.jar not found in " + serverDir);
        return;
    }

    m_serverProcess = new QProcess(this);
    m_serverProcess->setProcessChannelMode(QProcess::MergedChannels);
    m_serverProcess->setWorkingDirectory(serverDir);

    connect(m_serverProcess, &QProcess::readyReadStandardOutput,
            this, [this, logLine]() {
        QString output = QString::fromUtf8(m_serverProcess->readAllStandardOutput());
        if (logLine) logLine(output.trimmed());
        emit serverOutput(output);

        // Detect server started
        if (output.contains("Done") && output.contains("For help"))
            emit serverStarted();
    });

    connect(m_serverProcess,
            QOverload<int, QProcess::ExitStatus>::of(&QProcess::finished),
            this, [this](int code, QProcess::ExitStatus) {
        emit serverStopped(code);
    });

    QString javaPath = MinecraftLauncher::findJava();
    if (javaPath.isEmpty()) {
        if (logLine) logLine("Java not found!");
        return;
    }

    QStringList args = MinecraftLauncher::parseJvmArgs(javaArgs);
    args.prepend("-Xmx" + QString::number(ramMB) + "M");
    args.prepend("-Xms" + QString::number(ramMB / 2) + "M");
    args.prepend(javaPath);
    args << "-jar" << jarPath << "nogui";

    m_serverProcess->setEnvironment(QProcessEnvironment::systemEnvironment().toStringList());
    m_serverProcess->start(args.first(), args.mid(1));
}

void ServerManager::stopServer()
{
    if (m_serverProcess && m_serverProcess->state() != QProcess::NotRunning) {
        m_serverProcess->write("stop\n");
        if (!m_serverProcess->waitForFinished(10000)) {
            m_serverProcess->kill();
            m_serverProcess->waitForFinished(3000);
        }
    }
}

void ServerManager::restartServer(const QString &serverDir, int ramMB,
                                   const QString &javaArgs,
                                   std::function<void(const QString &)> logLine)
{
    stopServer();
    QThread::msleep(1000);
    startServer(serverDir, ramMB, javaArgs, logLine);
}

void ServerManager::downloadServerJar(const QString &url, const QString &dest,
                                       std::function<void(bool)> cb)
{
    m_client->downloadFile(url, dest,
        [cb](bool ok, const QJsonDocument &) { cb(ok); });
}

bool ServerManager::isRunning() const
{
    return m_serverProcess &&
           m_serverProcess->state() != QProcess::NotRunning;
}

void ServerManager::startPlayitTunnel(const QString &playitPath)
{
    if (!QFile::exists(playitPath)) return;
    m_playitProcess = new QProcess(this);
    m_playitProcess->setProcessChannelMode(QProcess::MergedChannels);
    connect(m_playitProcess, &QProcess::readyReadStandardOutput, this, [this]() {
        QString out = QString::fromUtf8(m_playitProcess->readAllStandardOutput());
        QRegularExpression re(R"(https://[a-zA-Z0-9.-]+\.playit\.(gg|xyz))");
        auto match = re.match(out);
        if (match.hasMatch())
            emit tunnelReady(match.captured());
    });
    m_playitProcess->start(playitPath);
}

void ServerManager::stopPlayitTunnel()
{
    if (m_playitProcess && m_playitProcess->state() != QProcess::NotRunning) {
        m_playitProcess->kill();
        m_playitProcess->waitForFinished(3000);
    }
}
