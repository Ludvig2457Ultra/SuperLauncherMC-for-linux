#ifndef AIAGENTPAGE_H
#define AIAGENTPAGE_H

#include <QWidget>
#include <QTextEdit>
#include <QPushButton>
#include <QLabel>
#include <QVBoxLayout>
#include <QLineEdit>

class ApiClient;

class AIAgentPage : public QWidget
{
    Q_OBJECT
public:
    explicit AIAgentPage(ApiClient *client, QWidget *parent = nullptr);

private:
    void setupUi();
    void sendMessage();

    ApiClient   *m_client;
    QTextEdit   *m_chatHistory = nullptr;
    QLineEdit   *m_inputField  = nullptr;
    QPushButton *m_sendBtn     = nullptr;
};

#endif // AIAGENTPAGE_H
