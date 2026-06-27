#ifndef SERVERCONTROLDIALOG_H
#define SERVERCONTROLDIALOG_H

#include <QDialog>
#include <QTextEdit>
#include <QPushButton>
#include <QVBoxLayout>
#include <QSpinBox>
#include <QLabel>
#include <QLineEdit>
#include "src/models/Server.h"

class ServerControlDialog : public QDialog
{
    Q_OBJECT
public:
    explicit ServerControlDialog(const Server &server, QWidget *parent = nullptr);

    int ramMB() const;
    QString javaArgs() const;

signals:
    void startRequested();
    void stopRequested();
    void restartRequested();

private:
    void setupUi();
    void appendLog(const QString &line);

    Server     m_server;
    QTextEdit *m_console  = nullptr;
    QSpinBox  *m_ramSpinner = nullptr;
    QLineEdit *m_javaArgs  = nullptr;
    QPushButton *m_startBtn = nullptr;
    QPushButton *m_stopBtn  = nullptr;
    QPushButton *m_restartBtn = nullptr;
};

#endif // SERVERCONTROLDIALOG_H
