#include "MinecraftLauncher.h"
#include "src/network/ApiClient.h"
#include "src/core/Constants.h"
#include <QDir>
#include <QDirIterator>
#include <QFile>
#include <QFileInfo>
#include <QJsonArray>
#include <QJsonDocument>
#include <QJsonObject>
#include <QProcessEnvironment>
#include <QStandardPaths>
#include <QThread>

MinecraftLauncher::MinecraftLauncher(ApiClient *client, QObject *parent)
    : QObject(parent), m_client(client)
{
}

QString MinecraftLauncher::findJava()
{
    // Try common Java paths
    QStringList candidates = {
        "java",
        QStandardPaths::findExecutable("java"),
#ifdef Q_OS_WIN
        QDir::rootPath() + "Program Files/Java/jre*/bin/java.exe",
        QDir::rootPath() + "Program Files (x86)/Java/jre*/bin/java.exe",
        QDir::homePath() + "/.jdk/*/bin/java.exe",
#endif
#ifdef Q_OS_LINUX
        "/usr/lib/jvm/java-*-openjdk-*/bin/java",
        "/usr/lib/jvm/java-*-oracle/bin/java",
#endif
    };

    for (const auto &pattern : candidates) {
        if (pattern.contains('*')) {
            auto files = QDir::root().entryList({QFileInfo(pattern).fileName()},
                                                 QDir::Files);
            if (!files.isEmpty())
                return QFileInfo(pattern).absoluteDir().absoluteFilePath(files.first());
        }
        QString exe = QStandardPaths::findExecutable(
            QFileInfo(pattern).fileName(), {QFileInfo(pattern).absolutePath()});
        if (!exe.isEmpty()) return exe;
    }
    return {};
}

QStringList MinecraftLauncher::parseJvmArgs(const QString &args)
{
    QStringList result;
    bool inQuote = false;
    QString current;
    for (const QChar &c : args) {
        if (c == '"' || c == '\'') {
            inQuote = !inQuote;
            continue;
        }
        if (c == ' ' && !inQuote) {
            if (!current.trimmed().isEmpty())
                result.append(current.trimmed());
            current.clear();
        } else {
            current += c;
        }
    }
    if (!current.trimmed().isEmpty())
        result.append(current.trimmed());
    return result;
}

void MinecraftLauncher::launch(const QString &mcDir, const QString &username,
                                const QString &version, const QString &loader,
                                int minMem, int maxMem,
                                const QString &jvmArgs,
                                std::function<void(const QString &)> logLine)
{
    QString javaPath = findJava();
    if (javaPath.isEmpty()) {
        logLine("Java not found!");
        emit launchFinished(-1);
        return;
    }

    QString nativesDir = mcDir + "/versions/" + version + "/natives";
    QString librariesDir = mcDir + "/libraries";
    QString assetsDir = mcDir + "/assets";
    QString assetsIndex = mcDir + "/assets/indexes/" + version + ".json";

    QDir().mkpath(nativesDir);

    // Build classpath from libraries
    QStringList classpathItems;
    // Main jar
    QString mainJar = mcDir + "/versions/" + version + "/" + version + ".jar";
    if (QFile::exists(mainJar))
        classpathItems.append(mainJar);

    // Library jars
    QDirIterator it(librariesDir, {"*.jar"}, QDir::Files, QDirIterator::Subdirectories);
    while (it.hasNext()) {
        classpathItems.append(it.next());
    }

    QString classpath = classpathItems.join(";");

    QString mainClass = "net.minecraft.client.main.Main";
    // For Fabric/Forge loaders, attempt to detect main class
    if (loader == "fabric") {
        QString fabricJar = mcDir + "/versions/" + version + "-fabric/" + version + "-fabric.jar";
        if (QFile::exists(fabricJar))
            mainClass = "net.fabricmc.loader.launch.knot.KnotClient";
    } else if (loader == "forge") {
        mainClass = "cpw.mods.modlauncher.Launcher";
    }

    QStringList args;
    args << javaPath;
    args << parseJvmArgs(jvmArgs);
    args << "-Xms" + QString::number(minMem) + "M";
    args << "-Xmx" + QString::number(maxMem) + "M";
    args << "-Djava.library.path=" + nativesDir;
    args << "-cp" << classpath;
    args << mainClass;
    args << "--username" << username;
    args << "--version" << (loader.isEmpty() ? version : loader + "-" + version);
    args << "--gameDir" << mcDir;
    args << "--assetsDir" << assetsDir;
    args << "--assetIndex" << version;
    args << "--uuid" << "00000000-0000-0000-0000-000000000000";
    args << "--accessToken" << "0";
    args << "--userType" << "mojang";
    args << "--versionType" << (loader.isEmpty() ? "release" : loader);

    logLine("Launching Minecraft " + version + "...");
    logLine("Java: " + javaPath);
    logLine("Args: " + args.join(" "));

    m_process = new QProcess(this);
    m_process->setProcessChannelMode(QProcess::MergedChannels);
    m_process->setWorkingDirectory(mcDir);

    connect(m_process, &QProcess::readyReadStandardOutput, this, [this, logLine]() {
        QString output = QString::fromUtf8(m_process->readAllStandardOutput());
        logLine(output.trimmed());
        emit outputReceived(output);
    });

    connect(m_process, QOverload<int, QProcess::ExitStatus>::of(&QProcess::finished),
            this, [this](int exitCode, QProcess::ExitStatus) {
        emit launchFinished(exitCode);
    });

    emit launchStarted();
    m_process->start(args.first(), args.mid(1));
}

void MinecraftLauncher::installVersion(const QString &mcDir,
                                        const QString &version,
                                        const QString &loader,
                                        std::function<void(bool)> cb)
{
    // Download version manifest
    QString manifestUrl = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json";
    m_client->get(manifestUrl,
        [this, mcDir, version, loader, cb](bool ok, const QJsonDocument &doc) {
            if (!ok || !doc.isObject()) { cb(false); return; }
            QJsonArray versions = doc.object()["versions"].toArray();
            QString versionUrl;
            for (const auto &v : versions) {
                if (v.toObject()["id"].toString() == version) {
                    versionUrl = v.toObject()["url"].toString();
                    break;
                }
            }
            if (versionUrl.isEmpty()) { cb(false); return; }

            m_client->get(versionUrl,
                [this, mcDir, version, loader, cb](bool ok2, const QJsonDocument &vd) {
                    if (!ok2) { cb(false); return; }
                    QJsonObject vObj = vd.object();
                    QString clientUrl = vObj["downloads"].toObject()["client"].toObject()["url"].toString();
                    if (clientUrl.isEmpty()) { cb(false); return; }

                    QString verDir = mcDir + "/versions/" + version;
                    QDir().mkpath(verDir);

                    downloadFile(clientUrl, verDir + "/" + version + ".jar", cb);
                }
            );
        }
    );
}

void MinecraftLauncher::downloadFile(const QString &url, const QString &dest,
                                      std::function<void(bool)> cb)
{
    m_client->downloadFile(url, dest,
        [cb](bool ok, const QJsonDocument &) { cb(ok); }
    );
}

void MinecraftLauncher::kill()
{
    if (m_process && m_process->state() != QProcess::NotRunning) {
        m_process->kill();
        m_process->waitForFinished(3000);
    }
}
