#include "Translations.h"
#include <QFile>
#include <QJsonDocument>
#include <QJsonArray>

void Translations::load(const QString &lang)
{
    m_lang = lang;
    m_data.clear();

    QStringList langs = {"ru", "en"};
    for (const auto &l : langs) {
        QFile f(QString("resources/lang/%1.json").arg(l));
        if (f.open(QIODevice::ReadOnly)) {
            QJsonObject obj = QJsonDocument::fromJson(f.readAll()).object();
            m_data[l] = obj;
            f.close();
        }
    }
}

QString Translations::tr(const QString &key) const
{
    auto it = m_data.find(m_lang);
    if (it != m_data.end() && it->contains(key))
        return it->value(key).toString();
    // fallback to english
    auto en = m_data.find("en");
    if (en != m_data.end() && en->contains(key))
        return en->value(key).toString();
    return key;
}

Translations& Translations::instance()
{
    static Translations t;
    return t;
}
