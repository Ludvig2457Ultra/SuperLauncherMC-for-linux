#ifndef MODSPAGE_H
#define MODSPAGE_H

#include <QWidget>
#include <QListWidget>
#include <QLineEdit>
#include <QPushButton>
#include <QVBoxLayout>
#include <QComboBox>
#include "src/models/Mod.h"

class ModManager;

class ModsPage : public QWidget
{
    Q_OBJECT
public:
    explicit ModsPage(ModManager *modManager, QWidget *parent = nullptr);

    void refreshLocalMods(const QString &modsDir);

signals:
    void searchRequested(const QString &query);
    void downloadRequested(const Mod &mod);
    void removeRequested(const QString &path);

private:
    void setupUi();
    void onSearchResult(bool ok, const QList<Mod> &mods);
    void onLocalModsLoaded(const QList<Mod> &mods);

    ModManager  *m_modManager;
    QLineEdit   *m_searchInput   = nullptr;
    QComboBox   *m_sourceCombo   = nullptr;
    QPushButton *m_searchBtn     = nullptr;
    QListWidget *m_modList       = nullptr;
    QListWidget *m_installedList = nullptr;
    QList<Mod>   m_searchResults;
};

#endif // MODSPAGE_H
