#ifndef APPCONFIG_H
#define APPCONFIG_H

#include <QString>
#include <QJsonObject>
#include <QMap>

class AppConfig
{
public:
    static AppConfig& instance();

    void load(const QString &path = "settings.json");
    void save();

    QString getString(const QString &key, const QString &defaultVal = {}) const;
    int     getInt(const QString &key, int defaultVal = 0) const;
    bool    getBool(const QString &key, bool defaultVal = false) const;
    void    setValue(const QString &key, const QVariant &value);

    // Convenience
    QString language() const { return getString("language", "ru"); }
    QString theme()    const { return getString("theme", "dark"); }
    int     maxRam()   const { return getInt("max_ram", 4096); }
    QString javaPath() const { return getString("java_path"); }
    QString jvmArgs()  const { return getString("jvm_args"); }
    QString launchMode() const { return getString("launch_mode", "launcher_lib"); }
    QString cfApiKey()  const { return getString("curseforge_api_key"); }

    void setLanguage(const QString &l) { setValue("language", l); }
    void setTheme(const QString &t)    { setValue("theme", t); }
    void setMaxRam(int ram)            { setValue("max_ram", ram); }
    void setJavaPath(const QString &p) { setValue("java_path", p); }
    void setJvmArgs(const QString &a)  { setValue("jvm_args", a); }
    void setLaunchMode(const QString &m) { setValue("launch_mode", m); }
    void setCfApiKey(const QString &k) { setValue("curseforge_api_key", k); }

private:
    AppConfig() = default;
    QJsonObject m_data;
    QString     m_path;
};

#endif // APPCONFIG_H
