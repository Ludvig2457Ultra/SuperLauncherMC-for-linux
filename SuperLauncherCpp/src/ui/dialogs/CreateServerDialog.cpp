#include "CreateServerDialog.h"
#include <QFormLayout>

CreateServerDialog::CreateServerDialog(QWidget *parent)
    : QDialog(parent)
{
    setupUi();
}

void CreateServerDialog::setupUi()
{
    setWindowTitle("Создание сервера");
    setFixedSize(400, 260);
    setStyleSheet("QDialog { background: #1E1E2E; }");

    auto *layout = new QVBoxLayout(this);
    layout->setContentsMargins(24, 24, 24, 24);
    layout->setSpacing(12);

    auto *title = new QLabel("Новый сервер", this);
    title->setStyleSheet("color: white; font-size: 18px; font-weight: bold;");
    layout->addWidget(title);

    auto *form = new QFormLayout();
    form->setLabelAlignment(Qt::AlignRight);

    m_name = new QLineEdit(this);
    m_name->setPlaceholderText("MyServer");
    m_name->setStyleSheet(
        "QLineEdit { background: rgba(255,255,255,0.08); color: white; "
        "border: 1px solid rgba(255,255,255,0.15); border-radius: 6px; "
        "padding: 8px; }");

    m_version = new QComboBox(this);
    m_version->addItems({"1.20.4", "1.20.1", "1.19.4", "1.18.2", "1.16.5"});
    m_version->setStyleSheet(
        "QComboBox { background: rgba(255,255,255,0.08); color: white; "
        "border: 1px solid rgba(255,255,255,0.15); border-radius: 6px; "
        "padding: 6px; }");

    m_type = new QComboBox(this);
    m_type->addItems({"vanilla", "fabric", "forge", "paper"});
    m_type->setStyleSheet(
        "QComboBox { background: rgba(255,255,255,0.08); color: white; "
        "border: 1px solid rgba(255,255,255,0.15); border-radius: 6px; "
        "padding: 6px; }");

    form->addRow("Название:", m_name);
    form->addRow("Версия:", m_version);
    form->addRow("Тип:", m_type);
    layout->addLayout(form);

    auto *btnRow = new QHBoxLayout();
    auto *createBtn = new QPushButton("Создать", this);
    createBtn->setStyleSheet(
        "QPushButton { background: #4CAF50; color: white; border: none; "
        "border-radius: 6px; padding: 8px 24px; }"
        "QPushButton:hover { background: #45a049; }");
    connect(createBtn, &QPushButton::clicked, this, &QDialog::accept);

    auto *cancelBtn = new QPushButton("Отмена", this);
    cancelBtn->setStyleSheet(
        "QPushButton { background: #555; color: white; border: none; "
        "border-radius: 6px; padding: 8px 24px; }"
        "QPushButton:hover { background: #666; }");
    connect(cancelBtn, &QPushButton::clicked, this, &QDialog::reject);

    btnRow->addStretch();
    btnRow->addWidget(cancelBtn);
    btnRow->addWidget(createBtn);
    layout->addLayout(btnRow);
}

QString CreateServerDialog::serverName() const { return m_name->text(); }
QString CreateServerDialog::mcVersion() const { return m_version->currentText(); }
QString CreateServerDialog::serverType() const { return m_type->currentText(); }
