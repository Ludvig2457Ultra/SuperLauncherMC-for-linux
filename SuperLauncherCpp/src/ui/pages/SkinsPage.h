#ifndef SKINSPAGE_H
#define SKINSPAGE_H

#include <QWidget>
#include <QPushButton>
#include <QVBoxLayout>
#include <QGridLayout>
#include <QLabel>
#include <QScrollArea>
#include <QList>
#include "src/models/Skin.h"

class SkinsManager;

class SkinsPage : public QWidget
{
    Q_OBJECT
public:
    explicit SkinsPage(SkinsManager *skinsMgr, QWidget *parent = nullptr);

    void refreshSkins(const QString &userDir);

signals:
    void applySkin(const QString &skinId, const QString &username);
    void uploadSkin(const QString &filePath, const QString &username);

private:
    void setupUi();
    void populateSkins();

    SkinsManager *m_skinsMgr;
    QWidget      *m_skinGrid      = nullptr;
    QGridLayout  *m_gridLayout    = nullptr;
    QLabel       *m_currentSkinLabel = nullptr;
    QString       m_userDir;
    QList<Skin>   m_skins;
};

#endif // SKINSPAGE_H
