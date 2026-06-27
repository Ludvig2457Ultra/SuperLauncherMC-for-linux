#ifndef BUILDSPAGE_H
#define BUILDSPAGE_H

#include <QWidget>
#include <QLineEdit>
#include <QPushButton>
#include <QListWidget>
#include <QVBoxLayout>
#include <QComboBox>
#include <QProgressBar>
#include "src/models/Modpack.h"

class BuildsManager;

class BuildsPage : public QWidget
{
    Q_OBJECT
public:
    explicit BuildsPage(BuildsManager *builds, QWidget *parent = nullptr);

    void refreshInstalled(const QString &installBase);

signals:
    void installRequested(const ModpackVersion &ver, const QString &source);
    void importRequested(const QString &path);

private:
    void setupUi();

    BuildsManager *m_builds;
    QLineEdit    *m_searchInput  = nullptr;
    QComboBox    *m_sourceCombo  = nullptr;
    QPushButton  *m_searchBtn    = nullptr;
    QListWidget  *m_resultsList  = nullptr;
    QListWidget  *m_installedList = nullptr;
    QProgressBar *m_progressBar  = nullptr;
    QList<Modpack> m_searchResults;
};

#endif // BUILDSPAGE_H
