#ifndef ANIMATEDBUTTON_H
#define ANIMATEDBUTTON_H

#include <QPushButton>
#include <QPropertyAnimation>
#include <QGraphicsOpacityEffect>

class AnimatedButton : public QPushButton
{
    Q_OBJECT
    Q_PROPERTY(QColor hoverColor READ hoverColor WRITE setHoverColor)
public:
    explicit AnimatedButton(const QString &text = {},
                            QWidget *parent = nullptr);

    void setDefaultStyle(const QString &style);
    void setHoverColor(const QColor &c);
    QColor hoverColor() const;

    void animateClick();

signals:
    void clicked();

protected:
    void enterEvent(QEnterEvent *event) override;
    void leaveEvent(QEvent *event) override;
    void paintEvent(QPaintEvent *event) override;

private:
    QColor m_defaultBg{60, 60, 70};
    QColor m_hoverBg{80, 80, 95};
    QColor m_currentBg{60, 60, 70};
    QColor m_textColor{220, 220, 220};
    QColor m_hoverColor{80, 80, 95};
    int m_borderRadius = 8;
    QPropertyAnimation *m_hoverAnim = nullptr;
};

#endif // ANIMATEDBUTTON_H
