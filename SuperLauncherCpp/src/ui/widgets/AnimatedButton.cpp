#include "AnimatedButton.h"
#include <QPainter>
#include <QPainterPath>
#include <QTimer>

AnimatedButton::AnimatedButton(const QString &text, QWidget *parent)
    : QPushButton(text, parent)
{
    setCursor(Qt::PointingHandCursor);
    setFixedHeight(36);
    setMinimumWidth(80);
    setMouseTracking(true);

    m_hoverAnim = new QPropertyAnimation(this, "hoverColor", this);
    m_hoverAnim->setDuration(200);
}

void AnimatedButton::setDefaultStyle(const QString &style)
{
    setStyleSheet(style);
}

void AnimatedButton::setHoverColor(const QColor &c)
{
    m_hoverColor = c;
    m_currentBg = c;
    update();
}

QColor AnimatedButton::hoverColor() const
{
    return m_hoverColor;
}

void AnimatedButton::animateClick()
{
    QPropertyAnimation *anim = new QPropertyAnimation(this, "geometry", this);
    QRect start = geometry();
    QRect end = start.adjusted(2, 2, -2, -2);
    anim->setDuration(100);
    anim->setKeyValueAt(0, start);
    anim->setKeyValueAt(0.5, end);
    anim->setKeyValueAt(1, start);
    anim->start(QAbstractAnimation::DeleteWhenStopped);

    QTimer::singleShot(100, this, [this]() {
        emit clicked();
    });
}

void AnimatedButton::enterEvent(QEnterEvent *)
{
    m_hoverAnim->stop();
    m_hoverAnim->setStartValue(m_currentBg);
    m_hoverAnim->setEndValue(m_hoverBg);
    m_hoverAnim->setDuration(200);
    m_hoverAnim->start();
}

void AnimatedButton::leaveEvent(QEvent *)
{
    m_hoverAnim->stop();
    m_hoverAnim->setStartValue(m_currentBg);
    m_hoverAnim->setEndValue(m_defaultBg);
    m_hoverAnim->setDuration(200);
    m_hoverAnim->start();
}

void AnimatedButton::paintEvent(QPaintEvent *)
{
    QPainter p(this);
    p.setRenderHint(QPainter::Antialiasing);

    QPainterPath path;
    path.addRoundedRect(rect(), m_borderRadius, m_borderRadius);
    p.fillPath(path, m_currentBg);

    p.setPen(m_textColor);
    p.setFont(font());
    p.drawText(rect(), Qt::AlignCenter, text());
}
