#ifndef HOMEPAGE_H
#define HOMEPAGE_H

#include <QWidget>
#include <QLabel>
#include <QPushButton>
#include <QVBoxLayout>

class HomePage : public QWidget
{
    Q_OBJECT
public:
    explicit HomePage(QWidget *parent = nullptr);

signals:
    void playClicked();
    void openAccount();
    void openNews();

private:
    void setupUi();
    QLabel *m_titleLabel     = nullptr;
    QLabel *m_welcomeLabel   = nullptr;
    QLabel *m_statusLabel    = nullptr;
    QPushButton *m_playBtn   = nullptr;
};

#endif // HOMEPAGE_H
