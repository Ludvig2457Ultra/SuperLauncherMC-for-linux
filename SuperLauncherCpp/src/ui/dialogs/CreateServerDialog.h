#ifndef CREATESERVERDIALOG_H
#define CREATESERVERDIALOG_H

#include <QDialog>
#include <QLineEdit>
#include <QComboBox>
#include <QPushButton>
#include <QVBoxLayout>
#include <QLabel>

class CreateServerDialog : public QDialog
{
    Q_OBJECT
public:
    explicit CreateServerDialog(QWidget *parent = nullptr);

    QString serverName() const;
    QString mcVersion() const;
    QString serverType() const;

private:
    void setupUi();

    QLineEdit  *m_name    = nullptr;
    QComboBox  *m_version = nullptr;
    QComboBox  *m_type    = nullptr;
};

#endif // CREATESERVERDIALOG_H
