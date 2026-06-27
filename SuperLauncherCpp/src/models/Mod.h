#ifndef MOD_H
#define MOD_H

#include <QString>
#include <QStringList>

struct ModVersion {
    QString versionNumber;
    QStringList gameVersions;
    QStringList loaders;
    QString downloadUrl;
    QString filename;
    int       fileSize = 0;
};

struct Mod {
    QString   id;
    QString   slug;
    QString   name;
    QString   title;
    QString   description;
    QString   iconUrl;
    QString   author;
    QString   version;
    QString   downloadUrl;
    QString   source;   // "modrinth" or "curseforge"
    int       downloads = 0;
};

#endif // MOD_H
