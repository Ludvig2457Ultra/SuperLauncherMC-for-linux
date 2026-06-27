#ifndef SKINWIDGET_H
#define SKINWIDGET_H

#include <QWidget>
#include <QPixmap>
#include <QString>

class SkinWidget : public QWidget
{
    Q_OBJECT
public:
    explicit SkinWidget(QWidget *parent = nullptr);

    void setSkin(const QPixmap &pixmap);
    void setSkinPath(const QString &path);
    void setZoom(qreal factor);
    void setShowPreview(bool show);
    void setLabel(const QString &text);

    QPixmap skin() const;
    QString skinPath() const;

signals:
    void clicked();
    void doubleClicked();

protected:
    void paintEvent(QPaintEvent *event) override;
    void mousePressEvent(QMouseEvent *event) override;
    void mouseDoubleClickEvent(QMouseEvent *event) override;

private:
    QPixmap m_skin;
    QString m_skinPath;
    QString m_label;
    qreal m_zoom = 1.0;
    bool m_showPreview = true;
};

#endif // SKINWIDGET_H
