#ifndef MINECRAFTLAUNCHER_H
#define MINECRAFTLAUNCHER_H

#include <QObject>
#include <QString>
#include <QProcess>
#include <QJsonObject>
#include <functional>

class ApiClient;

class MinecraftLauncher : public QObject
{
    Q_OBJECT
public:
    explicit MinecraftLauncher(ApiClient *client, QObject *parent = nullptr);

    void launch(const QString &mcDir, const QString &username,
                const QString &version, const QString &loader,
                int minMem, int maxMem,
                const QString &jvmArgs,
                std::function<void(const QString &)> logLine);

    void installVersion(const QString &mcDir, const QString &version,
                        const QString &loader,
                        std::function<void(bool)> cb);

    void kill();

    static QString findJava();
    static QStringList parseJvmArgs(const QString &args);

signals:
    void launchStarted();
    void launchFinished(int exitCode);
    void outputReceived(const QString &line);

private:
    QString formatJvmArg(const QString &arg, int minMem, int maxMem, const QString &mcDir);
    void downloadFile(const QString &url, const QString &dest,
                      std::function<void(bool)> cb);

    ApiClient *m_client;
    QProcess  *m_process = nullptr;
};

#endif // MINECRAFTLAUNCHER_H
