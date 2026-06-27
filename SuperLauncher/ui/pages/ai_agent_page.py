import threading
import requests
import random
import json
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                              QTextEdit, QListWidget, QListWidgetItem, QLineEdit, QComboBox)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QObject
from PyQt6.QtGui import QColor

OLLAMA_DEFAULT = "http://localhost:11434/v1"


class SignalBridge(QObject):
    append = pyqtSignal(str, str)


class AIAgentPage(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.bridge = SignalBridge()
        self.bridge.append.connect(self._on_append)
        self._quantum = False
        self._quantum_timer = None

        font_style = "color: white;"
        input_style = "QLineEdit { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; padding: 6px; color: white; }"
        label_style = "color: #aaa; font-size: 12px;"

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)

        title_row = QHBoxLayout()
        t = QLabel("AI Агент")
        t.setStyleSheet("font-size: 26px; font-weight: bold; color: white;")
        title_row.addWidget(t)

        self.quantum_btn = QPushButton("🧪 Квантовый режим")
        self.quantum_btn.setCheckable(True)
        self.quantum_btn.setFixedHeight(32)
        self.quantum_btn.setStyleSheet(
            "QPushButton { background: rgba(100,60,200,0.2); border: 1px solid #643cc8; "
            "border-radius: 14px; padding: 4px 14px; color: #b088ff; font-size: 11px; }"
            "QPushButton:checked { background: rgba(100,60,200,0.5); color: #d0bbff; }")
        self.quantum_btn.clicked.connect(self._toggle_quantum)
        title_row.addStretch()
        title_row.addWidget(self.quantum_btn)
        layout.addLayout(title_row)

        # Connection row
        conn = QHBoxLayout()
        conn.addWidget(QLabel("Endpoint:", styleSheet=label_style))
        self.api_url = QLineEdit(main.config.get("ai_api_url", OLLAMA_DEFAULT))
        self.api_url.setStyleSheet(input_style)
        conn.addWidget(self.api_url)

        self.model_box = QComboBox()
        self.model_box.setEditable(True)
        self.model_box.setStyleSheet(
            "QComboBox { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); "
            "border-radius: 6px; padding: 6px; color: white; }"
            "QComboBox QAbstractItemView { background: #1a1a2e; color: white; border: 1px solid rgba(255,255,255,0.1); }")
        self.model_box.addItems(["llama3.2:latest", "mistral:latest", "codellama:latest", "qwen2.5:latest"])
        conn.addWidget(self.model_box)

        scan_btn = QPushButton("Scan")
        scan_btn.setFixedWidth(50)
        scan_btn.setStyleSheet("QPushButton { background: rgba(79,172,254,0.2); border: none; border-radius: 6px; color: #4facfe; font-size: 11px; } QPushButton:hover { background: rgba(79,172,254,0.3); }")
        scan_btn.clicked.connect(self._scan_ollama)
        conn.addWidget(scan_btn)
        layout.addLayout(conn)

        # Chat
        self.chat = QListWidget()
        self.chat.setStyleSheet(
            "QListWidget { background: rgba(0,0,0,0.15); border: 1px solid rgba(255,255,255,0.05); "
            "border-radius: 8px; padding: 4px; }"
            "QListWidget::item { padding: 8px; border-bottom: 1px solid rgba(255,255,255,0.03); color: #ccc; }")
        layout.addWidget(self.chat, 1)

        # Input
        inp_row = QHBoxLayout()
        self.input = QTextEdit()
        self.input.setMaximumHeight(60)
        self.input.setPlaceholderText("Спроси у ИИ...")
        self.input.setStyleSheet(
            "QTextEdit { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); "
            "border-radius: 8px; padding: 8px; color: white; }")
        inp_row.addWidget(self.input, 1)

        send_btn = QPushButton("➤")
        send_btn.setFixedSize(44, 44)
        send_btn.setStyleSheet(
            "QPushButton { background: #4facfe; border: none; border-radius: 10px; font-size: 18px; color: white; }"
            "QPushButton:hover { background: #6db8ff; }")
        send_btn.clicked.connect(self._send)
        inp_row.addWidget(send_btn)
        layout.addLayout(inp_row)

        self._add_msg("system", "AI готов. Ollama: " + self.api_url.text().strip())

    def _add_msg(self, role, text):
        prefix = "🧠 AI:" if role == "ai" else ("👤 Вы:" if role == "user" else "⚡")
        item = QListWidgetItem(f"{prefix} {text}")
        if role == "ai":
            item.setForeground(QColor(180, 200, 255))
        elif role == "user":
            item.setForeground(QColor(200, 220, 200))
        self.chat.addItem(item)
        self.chat.scrollToBottom()

    def _on_append(self, role, text):
        self._add_msg(role, text)

    def _send(self):
        text = self.input.toPlainText().strip()
        if not text:
            return
        self.input.clear()
        self._add_msg("user", text)
        self._add_msg("ai", "Думаю...")

        if self._quantum:
            text = self._quantumify(text)

        url = self.api_url.text().strip().rstrip("/") + "/chat/completions"
        model = self.model_box.currentText().strip()

        def task():
            try:
                headers = {"Content-Type": "application/json"}
                if "openai" in url and "localhost" not in url:
                    k = self.main.config.get("ai_api_key", "")
                    if k:
                        headers["Authorization"] = f"Bearer {k}"
                payload = {"model": model,
                           "messages": [{"role": "user", "content": text}],
                           "max_tokens": 1024, "temperature": 0.7}
                r = requests.post(url, headers=headers, json=payload, timeout=120)
                r.raise_for_status()
                content = r.json()["choices"][0]["message"]["content"]
                self.bridge.append.emit("ai", content[:500])
            except requests.exceptions.ConnectionError:
                self.bridge.append.emit("ai", "Ошибка: Ollama не запущен. Запусти `ollama serve`")
            except Exception as e:
                self.bridge.append.emit("ai", f"Ошибка: {str(e)[:120]}")

        threading.Thread(target=task, daemon=True).start()

    def _scan_ollama(self):
        def task():
            try:
                base = self.api_url.text().strip().rstrip("/")
                if "/v1" in base:
                    base = base[:base.index("/v1")]
                r = requests.get(base.rstrip("/") + "/api/tags", timeout=5)
                if r.status_code == 200:
                    models = [m["name"] for m in r.json().get("models", [])]
                    if models:
                        self.model_box.clear()
                        self.model_box.addItems(models)
                        self.bridge.append.emit("system", f"Найдено моделей: {', '.join(models[:5])}{'...' if len(models) > 5 else ''}")
                    else:
                        self.bridge.append.emit("system", "Модели не найдены. Запусти `ollama pull llama3.2`")
                else:
                    self.bridge.append.emit("system", f"Ollama ответил кодом {r.status_code}")
            except Exception as e:
                self.bridge.append.emit("system", f"Ollama недоступен ({str(e)[:60]}). Убедись что ollama запущен")
        threading.Thread(target=task, daemon=True).start()

    def _toggle_quantum(self, checked):
        self._quantum = checked
        if checked:
            self.quantum_btn.setText("🔮 Квантовый: ВКЛ")
            self._start_quantum_effect()
        else:
            self.quantum_btn.setText("🧪 Квантовый режим")
            if self._quantum_timer:
                self._quantum_timer.stop()
                self._quantum_timer = None

    def _start_quantum_effect(self):
        self._quantum_timer = QTimer(self)
        self._quantum_timer.timeout.connect(self._quantum_flash)
        self._quantum_timer.start(2000)

    def _quantum_flash(self):
        states = [
            "🌀 Суперпозиция: лаунчер одновременно открыт и закрыт",
            "⚛️ Квантовая запутанность: версия майнкрафта зависит от наблюдения",
            "🔬 Эффект наблюдателя: моды загружаются только если на них смотреть",
            "🌌 Туннелирование: скин проходит сквозь текстуры",
            "🧬 Квантовый спавн: игрок появляется во всех чанках сразу",
            "⚡ Планковская частота: тиков в секунду — 10⁴³",
            "🌀 Декогеренция: мир схлопнулся в волновую функцию",
            "🔮 Квантовый бит: текст = 0 и 1 одновременно",
        ]
        self._add_msg("system", random.choice(states))

    def _quantumify(self, text):
        prefixes = [
            "Представь что ты квантовый компьютер и ", "В контексте квантовой суперпозиции, ",
            "С точки зрения многомировой интерпретации, ", "Если рассматривать нелокальность Эйнштейна-Подольского-Розена, ",
        ]
        suffixes = [
            " в квантовом состоянии", " с учётом планковской длины", " в параллельной вселенной",
        ]
        return random.choice(prefixes) + text + random.choice(suffixes)
