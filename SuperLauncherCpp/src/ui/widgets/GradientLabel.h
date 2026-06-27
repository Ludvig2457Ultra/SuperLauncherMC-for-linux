#ifndef GRADIENTLABEL_H
#define GRADIENTLABEL_H

#include <QLabel>
#include <QLinearGradient>

class GradientLabel : public QLabel
{
    Q_OBJECT
public:
    explicit GradientLabel(const QString &text = {},
                           QWidget *parent = nullptr);

    void setGradientColors(const QColor &start, const QColor &end);
    void setGradientAngle(qreal angle);

protected:
    void paintEvent(QPaintEvent *event) override;

private:
    QColor m_gradStart{180, 130, 255};
    QColor m_gradEnd{100, 200, 255};
    qreal m_angle = 0.0;
};

#endif // GRADIENTLABEL_H
