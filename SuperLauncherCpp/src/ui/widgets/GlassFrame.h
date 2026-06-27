#ifndef GLASSFRAME_H
#define GLASSFRAME_H

#include <QFrame>
#include <QPainter>
#include <QGraphicsBlurEffect>

class GlassFrame : public QFrame
{
    Q_OBJECT
public:
    explicit GlassFrame(QWidget *parent = nullptr);

    void setBlurIntensity(qreal radius);
    void setTintColor(const QColor &color);
    void setBorderRadius(int radius);
    void setBorderColor(const QColor &color);

protected:
    void paintEvent(QPaintEvent *event) override;

private:
    qreal m_blurRadius = 10.0;
    QColor m_tintColor{255, 255, 255, 30};
    int m_borderRadius = 12;
    QColor m_borderColor{255, 255, 255, 20};
};

#endif // GLASSFRAME_H
