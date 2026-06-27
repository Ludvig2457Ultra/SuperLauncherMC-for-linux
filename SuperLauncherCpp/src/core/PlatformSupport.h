#ifndef PLATFORMSUPPORT_H
#define PLATFORMSUPPORT_H

#include <QString>
#include <QStringList>

class PlatformSupport
{
public:
    static QString minecraftPath();
    static QString appDataPath();
    static QString findJavaPath();
    static bool    isMacArm();
    static QStringList platformOptimizations();
    static QString platformInfo();
};

#endif // PLATFORMSUPPORT_H
