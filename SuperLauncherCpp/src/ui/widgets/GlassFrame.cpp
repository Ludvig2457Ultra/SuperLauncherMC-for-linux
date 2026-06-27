#include "GlassFrame.h"
#include <QPainterPath>
#include <QGraphicsBlurEffect>

GlassFrame::GlassFrame(QWidget *parent)
    : QFrame(parent)
{
    setAttribute(Qt::WA_TranslucentBackground);
}

void GlassFrame::setBlurIntensity(qreal radius) { m_blurRadius = radius; }
void GlassFrame::setTintColor(const QColor &c) { m_tintColor = c; }
void GlassFrame::setBorderRadius(int r) { m_borderRadius = r; }
void GlassFrame::setBorderColor(const QColor &c) { m_borderColor = c; }

void GlassFrame::paintEvent(QPaintEvent *)
{
    QPainter p(this);
    p.setRenderHint(QPainter::Antialiasing);
    p.setRenderHint(QPainter::SmoothPixmapTransform);

    QPainterPath path;
    path.addRoundedRect(rect().adjusted(2, 2, -2, -2), m_borderRadius, m_borderRadius);

    p.fillPath(path, m_tintColor);

    QPen pen(m_borderColor, 1);
    p.setPen(pen);
    p.drawPath(path);
}
