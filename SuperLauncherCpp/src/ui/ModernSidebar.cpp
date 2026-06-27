#include "ModernSidebar.h"
#include <QPainter>
#include <QPainterPath>
#include <QEnterEvent>

ModernSidebar::ModernSidebar(QWidget *parent)
    : QWidget(parent)
{
    setFixedWidth(m_expandedWidth);

    m_layout = new QVBoxLayout(this);
    m_layout->setContentsMargins(8, 20, 8, 20);
    m_layout->setSpacing(4);

    m_layout->addStretch(0);
}

void ModernSidebar::setItemCount(int count)
{
    m_itemCount = count;
}

void ModernSidebar::addItem(const QString &icon, const QString &label, int index)
{
    auto *btn = createSidebarButton(icon, label, index);
    m_layout->insertWidget(m_layout->count() - 1, btn);
    m_buttons.append(btn);
}

QPushButton* ModernSidebar::createSidebarButton(const QString &icon,
                                                 const QString &label, int index)
{
    auto *btn = new QPushButton(this);
    btn->setFixedHeight(44);
    btn->setCursor(Qt::PointingHandCursor);
    btn->setCheckable(true);

    btn->setText(icon + "  " + label);
    btn->setFont(QFont("Segoe UI", 11, QFont::Normal));

    connect(btn, &QPushButton::clicked, this, [this, index]() {
        setActiveIndex(index);
        emit itemClicked(index);
    });

    return btn;
}

void ModernSidebar::setActiveIndex(int index)
{
    m_activeIndex = index;
    updateActiveButton();
}

void ModernSidebar::setCollapsed(bool collapsed)
{
    if (m_animating) return;
    m_collapsed = collapsed;
    int target = collapsed ? m_collapsedWidth : m_expandedWidth;
    animateWidth(target);

    QStringList icons = {"\u2302",  "\u25CB", "\u25A3", "\u2B07", "\u2660",
                         "\u2261",  "\u21BB", "\u2B21", "\u2699", "\u25B6",
                         "\u25C6"};
    QStringList labels = {"Главная", "Аккаунт",  "Моды",   "Сборки",
                          "Скины",   "Новости",  "Обновления", "Серверы",
                          "Настройки", "Minecraft", "AI Агент"};

    for (int i = 0; i < m_buttons.size() && i < labels.size(); ++i) {
        if (collapsed) {
            m_buttons[i]->setText(icons[i]);
        } else {
            m_buttons[i]->setText(icons[i] + "  " + labels[i]);
        }
    }
}

void ModernSidebar::animateWidth(int targetWidth)
{
    if (m_widthAnim) {
        m_widthAnim->stop();
        m_widthAnim->deleteLater();
        m_widthAnim = nullptr;
    }

    m_animating = true;

    m_widthAnim = new QPropertyAnimation(this, "fixedWidth", this);
    m_widthAnim->setDuration(200);
    m_widthAnim->setEasingCurve(QEasingCurve::OutQuad);
    m_widthAnim->setStartValue(width());
    m_widthAnim->setEndValue(targetWidth);

    connect(m_widthAnim, &QPropertyAnimation::finished, this, [this]() {
        m_animating = false;
        m_widthAnim = nullptr;
    });

    m_widthAnim->start(QAbstractAnimation::DeleteWhenStopped);
}

void ModernSidebar::updateActiveButton()
{
    for (int i = 0; i < m_buttons.size(); ++i) {
        m_buttons[i]->setChecked(i == m_activeIndex);
        if (i == m_activeIndex) {
            m_buttons[i]->setStyleSheet(
                "QPushButton { background: qlineargradient(x1:0,y1:0,x2:0,y2:1, "
                "stop:0 rgba(79,172,254,0.3), stop:1 rgba(118,75,162,0.3)); "
                "color: white; border: none; border-radius: 8px; "
                "text-align: left; padding-left: 8px; }");
        } else {
            m_buttons[i]->setStyleSheet(
                "QPushButton { background: transparent; color: #AAAAAA; "
                "border: none; border-radius: 8px; text-align: left; padding-left: 8px; }"
                "QPushButton:hover { background: rgba(255,255,255,0.08); color: #DDDDDD; }");
        }
    }
}

void ModernSidebar::paintEvent(QPaintEvent *)
{
    QPainter p(this);
    p.setRenderHint(QPainter::Antialiasing);

    QLinearGradient grad(0, 0, width(), height());
    grad.setColorAt(0.0, QColor(16, 16, 26));
    grad.setColorAt(1.0, QColor(12, 12, 20));
    p.fillRect(rect(), grad);

    QPen borderPen(QColor(255, 255, 255, 16), 1);
    p.setPen(borderPen);
    p.drawLine(width() - 1, 0, width() - 1, height());
}

void ModernSidebar::enterEvent(QEnterEvent *)
{
    if (m_collapsed && !m_animating) setCollapsed(false);
}

void ModernSidebar::leaveEvent(QEvent *)
{
    if (!m_collapsed && !m_animating) setCollapsed(true);
}
