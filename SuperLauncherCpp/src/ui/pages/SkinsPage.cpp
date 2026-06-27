#include "SkinsPage.h"
#include "src/backend/SkinsManager.h"
#include "src/ui/widgets/SkinWidget.h"
#include <QScrollArea>
#include <QFileDialog>
#include <QHBoxLayout>

SkinsPage::SkinsPage(SkinsManager *skinsMgr, QWidget *parent)
    : QWidget(parent), m_skinsMgr(skinsMgr)
{
    setupUi();
}

void SkinsPage::setupUi()
{
    auto *mainLayout = new QVBoxLayout(this);
    mainLayout->setContentsMargins(24, 24, 24, 24);

    auto *title = new QLabel("Скины", this);
    title->setStyleSheet("color: white; font-size: 22px; font-weight: bold;");
    mainLayout->addWidget(title);

    // Current skin display
    m_currentSkinLabel = new QLabel("Текущий скин: default", this);
    m_currentSkinLabel->setStyleSheet("color: #AAAAAA; font-size: 13px;");
    mainLayout->addWidget(m_currentSkinLabel);

    // Upload button
    auto *btnRow = new QHBoxLayout();
    auto *uploadBtn = new QPushButton("Загрузить скин", this);
    uploadBtn->setStyleSheet(
        "QPushButton { background: #7C4DFF; color: white; border: none; "
        "border-radius: 6px; padding: 8px 20px; }"
        "QPushButton:hover { background: #9C6DFF; }");
    connect(uploadBtn, &QPushButton::clicked, this, [this]() {
        QString path = QFileDialog::getOpenFileName(this, "Выберите скин",
                                                     {}, "*.png *.jpg");
        if (!path.isEmpty())
            emit uploadSkin(path, "player");
    });
    btnRow->addWidget(uploadBtn);
    btnRow->addStretch();
    mainLayout->addLayout(btnRow);

    // Skin grid
    auto *scrollArea = new QScrollArea(this);
    scrollArea->setWidgetResizable(true);
    scrollArea->setStyleSheet("QScrollArea { border: none; background: transparent; }");

    m_skinGrid = new QWidget(scrollArea);
    m_gridLayout = new QGridLayout(m_skinGrid);
    m_gridLayout->setSpacing(16);
    scrollArea->setWidget(m_skinGrid);
    mainLayout->addWidget(scrollArea, 1);
}

void SkinsPage::refreshSkins(const QString &userDir)
{
    m_userDir = userDir;
    m_skins = m_skinsMgr->getLocalSkins(userDir);
    populateSkins();

    // Also fetch online skins
    m_skinsMgr->fetchSkins([this](bool, const QList<Skin> &onlineSkins) {
        for (const auto &s : onlineSkins) {
            bool exists = false;
            for (const auto &local : m_skins) {
                if (local.id == s.id) { exists = true; break; }
            }
            if (!exists) m_skins.append(s);
        }
        populateSkins();
    });
}

void SkinsPage::populateSkins()
{
    // Clear grid
    QLayoutItem *item;
    while ((item = m_gridLayout->takeAt(0))) {
        delete item->widget();
        delete item;
    }

    int col = 0, row = 0;
    for (const auto &skin : m_skins) {
        auto *sw = new SkinWidget(m_skinGrid);
        sw->setLabel(skin.name);
        if (!skin.localPath.isEmpty())
            sw->setSkinPath(skin.localPath);
        else if (!skin.imageUrl.isEmpty()) {
            // Would need to download via ApiClient
        }

        connect(sw, &SkinWidget::clicked, this, [this, skin]() {
            emit applySkin(skin.id, "player");
        });

        m_gridLayout->addWidget(sw, row, col);
        col++;
        if (col >= 4) { col = 0; row++; }
    }
}
