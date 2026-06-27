#ifndef TRANSLATIONS_H
#define TRANSLATIONS_H

#include <QString>
#include <QMap>
#include <QJsonObject>

class Translations
{
public:
    static Translations& instance();

    void load(const QString &lang = "ru");
    QString tr(const QString &key) const;
    QString currentLang() const { return m_lang; }

private:
    Translations() = default;
    QMap<QString, QJsonObject> m_data;
    QString m_lang = "ru";
};

#define trKey(key) Translations::instance().tr(key)

#endif // TRANSLATIONS_H
