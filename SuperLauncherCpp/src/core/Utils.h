#ifndef UTILS_H
#define UTILS_H

#include <QString>
#include <QDir>
#include <QFile>

inline bool copyDir(const QString &src, const QString &dst)
{
    QDir srcDir(src);
    if (!srcDir.exists()) return false;
    QDir dstDir(dst);
    if (!dstDir.exists())
        dstDir.mkpath(".");

    bool ok = true;
    for (const auto &entry : srcDir.entryInfoList(QDir::Files | QDir::Dirs | QDir::NoDotAndDotDot)) {
        if (entry.isDir()) {
            ok &= copyDir(entry.absoluteFilePath(), dst + "/" + entry.fileName());
        } else {
            QFile::remove(dst + "/" + entry.fileName());
            ok &= QFile::copy(entry.absoluteFilePath(), dst + "/" + entry.fileName());
        }
    }
    return ok;
}

#endif // UTILS_H
