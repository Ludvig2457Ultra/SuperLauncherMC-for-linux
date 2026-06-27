#ifndef MODERNSIDEBAR_H
#define MODERNSIDEBAR_H

#include <QWidget>
#include <QVBoxLayout>
#include <QPushButton>
#include <QPropertyAnimation>
#include <QList>

class ModernSidebar : public QWidget
{
    Q_OBJECT
public:
    explicit ModernSidebar(QWidget *parent = nullptr);

    void addItem(const QString &icon, const QString &label, int index);
    void setActiveIndex(int index);
    int activeIndex() const { return m_activeIndex; }
    void setCollapsed(bool collapsed);
    bool isCollapsed() const { return m_collapsed; }
    void setItemCount(int count);

signals:
    void itemClicked(int index);

protected:
    void paintEvent(QPaintEvent *event) override;
    void enterEvent(QEnterEvent *event) override;
    void leaveEvent(QEvent *event) override;

private:
    QPushButton* createSidebarButton(const QString &icon, const QString &label, int index);
    void updateActiveButton();
    void animateWidth(int targetWidth);

    QVBoxLayout *m_layout = nullptr;
    QList<QPushButton*> m_buttons;
    int m_activeIndex = 0;
    bool m_collapsed = false;
    int m_expandedWidth = 220;
    int m_collapsedWidth = 56;
    QPropertyAnimation *m_widthAnim = nullptr;
    int m_itemCount = 11;
    bool m_animating = false;
};

#endif // MODERNSIDEBAR_H
