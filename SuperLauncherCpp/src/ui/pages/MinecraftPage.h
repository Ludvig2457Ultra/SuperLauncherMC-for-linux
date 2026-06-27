#ifndef MINECRAFTPAGE_H
#define MINECRAFTPAGE_H

#include <QWidget>
#include <QComboBox>
#include <QPushButton>
#include <QTextEdit>
#include <QLabel>
#include <QVBoxLayout>
#include <QProgressBar>

class MinecraftLauncher;
class AppConfig;

class MinecraftPage : public QWidget
{
    Q_OBJECT
public:
    explicit MinecraftPage(MinecraftLauncher *launcher, AppConfig *config,
                            QWidget *parent = nullptr);

    void refreshVersions();

signals:
    void launchRequested(const QString &version, const QString &loader,
                         int minMem, int maxMem, const QString &jvmArgs);

private:
    void setupUi();

    MinecraftLauncher *m_launcher;
    AppConfig        *m_config;
    QComboBox        *m_versionCombo = nullptr;
    QComboBox        *m_loaderCombo  = nullptr;
    QPushButton      *m_launchBtn    = nullptr;
    QPushButton      *m_killBtn      = nullptr;
    QTextEdit        *m_logOutput    = nullptr;
    QProgressBar     *m_progressBar  = nullptr;
};

#endif // MINECRAFTPAGE_H
