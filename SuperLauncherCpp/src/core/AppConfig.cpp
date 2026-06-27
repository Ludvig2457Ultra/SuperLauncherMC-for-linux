#include "AppConfig.h"
#include <QFile>
#include <QJsonDocument>
#include <QJsonObject>
#include <QVariant>

AppConfig& AppConfig::instance()
{
    static AppConfig cfg;
    return cfg;
}

void AppConfig::load(const QString &path)
{
    m_path = path;
    QFile f(path);
    if (f.open(QIODevice::ReadOnly)) {
        m_data = QJsonDocument::fromJson(f.readAll()).object();
        f.close();
    } else {
        m_data = {
            {"java_path", ""},
            {"ram", 4096},
            {"max_ram", 4096},
            {"jvm_args", ""},
            {"language", "ru"},
            {"theme", "dark"},
            {"launch_mode", "launcher_lib"},
            {"curseforge_api_key", ""}
        };
    }
}

void AppConfig::save()
{
    QFile f(m_path);
    if (f.open(QIODevice::WriteOnly)) {
        f.write(QJsonDocument(m_data).toJson(QJsonDocument::Indented));
        f.close();
    }
}

QString AppConfig::getString(const QString &key, const QString &defaultVal) const
{
    return m_data.value(key).toString(defaultVal);
}

int AppConfig::getInt(const QString &key, int defaultVal) const
{
    return m_data.value(key).toInt(defaultVal);
}

bool AppConfig::getBool(const QString &key, bool defaultVal) const
{
    return m_data.value(key).toBool(defaultVal);
}

void AppConfig::setValue(const QString &key, const QVariant &value)
{
    m_data[key] = QJsonValue::fromVariant(value);
}
