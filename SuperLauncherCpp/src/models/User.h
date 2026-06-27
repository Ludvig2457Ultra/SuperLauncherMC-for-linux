#ifndef USER_H
#define USER_H

#include <QString>
#include <QStringList>

struct User {
    QString     userId;
    QString     username;
    QString     email;
    QString     passwordHash;
    QString     salt;
    QString     createdAt;
    QString     lastLogin;
    QString     licenseTier  = "free";
    int         xp           = 0;
    int         level        = 1;
    QStringList skins;
    QString     currentSkin;
    QStringList giftsClaimed;
    QStringList achievements;
    QStringList friends;
};

#endif // USER_H
