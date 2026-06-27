#ifndef SERVERCARDWIDGET_H
#define SERVERCARDWIDGET_H

#include <QFrame>
#include <QLabel>
#include <QPushButton>
#include "src/models/Server.h"

class ServerCardWidget : public QFrame
{
    Q_OBJECT
public:
    explicit ServerCardWidget(const Server &server, QWidget *parent = nullptr);

    Server server() const { return m_server; }
    void setServer(const Server &s);
    void setStatusRunning(bool running);

signals:
    void startClicked(const Server &server);
    void stopClicked(const Server &server);
    void configureClicked(const Server &server);
    void removeClicked(const Server &server);

private:
    void setupUi();
    void applyStyle();

    Server m_server;
    QLabel *m_nameLabel     = nullptr;
    QLabel *m_versionLabel  = nullptr;
    QLabel *m_statusLabel   = nullptr;
    QPushButton *m_startBtn = nullptr;
    QPushButton *m_stopBtn  = nullptr;
    QPushButton *m_configBtn = nullptr;
    QPushButton *m_removeBtn = nullptr;
};

#endif // SERVERCARDWIDGET_H
