#include "ServerControlDialog.h"
#include <QHBoxLayout>
#include <QGroupBox>
#include <QFormLayout>

ServerControlDialog::ServerControlDialog(const Server &server, QWidget *parent)
    : QDialog(parent), m_server(server)
{
    setupUi();
}

void ServerControlDialog::setupUi()
{
    setWindowTitle("Управление сервером - " + m_server.name);
    setMinimumSize(700, 500);
    setStyleSheet("QDialog { background: #1E1E2E; }");

    auto *mainLayout = new QVBoxLayout(this);
    mainLayout->setContentsMargins(16, 16, 16, 16);
    mainLayout->setSpacing(12);

    // Info
    auto *infoLabel = new QLabel(
        QString("%1 | %2 | %3:%4")
            .arg(m_server.name, m_server.version + " (" + m_server.type + ")",
                 m_server.ip, QString::number(m_server.port)),
        this);
    infoLabel->setStyleSheet("color: #AAAAAA; font-size: 13px;");
    mainLayout->addWidget(infoLabel);

    // Controls
    auto *ctrlGroup = new QGroupBox("Управление", this);
    ctrlGroup->setStyleSheet(
        "QGroupBox { color: white; font-size: 14px; font-weight: bold; "
        "border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; "
        "margin-top: 12px; padding-top: 16px; }"
        "QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 4px; }");
    auto *ctrlLayout = new QVBoxLayout(ctrlGroup);

    auto *ramRow = new QHBoxLayout();
    auto *ramLabel = new QLabel("RAM (MB):", ctrlGroup);
    ramLabel->setStyleSheet("color: #AAAAAA; font-weight: normal;");
    m_ramSpinner = new QSpinBox(ctrlGroup);
    m_ramSpinner->setRange(1024, 32768);
    m_ramSpinner->setValue(2048);
    m_ramSpinner->setSuffix(" MB");
    m_ramSpinner->setStyleSheet(
        "QSpinBox { background: rgba(255,255,255,0.08); color: white; "
        "border: 1px solid rgba(255,255,255,0.15); border-radius: 4px; "
        "padding: 4px; }");
    ramRow->addWidget(ramLabel);
    ramRow->addWidget(m_ramSpinner);
    ramRow->addStretch();

    auto *javaRow = new QHBoxLayout();
    auto *javaLabel = new QLabel("JVM args:", ctrlGroup);
    javaLabel->setStyleSheet("color: #AAAAAA; font-weight: normal;");
    m_javaArgs = new QLineEdit(ctrlGroup);
    m_javaArgs->setPlaceholderText("-XX:+UseG1GC");
    m_javaArgs->setStyleSheet(
        "QLineEdit { background: rgba(255,255,255,0.08); color: white; "
        "border: 1px solid rgba(255,255,255,0.15); border-radius: 4px; "
        "padding: 6px; }");
    javaRow->addWidget(javaLabel);
    javaRow->addWidget(m_javaArgs, 1);

    auto *btnRow = new QHBoxLayout();
    m_startBtn = new QPushButton("Запустить", ctrlGroup);
    m_startBtn->setStyleSheet(
        "QPushButton { background: #4CAF50; color: white; border: none; "
        "border-radius: 4px; padding: 8px 20px; }"
        "QPushButton:hover { background: #45a049; }");
    connect(m_startBtn, &QPushButton::clicked, this, &ServerControlDialog::startRequested);

    m_stopBtn = new QPushButton("Остановить", ctrlGroup);
    m_stopBtn->setStyleSheet(
        "QPushButton { background: #f44336; color: white; border: none; "
        "border-radius: 4px; padding: 8px 20px; }"
        "QPushButton:hover { background: #da190b; }");
    connect(m_stopBtn, &QPushButton::clicked, this, &ServerControlDialog::stopRequested);

    m_restartBtn = new QPushButton("Перезапустить", ctrlGroup);
    m_restartBtn->setStyleSheet(
        "QPushButton { background: #FF9800; color: white; border: none; "
        "border-radius: 4px; padding: 8px 20px; }"
        "QPushButton:hover { background: #F57C00; }");
    connect(m_restartBtn, &QPushButton::clicked, this, &ServerControlDialog::restartRequested);

    btnRow->addWidget(m_startBtn);
    btnRow->addWidget(m_stopBtn);
    btnRow->addWidget(m_restartBtn);
    btnRow->addStretch();

    ctrlLayout->addLayout(ramRow);
    ctrlLayout->addLayout(javaRow);
    ctrlLayout->addLayout(btnRow);
    mainLayout->addWidget(ctrlGroup);

    // Console
    auto *consoleLabel = new QLabel("Консоль", this);
    consoleLabel->setStyleSheet("color: white; font-size: 14px; font-weight: bold;");
    mainLayout->addWidget(consoleLabel);

    m_console = new QTextEdit(this);
    m_console->setReadOnly(true);
    m_console->setStyleSheet(
        "QTextEdit { background: rgba(0,0,0,0.4); border: 1px solid "
        "rgba(255,255,255,0.08); border-radius: 8px; color: #00FF00; "
        "font-family: 'Consolas', 'Courier New'; font-size: 11px; "
        "padding: 8px; }");
    mainLayout->addWidget(m_console, 1);

    // Close
    auto *closeBtn = new QPushButton("Закрыть", this);
    closeBtn->setStyleSheet(
        "QPushButton { background: #555; color: white; border: none; "
        "border-radius: 4px; padding: 8px 20px; }"
        "QPushButton:hover { background: #666; }");
    connect(closeBtn, &QPushButton::clicked, this, &QDialog::accept);
    mainLayout->addWidget(closeBtn);
}

int ServerControlDialog::ramMB() const { return m_ramSpinner->value(); }
QString ServerControlDialog::javaArgs() const { return m_javaArgs->text(); }

void ServerControlDialog::appendLog(const QString &line)
{
    m_console->append(line);
}
