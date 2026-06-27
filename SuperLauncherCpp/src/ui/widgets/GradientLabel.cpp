#include "GradientLabel.h"
#include <QPainter>
#include <QPainterPath>
#include <QtMath>

GradientLabel::GradientLabel(const QString &text, QWidget *parent)
    : QLabel(text, parent)
{
}

void GradientLabel::setGradientColors(const QColor &start, const QColor &end)
{
    m_gradStart = start;
    m_gradEnd = end;
    update();
}

void GradientLabel::setGradientAngle(qreal angle)
{
    m_angle = angle;
    update();
}

void GradientLabel::paintEvent(QPaintEvent *)
{
    QPainter p(this);
    p.setRenderHint(QPainter::Antialiasing);

    qreal rad = qDegreesToRadians(m_angle);
    qreal dx = qCos(rad) * width();
    qreal dy = qSin(rad) * height();

    QLinearGradient grad(width() / 2 - dx / 2, height() / 2 - dy / 2,
                          width() / 2 + dx / 2, height() / 2 + dy / 2);
    grad.setColorAt(0.0, m_gradStart);
    grad.setColorAt(1.0, m_gradEnd);

    QFont f = font();
    f.setPointSize(f.pointSize() > 0 ? f.pointSize() : 14);
    p.setFont(f);

    p.setPen(QPen(QBrush(grad), 1));
    p.drawText(rect(), Qt::AlignCenter, text());
}
