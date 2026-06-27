#ifndef NEWSPAGE_H
#define NEWSPAGE_H

#include <QWidget>
#include <QTextBrowser>
#include <QVBoxLayout>
#include <QPushButton>
#include <QComboBox>

class ApiClient;

class NewsPage : public QWidget
{
    Q_OBJECT
public:
    explicit NewsPage(ApiClient *client, QWidget *parent = nullptr);

    void loadNews(const QString &lang = "ru");

private:
    void setupUi();
    void renderNews(const QString &html);

    ApiClient    *m_client;
    QTextBrowser *m_newsViewer = nullptr;
    QComboBox    *m_langCombo  = nullptr;
    QPushButton  *m_refreshBtn = nullptr;
};

#endif // NEWSPAGE_H
