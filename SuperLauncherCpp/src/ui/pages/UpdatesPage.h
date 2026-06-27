#ifndef UPDATESPAGE_H
#define UPDATESPAGE_H

#include <QWidget>
#include <QLabel>
#include <QPushButton>
#include <QVBoxLayout>
#include <QScrollArea>
#include <QTextBrowser>

class UpdateChecker;

class UpdatesPage : public QWidget
{
    Q_OBJECT
public:
    explicit UpdatesPage(UpdateChecker *checker, QWidget *parent = nullptr);

    void checkNow();

signals:
    void downloadRequested(const QString &url);

private:
    void setupUi();

    UpdateChecker *m_checker;
    QLabel       *m_launcherVersion = nullptr;
    QPushButton  *m_checkBtn        = nullptr;
    QPushButton  *m_downloadBtn     = nullptr;
    QTextBrowser *m_changelogViewer = nullptr;
};

#endif // UPDATESPAGE_H
