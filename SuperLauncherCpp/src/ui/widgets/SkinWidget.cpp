#include "SkinWidget.h"
#include <QPainter>
#include <QPainterPath>
#include <QMouseEvent>

SkinWidget::SkinWidget(QWidget *parent)
    : QWidget(parent)
{
    setMinimumSize(100, 150);
    setCursor(Qt::PointingHandCursor);
}

void SkinWidget::setSkin(const QPixmap &pixmap)
{
    m_skin = pixmap;
    update();
}

void SkinWidget::setSkinPath(const QString &path)
{
    m_skinPath = path;
    m_skin = QPixmap(path);
    update();
}

void SkinWidget::setZoom(qreal factor) { m_zoom = factor; update(); }
void SkinWidget::setShowPreview(bool s) { m_showPreview = s; update(); }
void SkinWidget::setLabel(const QString &t) { m_label = t; update(); }

QPixmap SkinWidget::skin() const { return m_skin; }
QString SkinWidget::skinPath() const { return m_skinPath; }

void SkinWidget::paintEvent(QPaintEvent *)
{
    QPainter p(this);
    p.setRenderHint(QPainter::Antialiasing);
    p.setRenderHint(QPainter::SmoothPixmapTransform);

    int w = width();
    int h = height();

    // Background
    p.fillRect(rect(), QColor(30, 30, 40));

    if (!m_skin.isNull() && m_showPreview) {
        // Draw skin centered, maintaining aspect ratio
        QPixmap scaled = m_skin.scaled(w - 20, h - 40, Qt::KeepAspectRatio,
                                        Qt::SmoothTransformation);
        int x = (w - scaled.width()) / 2;
        int y = (h - scaled.height()) / 2;
        p.drawPixmap(x, y, scaled);
    }

    // Label
    if (!m_label.isEmpty()) {
        p.setPen(QColor(200, 200, 200));
        p.setFont(QFont("Segoe UI", 9));
        p.drawText(QRect(0, h - 25, w, 20), Qt::AlignCenter, m_label);
    }
}

void SkinWidget::mousePressEvent(QMouseEvent *e)
{
    if (e->button() == Qt::LeftButton)
        emit clicked();
    QWidget::mousePressEvent(e);
}

void SkinWidget::mouseDoubleClickEvent(QMouseEvent *e)
{
    if (e->button() == Qt::LeftButton)
        emit doubleClicked();
    QWidget::mouseDoubleClickEvent(e);
}
