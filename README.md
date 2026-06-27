# SuperLauncher

🎮 Легкий и быстрый лаунчер Minecraft с автоматическим обновлением и полным контролем для Linux.

---

## 🚀 Особенности

- Поддерживает последнюю версию Minecraft (на релизе — 1.21.8)
- Автоматическое обновление лаунчера и Minecraft
- Создание и управление локальными серверами прямо из лаунчера
- Панель управления сервером: EULA, online/offline, старт/стоп
- Добавляйте любые серверы в список для быстрого подключения
- Ручное управление версиями Minecraft (папка `versions`)
- Ручная установка Fabric, Forge и OptiFine
- Не требует установки Java — используется `minecraft-launcher-lib`
- Минималистичный интерфейс на Qt6
- Полноценная поддержка Linux (Arch, Debian, Ubuntu, Fedora)

---

## 📁 Состав

- `superlauncher` — исполняемый файл
- `assets/title.png` — иконка лаунчера
- `~/.local/share/superlauncher/` — папка с данными

---

## 🔧 Технологии

- Python 3.10+
- PyQt6
- PyInstaller
- `minecraft-launcher-lib`

---

## 📥 Установка на Arch Linux (AUR)

```bash
yay -S superlauncher
superlauncher
