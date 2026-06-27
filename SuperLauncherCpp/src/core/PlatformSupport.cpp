#include "PlatformSupport.h"
#include <QStandardPaths>
#include <QDir>
#include <QProcess>
#include <QFileInfo>
#include <QOperatingSystemVersion>

QString PlatformSupport::minecraftPath()
{
#ifdef Q_OS_WIN
    return QStandardPaths::writableLocation(QStandardPaths::GenericDataLocation)
           + "/.minecraft";
#elif defined(Q_OS_MACOS)
    return QDir::homePath() + "/Library/Application Support/minecraft";
#else
    return QDir::homePath() + "/.minecraft";
#endif
}

QString PlatformSupport::appDataPath()
{
#ifdef Q_OS_WIN
    return QStandardPaths::writableLocation(QStandardPaths::AppDataLocation);
#elif defined(Q_OS_MACOS)
    return QDir::homePath() + "/Library/Application Support/SuperLauncher";
#else
    return QDir::homePath() + "/.config/SuperLauncher";
#endif
}

QString PlatformSupport::findJavaPath()
{
    QStringList candidates;
#ifdef Q_OS_WIN
    QString pf = qEnvironmentVariable("ProgramFiles", "C:\\Program Files");
    QString pfx86 = qEnvironmentVariable("ProgramFiles(x86)", "C:\\Program Files (x86)");
    candidates << pf + "/Java/jdk-*/bin/java.exe"
               << pf + "/Java/jre-*/bin/java.exe"
               << pfx86 + "/Java/jdk-*/bin/java.exe"
               << pfx86 + "/Java/jre-*/bin/java.exe"
               << "C:\\ProgramData\\Oracle\\Java\\javapath\\java.exe";
#elif defined(Q_OS_MACOS)
    candidates << "/usr/bin/java"
               << "/Library/Internet Plug-Ins/JavaAppletPlugin.plugin/Contents/Home/bin/java"
               << "/opt/homebrew/opt/openjdk/bin/java";
#else
    candidates << "/usr/bin/java"
               << "/usr/lib/jvm/default-java/bin/java";
#endif
    for (auto &p : candidates) {
        if (p.contains('*')) {
            QDir dir(QFileInfo(p).path());
            QString filter = QFileInfo(p).fileName();
            auto entries = dir.entryList({filter}, QDir::Files);
            if (!entries.isEmpty())
                return dir.absoluteFilePath(entries.first());
        } else {
            if (QFileInfo::exists(p))
                return p;
        }
    }
    return QStandardPaths::findExecutable("java");
}

bool PlatformSupport::isMacArm()
{
#ifdef Q_OS_MACOS
    QProcess proc;
    proc.start("sysctl", {"-n", "machdep.cpu.brand_string"});
    proc.waitForFinished();
    return QString::fromUtf8(proc.readAllStandardOutput()).contains("Apple");
#endif
    return false;
}

QStringList PlatformSupport::platformOptimizations()
{
#ifdef Q_OS_WIN
    return {"Обновите драйверы видеокарты",
            "Включите игровой режим в Windows",
            "Проверьте антивирус"};
#elif defined(Q_OS_MACOS)
    return {"Используйте ARM-версию Java",
            "Включите Metal API",
            "Проверьте обновления macOS"};
#else
    return {"Установите проприетарные драйверы NVIDIA",
            "Используйте OpenJDK 17+",
            "Проверьте права доступа к .minecraft"};
#endif
}

QString PlatformSupport::platformInfo()
{
    return QSysInfo::prettyProductName() + " (" + QSysInfo::currentCpuArchitecture() + ")";
}
