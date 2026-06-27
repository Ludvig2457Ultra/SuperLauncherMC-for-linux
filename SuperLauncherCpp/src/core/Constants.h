#ifndef CONSTANTS_H
#define CONSTANTS_H

#include <QString>

inline const QString CONFIG_FILE        = "settings.json";
inline const QString ACCOUNTS_FILE      = "accounts.json";
inline const QString LICENSES_FILE      = "licenses.json";
inline const QString GIFTS_FILE         = "gifts.json";
inline const QString UI_SETTINGS_FILE   = "ui_settings.json";
inline const QString SERVERS_FILE       = "servers_list.json";
inline const QString CURRENT_VERSION    = "v2.0.0_2026";
inline const QString MODRINTH_API_URL   = "https://api.modrinth.com/v2";
inline const QString CURSEFORGE_API_URL = "https://api.curseforge.com/v1";
inline const QString LAUNCHER_UPDATE_URL = "https://api.github.com/repos/anomalyco/SuperLauncher/releases/latest";

inline const QString APP_VERSION = CURRENT_VERSION;

#endif // CONSTANTS_H
