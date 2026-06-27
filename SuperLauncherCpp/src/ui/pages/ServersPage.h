#ifndef SERVERSPAGE_H
#define SERVERSPAGE_H

#include <QWidget>
#include <QVBoxLayout>
#include <QScrollArea>
#include <QList>
#include "src/models/Server.h"
#include "src/ui/widgets/ServerCardWidget.h"

class ServerManager;

class ServersPage : public QWidget
{
    Q_OBJECT
public:
    explicit ServersPage(ServerManager *mgr, QWidget *parent = nullptr);

    void refreshServers(const QString &serversBase);
    void addServerCard(const Server &server);

signals:
    void createServer(const QString &name, const QString &version,
                      const QString &type, const QString &mcDir);
    void startServer(const Server &server);
    void stopServer(const Server &server);
    void removeServer(const QString &name);

private:
    void setupUi();

    ServerManager *m_mgr;
    QVBoxLayout  *m_cardsLayout = nullptr;
    QScrollArea  *m_scrollArea  = nullptr;
    QString       m_serversBase;
};

#endif // SERVERSPAGE_H
