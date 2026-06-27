#ifndef LOGINDIALOG_H
#define LOGINDIALOG_H

#include <QDialog>
#include <QLineEdit>
#include <QPushButton>
#include <QVBoxLayout>
#include <QLabel>
#include <QCheckBox>

class LoginDialog : public QDialog
{
    Q_OBJECT
public:
    explicit LoginDialog(QWidget *parent = nullptr);

    QString username() const;
    QString password() const;
    bool rememberMe() const;

private:
    void setupUi();

    QLineEdit  *m_username = nullptr;
    QLineEdit  *m_password = nullptr;
    QCheckBox  *m_remember = nullptr;
    QPushButton*m_loginBtn = nullptr;
};

#endif // LOGINDIALOG_H
