#include "AIAgentPage.h"
#include "src/network/ApiClient.h"
#include <QHBoxLayout>
#include <QJsonObject>
#include <QScrollBar>
#include <QTextBlock>
#include <QTextCursor>

AIAgentPage::AIAgentPage(ApiClient *client, QWidget *parent)
    : QWidget(parent), m_client(client)
{
    setupUi();
}

void AIAgentPage::setupUi()
{
    auto *mainLayout = new QVBoxLayout(this);
    mainLayout->setContentsMargins(24, 24, 24, 24);

    auto *title = new QLabel("AI Агент", this);
    title->setStyleSheet("color: white; font-size: 22px; font-weight: bold;");
    mainLayout->addWidget(title);

    auto *desc = new QLabel("Помощник по установке модов, сборок и настройке серверов", this);
    desc->setStyleSheet("color: #AAAAAA; font-size: 13px;");
    desc->setWordWrap(true);
    mainLayout->addWidget(desc);

    // Chat
    m_chatHistory = new QTextEdit(this);
    m_chatHistory->setReadOnly(true);
    m_chatHistory->setStyleSheet(
        "QTextEdit { background: rgba(255,255,255,0.03); border: 1px solid "
        "rgba(255,255,255,0.08); border-radius: 8px; color: #CCCCCC; "
        "padding: 12px; font-size: 13px; }");
    m_chatHistory->setHtml("<p style='color:#888;'>AI Агент готов к работе. Задайте вопрос!</p>");
    mainLayout->addWidget(m_chatHistory, 1);

    // Input
    auto *inputRow = new QHBoxLayout();
    m_inputField = new QLineEdit(this);
    m_inputField->setPlaceholderText("Введите сообщение...");
    m_inputField->setStyleSheet(
        "QLineEdit { background: rgba(255,255,255,0.08); color: white; "
        "border: 1px solid rgba(255,255,255,0.15); border-radius: 6px; "
        "padding: 10px; font-size: 13px; }");
    connect(m_inputField, &QLineEdit::returnPressed, this, &AIAgentPage::sendMessage);

    m_sendBtn = new QPushButton("Отправить", this);
    m_sendBtn->setStyleSheet(
        "QPushButton { background: #7C4DFF; color: white; border: none; "
        "border-radius: 6px; padding: 10px 20px; }"
        "QPushButton:hover { background: #9C6DFF; }");
    connect(m_sendBtn, &QPushButton::clicked, this, &AIAgentPage::sendMessage);

    inputRow->addWidget(m_inputField, 1);
    inputRow->addWidget(m_sendBtn);
    mainLayout->addLayout(inputRow);
}

void AIAgentPage::sendMessage()
{
    QString msg = m_inputField->text().trimmed();
    if (msg.isEmpty()) return;
    m_inputField->clear();

    m_chatHistory->append("<p style='color:#7C4DFF;'><b>Вы:</b> " + msg.toHtmlEscaped() + "</p>");
    m_chatHistory->append("<p style='color:#888;'><i>AI печатает...</i></p>");

    // Scroll to bottom
    m_chatHistory->verticalScrollBar()->setValue(
        m_chatHistory->verticalScrollBar()->maximum());

    QJsonObject body;
    body["message"] = msg;
    m_client->post("https://api.example.com/ai/chat", body,
        [this](bool ok, const QJsonDocument &doc) {
            // Remove the "typing..." line
            QTextCursor cursor(m_chatHistory->document());
            cursor.movePosition(QTextCursor::End);
            cursor.select(QTextCursor::LineUnderCursor);
            if (cursor.selectedText().contains("AI печатает")) {
                cursor.removeSelectedText();
                cursor.deleteChar();
            }

            if (ok && doc.isObject()) {
                QString reply = doc.object()["reply"].toString();
                m_chatHistory->append("<p style='color:#4CAF50;'><b>AI:</b> "
                                      + reply.toHtmlEscaped() + "</p>");
            } else {
                m_chatHistory->append("<p style='color:#f44336;'><b>Ошибка:</b> "
                                      "Не удалось получить ответ</p>");
            }
        }
    );
}
