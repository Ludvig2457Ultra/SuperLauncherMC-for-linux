#ifndef SERVER_H
#define SERVER_H

#include <QString>

struct Server {
    QString name;
    QString version;
    QString type;
    QString dirPath;
    QString ip;
    int     port      = 25565;
    bool    running   = false;
    int     pid       = -1;
};

#endif // SERVER_H
