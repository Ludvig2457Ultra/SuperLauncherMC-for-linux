#ifndef MODPACK_H
#define MODPACK_H

#include <QString>
#include <QStringList>

struct ModpackVersion {
    QString   versionNumber;
    QString   id;
    QStringList gameVersions;
    QStringList loaders;
    QStringList files;       // download URLs
};

struct Modpack {
    QString   id;
    QString   slug;
    QString   name;
    QString   description;
    QString   iconUrl;
    QString   author;
    int       downloads = 0;
    QString   source;   // "modrinth" or "curseforge"
};

struct InstalledPack {
    QString name;
    QString mcVersion;
    QString loader;
    QString source;
    QString versionId;
    QStringList installedFiles;
};

#endif // MODPACK_H
