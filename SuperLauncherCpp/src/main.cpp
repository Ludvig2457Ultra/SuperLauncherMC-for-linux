#include <QApplication>
#include <QIcon>
#include <QFile>
#include <QDir>
#include "ui/MainWindow.h"

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    app.setApplicationName("SuperLauncher");
    app.setApplicationVersion("2.0.0");

    if (QFile::exists("assets/icon.png"))
        app.setWindowIcon(QIcon("assets/icon.png"));

    MainWindow window;
    window.show();

    return app.exec();
}
