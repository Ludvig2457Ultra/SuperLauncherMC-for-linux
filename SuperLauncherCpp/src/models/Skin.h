#ifndef SKIN_H
#define SKIN_H

#include <QString>
#include <QStringList>

struct Skin {
    QString id;
    QString name;
    QString type;
    QString imageUrl;
    QString localPath;
    QStringList colors;
    int     price      = 0;
    bool    unlockedByDefault = false;
};

#endif // SKIN_H
