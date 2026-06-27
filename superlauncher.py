import sys
import os
import json
import subprocess
import threading
import time
import datetime
import hashlib
import secrets
import platform
import shutil
import zipfile
import tempfile
import base64
import urllib.parse
import webbrowser
import random
import re
import math
from pathlib import Path
from typing import Optional, Dict, List, Tuple, Any, Union
from uuid import uuid1
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Fix console encoding for Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Внешние библиотеки
import requests
from packaging import version as packaging_version
from tqdm import tqdm
from pypresence import Presence
from random_username.generate import generate_username

# Дополнительные библиотеки (опционально)
try:
    from cryptography.fernet import Fernet
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    print("⚠️ Шифрование отключено (cryptography не установлен)")

try:
    import jwt
    JWT_AVAILABLE = True
except ImportError:
    JWT_AVAILABLE = False
    print("⚠️ JWT отключен (PyJWT не установлен)")

# Minecraft библиотеки
from minecraft_launcher_lib.utils import get_minecraft_directory, get_version_list
from minecraft_launcher_lib.install import install_minecraft_version
from minecraft_launcher_lib.command import get_minecraft_command
from minecraft_launcher_lib import fabric as fabric_loader
from minecraft_launcher_lib import forge as forge_loader
from minecraft_launcher_lib import quilt as quilt_loader
# neoforge пока недоступен в этой версии minecraft_launcher_lib

# =========== PYQT6 ИМПОРТЫ ===========

# PyQt6 Core - ОСНОВНЫЕ
from PyQt6.QtCore import (
    Qt, QThread, pyqtSignal, QSize, QTimer, QPropertyAnimation, 
    QEasingCurve, pyqtProperty, QUrl, QDateTime, QTime, QDate, 
    QRect, QRectF, QPoint, QPointF, QModelIndex,
    QObject, QEvent, QMargins,
    QByteArray, QBuffer, QIODevice, QLibraryInfo, QLocale,
    QSettings, QVariant, QMetaObject, QRunnable, QThreadPool,
    QProcess, QProcessEnvironment, QStandardPaths, QDir, QFile, QFileInfo,
    QTextStream, QDataStream, QCoreApplication,
    QRegularExpression  # Для регулярных выражений
)

# PyQt6 Widgets - ОСНОВНЫЕ ВИДЖЕТЫ
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFrame, QStackedWidget, QButtonGroup,
    QLineEdit, QComboBox, QProgressBar, QSpacerItem, QSizePolicy,
    QMessageBox, QScrollArea, QDialog, QCheckBox, QFormLayout,
    QListWidget, QListWidgetItem, QRadioButton, QFileDialog, QTextBrowser, QScrollBar,
    QGridLayout, QGroupBox, QTabWidget, QProgressDialog
)

# PyQt6 GUI - ОСНОВНЫЕ
from PyQt6.QtGui import (
    QPixmap, QCursor, QIcon, QPainter, QBrush, QPen, 
    QLinearGradient, QColor, QFont, QFontDatabase, QFontMetrics,
    QRadialGradient, QConicalGradient, QGradient, QImage,
    QPalette, QPainterPath, QKeySequence, QAction, QMovie,
    QTextCursor, QTextCharFormat, QTextFormat, QTextDocument,
    QTextOption, QTextBlockFormat, QTextLength,
    QBitmap, QRegion, QTransform, QPolygon, QPolygonF,
    QGuiApplication, QScreen, QClipboard, QDrag,
    QStandardItemModel, QStandardItem
)

# Валидаторы из QtGui (правильное место в PyQt6)
from PyQt6.QtGui import QValidator, QIntValidator, QDoubleValidator, QRegularExpressionValidator

# =========== ОПЦИОНАЛЬНЫЕ ИМПОРТЫ ===========

# Дополнительные виджеты
try:
    from PyQt6.QtWidgets import (
        QTreeWidget, QTableWidget, QSplitter, QToolBar, QMenuBar, 
        QStatusBar, QToolButton, QHeaderView, QStyleFactory, QInputDialog,
        QColorDialog, QFontDialog, QSlider, QSpinBox, QDoubleSpinBox,
        QTextEdit, QPlainTextEdit, QCompleter, QSystemTrayIcon, QMenu
    )
    EXTRA_WIDGETS = True
except ImportError:
    EXTRA_WIDGETS = False
    print("⚠️ Дополнительные виджеты не доступны")

# Дополнительные GUI элементы
try:
    from PyQt6.QtGui import (
        QVector2D, QVector3D, QVector4D, QMatrix4x4,
        QSurfaceFormat, QOpenGLContext, QOpenGLFunctions
    )
    EXTRA_GUI = True
except ImportError:
    EXTRA_GUI = False
    print("⚠️ 3D графика не доступна")

# Сортировка и фильтрация
try:
    from PyQt6.QtCore import QSortFilterProxyModel, QAbstractItemModel
    SORTING_AVAILABLE = True
except ImportError:
    SORTING_AVAILABLE = False
    print("⚠️ Сортировка моделей не доступна")

# Мультимедиа
try:
    from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
    MULTIMEDIA_AVAILABLE = True
except ImportError:
    MULTIMEDIA_AVAILABLE = False
    print("⚠️ Мультимедиа отключено")

# Сеть
try:
    from PyQt6.QtNetwork import (
        QNetworkAccessManager, QNetworkRequest, QNetworkReply
    )
    NETWORK_AVAILABLE = True
except ImportError:
    NETWORK_AVAILABLE = False
    print("⚠️ Сетевые функции ограничены")

# WebEngine
try:
    from PyQt6.QtWebEngineWidgets import QWebEngineView
    WEBENGINE_AVAILABLE = True
except ImportError:
    WEBENGINE_AVAILABLE = False
    print("⚠️ WebEngine отключен")

# Charts
try:
    from PyQt6.QtCharts import QChart, QChartView, QLineSeries
    CHARTS_AVAILABLE = True
except ImportError:
    CHARTS_AVAILABLE = False
    print("⚠️ Графики отключены")

# Pillow для изображений
try:
    from PIL import Image
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False
    print("⚠️ Обработка изображений ограничена")

# Мониторинг ресурсов
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("⚠️ Мониторинг ресурсов отключен")

# Уведомления Windows
try:
    from win10toast import ToastNotifier
    TOAST_AVAILABLE = True
except ImportError:
    TOAST_AVAILABLE = False
    print("⚠️ Уведомления Windows отключены")
# =========== КОНСТАНТЫ ===========

CONFIG_FILE = "settings.json"
ACCOUNTS_FILE = "accounts.json"
LICENSES_FILE = "licenses.json"
GIFTS_FILE = "gifts.json"
UI_SETTINGS_FILE = "ui_settings.json"
SERVERS_FILE = "servers_list.json"
CURRENT_VERSION = "v3.0.0"
MODRINTH_API = "https://api.modrinth.com/v2"
INSTANCES_FILE = "user_data/instances.json"
INSTANCES_DIR = "user_data/instances"

# =========== ИНИЦИАЛИЗАЦИЯ ===========

# Получаем путь Minecraft
try:
    minecraft_directory = get_minecraft_directory()
    print(f"🎮 Путь к Minecraft: {minecraft_directory}")
    
    if not os.path.exists(minecraft_directory):
        print("📁 Создаю папку Minecraft...")
        os.makedirs(minecraft_directory, exist_ok=True)
    
except Exception as e:
    print(f"⚠️ Ошибка: {e}")
    # Резервный путь
    if platform.system() == "Windows":
        minecraft_directory = os.path.join(os.getenv('APPDATA'), '.minecraft')
    elif platform.system() == "Darwin":
        minecraft_directory = os.path.expanduser("~/Library/Application Support/minecraft")
    else:
        minecraft_directory = os.path.expanduser("~/.minecraft")
    
    os.makedirs(minecraft_directory, exist_ok=True)
    print(f"📁 Использую резервный путь: {minecraft_directory}")

# Создаем профиль если нужно
profile_path = os.path.join(minecraft_directory, 'launcher_profiles.json')
if not os.path.isfile(profile_path):
    print("📄 Создаю launcher_profiles.json...")
    empty_profile = {
        "profiles": {},
        "settings": {},
        "selectedProfile": None
    }
    with open(profile_path, 'w', encoding='utf-8') as f:
        json.dump(empty_profile, f, indent=4)

# Создаем папки
folders = [
    "assets/skins", "assets/icons",
    "user_data", "servers", "builds", "mods_cache", "logs", "temp"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

print(f"✅ SuperLauncher {CURRENT_VERSION} готов к запуску!")
print(f"📊 PyQt6 виджеты: {'✅' if EXTRA_WIDGETS else '⚠️'}")
print(f"🎵 Мультимедиа: {'✅' if MULTIMEDIA_AVAILABLE else '⚠️'}")
print(f"🌐 WebEngine: {'✅' if WEBENGINE_AVAILABLE else '⚠️'}")
print(f"📊 Графики: {'✅' if CHARTS_AVAILABLE else '⚠️'}")
print("=" * 50)

translations = {
    "ru": {
        # --- SettingsPage ---
        "Theme:": "Тема:",
        "Language:": "Язык:",
        "Minecraft launch mode:": "Способ запуска Minecraft:",
        "minecraft-launcher-lib (default)": "minecraft-launcher-lib (по умолчанию)",
        "Java (specify path)": "Java (указать путь)",
        "Java path (if Java is selected):": "Путь к Java (если выбран Java):",
        "Browse Java path": "Выбрать путь к Java",
        "Page backgrounds:": "Фоны страниц:",
        "Save settings": "Сохранить настройки",
        "Export settings": "📤 Экспорт настроек",
        "Import settings": "📥 Импорт настроек",
        "Auto-detect": "🔍 Авто-поиск",
        "Download Java": "⬇ Скачать Java",
        "RAM allocation:": "Выделение ОЗУ:",
        "JVM arguments:": "JVM аргументы:",
        "Accent color": "🎨 Цвет акцента",
        "RAM Boost": "⚡ Очистка RAM",
        "Minimize to tray": "🔽 Сворачивать в трей",
        "Launch with Windows": "🚀 Запуск с Windows",
        "Test Java": "🧪 Проверить Java",
        "Test Notification": "🔔 Тест уведомления",
        "Reset Config": "⚠️ Сбросить настройки",
        "Select Background Image": "🖼 Выбрать фон",

        # --- MinecraftPage ---
        "Play": "Играть",
        "Username": "Имя пользователя",
        "No versions available": "Версии недоступны",

        # --- ModsPage ---
        "Mods from": "Моды из",
        "Modrinth": "Modrinth",
        "CurseForge": "CurseForge",
        "Select file:": "Выберите файл:",
        "Search mod...": "Найти мод...",
        "Open mods folder": "Открыть папку модов",
        "Delete all mods": "Удалить все моды",
        "Error": "Ошибка",
        "Downloading mod": "Загрузка мода",
        "Done": "Готово",
        "All mods deleted": "Удалено модов",
        "No available versions": "Нет доступных версий",
        "No supported builds": "Нет поддерживаемых билдов",
        "File not found": "Файл не найден",
        "Install mod": "Установка мода",
        "Minecraft version and loader:": "Версия Minecraft и ядро:",

        # --- NewsPage ---
        "News": "Новости",
        "2025-08-12 v1.4.0.7: Discord RPC added": "2025-08-12 v1.4.0.7: Добавлен Discord RPC",
        "2025-07-24 v1.4.0.5: Added support for downloading mods from Modrind and launcher settings": "2025-07-24 v1.4.0.5: Добавлена поддержка скачивания модов из Modrind и настроек лаунчера",
        "2025-07-23 v1.4.0.4: Added ability to create and manage local Minecraft servers directly from the launcher...": "2025-07-23 v1.4.0.4: Добавлена возможность создавать и управлять локальными Minecraft-серверами прямо из лаунчера...",
        "2025-07-23 v1.4.0.3: New design added and code restored": "2025-07-23 v1.4.0.3: Добавлен новый дизайн и восстановлен код",
        "2025-06-26 v1.4.0.2: New design added, but code lost": "2025-06-26 v1.4.0.2: Добавлен новый дизайн, но утерян код",
        "2025-06-26 v1.4.0.1: Bugs fixed, but design outdated": "2025-06-26 v1.4.0.1: Исправлены баги, но дизайн устаревший",
        "2025-06-26 v1.4.0.0: Bugs fixed, but design outdated": "2025-06-26 v1.4.0.0: Исправлены баги, но дизайн устаревший",
        "2025-06-26 v1.3: Launcher will exit beta in the next release": "2025-06-26 v1.3: Лаунчер выйдет из бета в следующем релизе",
        "CurseForge API Key:": "CurseForge API Ключ:",
        "Test key": "Проверить ключ",
        "No news available": "Новости недоступны",

        # --- HomePage ---
        "Welcome to SuperLauncher!": "Добро пожаловать в SuperLauncher!",

        # --- ServersPage ---
        "🖧 Minecraft Servers": "🖧 Серверы Minecraft",
        "Create your own server": "Создать свой сервер",
        "Server Name": "Имя сервера",
        "IP or domain": "IP или домен",
        "Add server": "Добавить сервер",
        "Manage": "Управление",
        "Delete": "Удалить",
        "Delete confirmation": "Подтверждение удаления",
        "Are you sure you want to delete the server '{server_name}'? This action cannot be undone.": "Вы уверены, что хотите удалить сервер '{server_name}'? Это действие нельзя отменить.",
        "Folder in use": "Папка занята",
        "Cannot delete folder because it is used by the following processes:\n{proc_names}\n\nDo you want to terminate them and try again?": "Не удалось удалить папку, так как её используют процессы:\n{proc_names}\n\nХотите завершить эти процессы и попробовать снова?",
        "Terminate processes": "Завершить процессы",
        "Cancel": "Отмена",
        "Success": "Успех",
        "Folder successfully deleted after terminating processes.": "Папка успешно удалена после завершения процессов.",
        "Failed to delete folder:\n{error}": "Не удалось удалить папку:\n{error}",
        "Deletion canceled.": "Удаление папки отменено.",
        "Please fill in the server name and IP.": "Пожалуйста, заполните имя и IP сервера.",

        # --- ServerControlPanel ---
        "Settings": "Настройки",
        "I accept the EULA": "Я принимаю лицензионное соглашение EULA",
        "Enable offline mode (cracked)": "Включить оффлайн режим (пиратка)",
        "Use playit.gg (tunnel)": "Использовать playit.gg (туннель)",
        "Control": "Управление",
        "Start server": "Запустить сервер",
        "Stop server": "Остановить сервер",
        "You must accept the EULA!": "Вы должны принять лицензионное соглашение EULA!",
        "Managing server: ": "Управление сервером: ",
        "Manage server": "Управление сервером",
        "Server started.": "Сервер запущен.",
        "Server stopped.": "Сервер остановлен.",
        "Server is already running.": "Сервер уже запущен.",
        "Server is not running.": "Сервер не запущен.",
        "Server forcefully stopped.": "Сервер принудительно остановлен.",

        # --- CreateServerDialog ---
        "Create your own server": "Создать свой сервер Minecraft",
        "Port": "Порт",
        "Version": "Версия",
        "Core": "Ядро",
        "Create": "Создать",
        "Please enter a valid server name and port (number).": "Пожалуйста, введите корректное имя и порт (число).",
        "RAM (GB):": "ОЗУ (ГБ):",
        "Console": "Консоль",
        "Plugins": "Плагины",
        "Backup": "Бэкап",
        "Search": "Поиск",
        "Install": "Установить",
        "Uninstall": "Удалить",
        "Open folder": "Открыть папку",
        "Server console": "Консоль сервера",
        "Enter command...": "Введите команду...",
        "Send": "Отправить",
        "Online mode": "Online-mode",
        "Offline mode": "Оффлайн режим",
        "Max players": "Макс. игроков",
        "MOTD": "MOTD",
        "Create Backup": "Создать бэкап",
        "Restore": "Восстановить",
        "Backup created": "Бэкап создан",
        "Backup restored": "Бэкап восстановлен",
        "Downloading plugin...": "Загрузка плагина...",
        "Plugin installed": "Плагин установлен",
        "Search plugins...": "Поиск плагинов...",
        "No plugins found": "Плагины не найдены",
        "Backups": "Бэкапы",
        "Restore backup": "Восстановить бэкап",
        "Are you sure?": "Вы уверены?",
        "Install plugin": "Установка плагина",
        "Error": "Ошибка"
    },

    "en": {
        # --- SettingsPage ---
        "Theme:": "Theme:",
        "Language:": "Language:",
        "Minecraft launch mode:": "Minecraft launch mode:",
        "minecraft-launcher-lib (default)": "minecraft-launcher-lib (default)",
        "Java (specify path)": "Java (specify path)",
        "Java path (if Java is selected):": "Java path (if Java is selected):",
        "Browse Java path": "Browse Java path",
        "Page backgrounds:": "Page backgrounds:",
        "Save settings": "Save settings",
        "RAM allocation:": "RAM allocation:",
        "JVM arguments:": "JVM arguments:",

        # --- MinecraftPage ---
        "Play": "Play",
        "Username": "Username",
        "No versions available": "No versions available",

        # --- ModsPage ---
        "Mods from": "Mods from",
        "Modrinth": "Modrinth",
        "CurseForge": "CurseForge",
        "Select file:": "Select file:",
        "Search mod...": "Search mod...",
        "Open mods folder": "Open mods folder",
        "Delete all mods": "Delete all mods",
        "Error": "Error",
        "Downloading mod": "Downloading mod",
        "Done": "Done",
        "All mods deleted": "All mods deleted",
        "No available versions": "No available versions",
        "No supported builds": "No supported builds",
        "File not found": "File not found",
        "Install mod": "Install mod",
        "Minecraft version and loader:": "Minecraft version and loader:",

        # --- NewsPage ---
        "News": "News",
        "2025-08-12 v1.4.0.7: Discord RPC added": "2025-08-12 v1.4.0.7: Discord RPC added",
        "2025-07-24 v1.4.0.5: Added support for downloading mods from Modrind and launcher settings": "2025-07-24 v1.4.0.5: Added support for downloading mods from Modrind and launcher settings",
        "2025-07-23 v1.4.0.4: Added ability to create and manage local Minecraft servers directly from the launcher...": "2025-07-23 v1.4.0.4: Added ability to create and manage local Minecraft servers directly from the launcher...",
        "2025-07-23 v1.4.0.3: New design added and code restored": "2025-07-23 v1.4.0.3: New design added and code restored",
        "2025-06-26 v1.4.0.2: New design added, but code lost": "2025-06-26 v1.4.0.2: New design added, but code lost",
        "2025-06-26 v1.4.0.1: Bugs fixed, but design outdated": "2025-06-26 v1.4.0.1: Bugs fixed, but design outdated",
        "2025-06-26 v1.4.0.0: Bugs fixed, but design outdated": "2025-06-26 v1.4.0.0: Bugs fixed, but design outdated",
        "2025-06-26 v1.3: Launcher will exit beta in the next release": "2025-06-26 v1.3: Launcher will exit beta in the next release",
        "No news available": "No news available",

        # --- HomePage ---
        "Welcome to SuperLauncher!": "Welcome to SuperLauncher!",

        # --- ServersPage ---
        "🖧 Minecraft Servers": "🖧 Minecraft Servers",
        "Create your own server": "Create your own server",
        "Server Name": "Server Name",
        "IP or domain": "IP or domain",
        "Add server": "Add server",
        "Manage": "Manage",
        "Delete": "Delete",
        "Delete confirmation": "Delete confirmation",
        "Are you sure you want to delete the server '{server_name}'? This action cannot be undone.": "Are you sure you want to delete the server '{server_name}'? This action cannot be undone.",
        "Folder in use": "Folder in use",
        "Cannot delete folder because it is used by the following processes:\n{proc_names}\n\nDo you want to terminate them and try again?": "Cannot delete folder because it is used by the following processes:\n{proc_names}\n\nDo you want to terminate them and try again?",
        "Terminate processes": "Terminate processes",
        "Cancel": "Cancel",
        "Success": "Success",
        "Folder successfully deleted after terminating processes.": "Folder successfully deleted after terminating processes.",
        "Failed to delete folder:\n{error}": "Failed to delete folder:\n{error}",
        "Deletion canceled.": "Deletion canceled.",
        "Please fill in the server name and IP.": "Please fill in the server name and IP.",

        # --- ServerControlPanel ---
        "Settings": "Settings",
        "I accept the EULA": "I accept the EULA",
        "Enable offline mode (cracked)": "Enable offline mode (cracked)",
        "Use playit.gg (tunnel)": "Use playit.gg (tunnel)",
        "Control": "Control",
        "Start server": "Start server",
        "Stop server": "Stop server",
        "You must accept the EULA!": "You must accept the EULA!",
        "Managing server: ": "Managing server: ",
        "Manage server": "Manage server",
        "Server started.": "Server started.",
        "Server stopped.": "Server stopped.",
        "Server is already running.": "Server is already running.",
        "Server is not running.": "Server is not running.",
        "Server forcefully stopped.": "Server forcefully stopped.",

        # --- CreateServerDialog ---
        "Create your own server": "Create your own server",
        "Port": "Port",
        "Version": "Version",
        "Core": "Core",
        "Create": "Create",
        "Please enter a valid server name and port (number).": "Please enter a valid server name and port (number).",
        "RAM (GB):": "RAM (GB):",
        "Console": "Console",
        "Plugins": "Plugins",
        "Backup": "Backup",
        "Search": "Search",
        "Install": "Install",
        "Uninstall": "Uninstall",
        "Open folder": "Open folder",
        "Server console": "Server console",
        "Enter command...": "Enter command...",
        "Send": "Send",
        "Online mode": "Online mode",
        "Offline mode": "Offline mode",
        "Max players": "Max players",
        "MOTD": "MOTD",
        "Create Backup": "Create Backup",
        "Restore": "Restore",
        "Backup created": "Backup created",
        "Backup restored": "Backup restored",
        "Downloading plugin...": "Downloading plugin...",
        "Plugin installed": "Plugin installed",
        "Search plugins...": "Search plugins...",
        "No plugins found": "No plugins found",
        "Backups": "Backups",
        "Restore backup": "Restore backup",
        "Are you sure?": "Are you sure?",
        "Install plugin": "Install plugin",
        "CurseForge API Key:": "CurseForge API Key:",
        "Test key": "Test key",
        "Error": "Error"
    },

    "de": {
        "Save settings": "Einstellungen speichern",
        "Play": "Spielen",
        "Error": "Fehler",
        "Done": "Erledigt"
    },

    "fr": {
        "Save settings": "Sauvegarder",
        "Play": "Jouer",
        "Error": "Erreur",
        "Done": "Terminé"
    }
}


def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    # Если файла нет или ошибка, возвращаем значения по умолчанию
    return {
        "java_path": "",
        "ram": 4096,
        "max_ram": 4096,
        "jvm_args": "",
        "language": "ru",
        "theme": "dark",
        "rpc_custom_status": "",
        "launch_mode": "launcher_lib",
        "curseforge_api_key": "",
        "azure_client_id": ""
    }


def save_config(config):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print("Ошибка сохранения настроек:", e)


CURSEFORGE_API = "https://api.curseforge.com/v1"

_cf_api_key_cache = None
def get_cf_api_key():
    global _cf_api_key_cache
    if _cf_api_key_cache is None:
        cfg = load_config()
        _cf_api_key_cache = cfg.get("curseforge_api_key", "")
    return _cf_api_key_cache

def invalidate_cf_api_key_cache():
    global _cf_api_key_cache
    _cf_api_key_cache = None


# =========== УПРАВЛЕНИЕ ИНСТАНСАМИ ===========

def load_instances():
    try:
        if not os.path.exists(INSTANCES_FILE):
            return []
        with open(INSTANCES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print("Ошибка загрузки инстансов:", e)
        return []

def save_instances(instances):
    try:
        os.makedirs(os.path.dirname(INSTANCES_FILE), exist_ok=True)
        with open(INSTANCES_FILE, "w", encoding="utf-8") as f:
            json.dump(instances, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("Ошибка сохранения инстансов:", e)

def create_instance(name, mc_version="latest_release", loader="Vanilla", loader_version="", icon="📦"):
    import uuid
    inst_id = str(uuid.uuid4())[:8]
    instance = {
        "id": inst_id,
        "name": name,
        "icon": icon,
        "mc_version": mc_version,
        "loader": loader,
        "loader_version": loader_version,
        "java_path": "",
        "min_ram": 2048,
        "max_ram": 4096,
        "jvm_args": "",
        "width": 854,
        "height": 480,
        "last_played": "",
        "created": datetime.datetime.now().isoformat(),
        "notes": "",
    }
    # Create instance game directory
    inst_dir = os.path.join(INSTANCES_DIR, inst_id, "game")
    os.makedirs(inst_dir, exist_ok=True)
    # Initialize launcher_profiles.json
    profile_path = os.path.join(inst_dir, "launcher_profiles.json")
    if not os.path.exists(profile_path):
        with open(profile_path, "w", encoding="utf-8") as f:
            json.dump({"profiles": {}, "settings": {}, "selectedProfile": None}, f)
    return instance


class AccountSystem:
    def __init__(self):
        self.accounts_file = "accounts.json"
        self.licenses_file = "licenses.json"
        self.current_user = None
        self.load_initial_data()
    
    def load_initial_data(self):
        """Загрузка начальных данных"""
        if not os.path.exists(self.accounts_file):
            self.save_accounts([])
        
        if not os.path.exists(self.licenses_file):
            self.save_licenses({})
    
    def save_accounts(self, accounts):
        """Сохранение аккаунтов"""
        with open(self.accounts_file, "w", encoding="utf-8") as f:
            json.dump(accounts, f, indent=2)
    
    def save_licenses(self, licenses):
        """Сохранение лицензий"""
        with open(self.licenses_file, "w", encoding="utf-8") as f:
            json.dump(licenses, f, indent=2)
    
    def load_accounts(self):
        """Загрузка аккаунтов"""
        try:
            with open(self.accounts_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    
    def generate_license_key(self, user_id, tier="standard", duration=365):
        """Генерация ключа лицензии"""
        timestamp = int(datetime.datetime.now().timestamp())
        key_base = f"{user_id}_{tier}_{duration}_{timestamp}_{secrets.token_hex(4)}"
        license_key = hashlib.sha256(key_base.encode()).hexdigest()[:24].upper()
        
        # Форматирование в группы по 6 символов
        formatted_key = '-'.join([license_key[i:i+6] for i in range(0, len(license_key), 6)])
        
        # Сохранение лицензии
        licenses = self.load_licenses()
        licenses[formatted_key] = {
            "user_id": user_id,
            "tier": tier,
            "duration_days": duration,
            "created_at": timestamp,
            "expires_at": timestamp + (duration * 86400),
            "activated": False
        }
        self.save_licenses(licenses)
        
        return formatted_key
    
    def load_licenses(self):
        """Загрузка лицензий"""
        try:
            with open(self.licenses_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    
    def activate_license(self, license_key, user_id):
        """Активация лицензии"""
        licenses = self.load_licenses()
        
        if license_key in licenses:
            license_data = licenses[license_key]
            
            if license_data["activated"]:
                return False, "Лицензия уже активирована"
            
            if datetime.datetime.now().timestamp() > license_data["expires_at"]:
                return False, "Срок действия лицензии истек"
            
            license_data["activated"] = True
            license_data["activated_by"] = user_id
            license_data["activated_at"] = datetime.datetime.now().timestamp()
            
            # Обновление пользователя
            accounts = self.load_accounts()
            for account in accounts:
                if account["user_id"] == user_id:
                    account["license_tier"] = license_data["tier"]
                    account["license_expires"] = license_data["expires_at"]
                    account["premium_features"] = self.get_premium_features(license_data["tier"])
                    break
            
            self.save_accounts(accounts)
            self.save_licenses(licenses)
            
            return True, "Лицензия успешно активирована"
        
        return False, "Неверный ключ лицензии"
    
    def get_premium_features(self, tier):
        """Получение премиум функций по уровню"""
        features = {
            "standard": ["basic_skins", "daily_gifts", "cloud_sync"],
            "premium": ["all_skins", "priority_support", "custom_themes", "no_ads"],
            "ultimate": ["early_access", "server_hosting", "dedicated_support", "all_features"]
        }
        return features.get(tier, ["basic_skins"])
    
    def register_user(self, username, email, password):
        """Регистрация пользователя"""
        # Проверка существования
        accounts = self.load_accounts()
        
        for account in accounts:
            if account["username"] == username:
                return False, "Имя пользователя уже занято"
            if account["email"] == email:
                return False, "Email уже зарегистрирован"
        
        # Создание пользователя
        user_id = secrets.token_hex(16)
        salt = secrets.token_hex(8)
        password_hash = hashlib.sha256(f"{password}{salt}".encode()).hexdigest()
        
        user_data = {
            "user_id": user_id,
            "username": username,
            "email": email,
            "password_hash": password_hash,
            "salt": salt,
            "created_at": datetime.datetime.now().isoformat(),
            "last_login": None,
            "license_tier": "free",
            "xp": 0,
            "level": 1,
            "gifts_claimed": [],
            "achievements": [],
            "settings": {},
            "skins": ["default"],
            "friends": []
        }
        
        accounts.append(user_data)
        self.save_accounts(accounts)
        
        # Создание папки пользователя
        user_folder = f"user_data/{user_id}"
        os.makedirs(user_folder, exist_ok=True)
        os.makedirs(f"{user_folder}/skins", exist_ok=True)
        os.makedirs(f"{user_folder}/configs", exist_ok=True)
        
        return True, user_data
    
    def login(self, username_or_email, password):
        """Вход в аккаунт"""
        accounts = self.load_accounts()
        
        for account in accounts:
            if account["username"] == username_or_email or account["email"] == username_or_email:
                # Проверка пароля
                test_hash = hashlib.sha256(
                    f"{password}{account['salt']}".encode()
                ).hexdigest()
                
                if test_hash == account["password_hash"]:
                    account["last_login"] = datetime.datetime.now().isoformat()
                    self.save_accounts(accounts)
                    self.current_user = account
                    return True, account
        
        return False, "Неверное имя пользователя или пароль"
    
    def logout(self):
        """Выход из аккаунта"""
        self.current_user = None
    
    def is_premium(self):
        """Проверка премиум статуса"""
        if not self.current_user:
            return False
        
        if self.current_user.get("license_tier") == "free":
            return False
        
        expires = self.current_user.get("license_expires", 0)
        return datetime.datetime.now().timestamp() < expires
    
    def get_user_folder(self):
        """Получение папки пользователя"""
        if self.current_user:
            return f"user_data/{self.current_user['user_id']}"
        return "user_data/guest"
    

class CustomizableUI:
    def __init__(self):
        self.settings_file = "ui_settings.json"
        self.load_settings()
    
    def load_settings(self):
        """Загрузка настроек UI"""
        try:
            with open(self.settings_file, "r", encoding="utf-8") as f:
                self.settings = json.load(f)
        except:
            self.settings = {
                "theme": "dark",
                "accent_color": "#4facfe",
                "background_type": "gradient",  # gradient, image, solid
                "background_image": None,
                "gradient_start": "#1a1a2e",
                "gradient_end": "#16213e",
                "animations": True,
                "font_size": 14,
                "font_family": "Segoe UI",
                "rounded_corners": True,
                "button_style": "modern",  # modern, classic, flat
                "transparency": 0.95,
                "custom_css": ""
            }
            self.save_settings()
    
    def save_settings(self):
        """Сохранение настроек"""
        with open(self.settings_file, "w", encoding="utf-8") as f:
            json.dump(self.settings, f, indent=2)
    
    def apply_to_widget(self, widget):
        """Применение настроек к виджету"""
        style = self.generate_stylesheet()
        widget.setStyleSheet(style)
        
        # Установка шрифта
        font = QFont()
        font.setFamily(self.settings["font_family"])
        font.setPointSize(self.settings["font_size"])
        widget.setFont(font)
    
    def generate_stylesheet(self):
        """CurseForge-style design"""
        accent = self.settings.get("accent_color", "#a855f7")
        
        return f"""
            QMainWindow, QWidget {{
                background: transparent;
                color: #e8e8ee;
                font-family: 'Segoe UI', -apple-system, sans-serif;
            }}
            
            QLabel {{
                color: #e8e8ee;
                font-size: 13px;
                background: transparent;
            }}
            
            QPushButton {{
                background: rgba(255,255,255,0.06);
                color: rgba(255,255,255,0.85);
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 12px;
                font-weight: 500;
            }}
            
            QPushButton:hover {{
                background: rgba(255,255,255,0.1);
                color: white;
            }}
            
            QPushButton:pressed {{
                background: rgba(255,255,255,0.04);
            }}
            
            QLineEdit, QTextEdit, QPlainTextEdit {{
                background: rgba(255,255,255,0.05);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 6px;
                padding: 8px 12px;
                color: #e8e8ee;
                font-size: 12px;
                selection-background-color: {accent};
            }}
            
            QLineEdit:focus, QTextEdit:focus {{
                border-color: {accent};
            }}
            
            QComboBox {{
                background: rgba(255,255,255,0.05);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 6px;
                padding: 6px 12px;
                color: #e8e8ee;
                font-size: 12px;
            }}
            
            QComboBox:focus {{ border-color: {accent}; }}
            
            QComboBox QAbstractItemView {{
                background: #1a1a24;
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 6px;
                selection-background-color: {accent};
                color: white;
                padding: 2px;
            }}
            
            QProgressBar {{
                background: rgba(255,255,255,0.04);
                border-radius: 3px;
                height: 4px;
                text-align: center;
                font-size: 10px;
                color: rgba(255,255,255,0.3);
            }}
            
            QProgressBar::chunk {{
                background: {accent};
                border-radius: 3px;
            }}
            
            QListWidget, QTreeWidget, QTableWidget {{
                background: rgba(255,255,255,0.02);
                border: 1px solid rgba(255,255,255,0.06);
                border-radius: 8px;
                color: #e8e8ee;
                font-size: 12px;
            }}
            
            QListWidget::item, QTreeWidget::item {{
                padding: 6px 10px;
                border-radius: 5px;
                margin: 1px 4px;
            }}
            
            QListWidget::item:hover, QTreeWidget::item:hover {{
                background: rgba(255,255,255,0.04);
            }}
            
            QListWidget::item:selected, QTreeWidget::item:selected {{
                background: {accent};
                color: white;
            }}
            
            QScrollBar:vertical {{
                background: transparent;
                width: 4px;
            }}
            
            QScrollBar::handle:vertical {{
                background: rgba(255,255,255,0.06);
                border-radius: 2px;
                min-height: 24px;
            }}
            
            QScrollBar::handle:vertical:hover {{
                background: rgba(255,255,255,0.12);
            }}
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0;
            }}
            
            QScrollBar:horizontal {{
                background: transparent;
                height: 4px;
            }}
            
            QScrollBar::handle:horizontal {{
                background: rgba(255,255,255,0.06);
                border-radius: 2px;
                min-width: 24px;
            }}
            
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                width: 0;
            }}
            
            QTabWidget::pane {{
                background: rgba(255,255,255,0.02);
                border: 1px solid rgba(255,255,255,0.06);
                border-radius: 8px;
            }}
            
            QTabBar::tab {{
                background: transparent;
                color: rgba(255,255,255,0.35);
                padding: 8px 16px;
                border-radius: 6px;
                margin: 2px;
                font-weight: 500;
                font-size: 12px;
            }}
            
            QTabBar::tab:hover {{
                background: rgba(255,255,255,0.04);
                color: rgba(255,255,255,0.7);
            }}
            
            QTabBar::tab:selected {{
                background: {accent};
                color: white;
            }}
            
            QCheckBox, QRadioButton {{
                color: #e8e8ee;
                font-size: 12px;
                spacing: 6px;
            }}
            
            QCheckBox::indicator {{
                width: 16px; height: 16px;
                border-radius: 3px;
                border: 1px solid rgba(255,255,255,0.15);
                background: rgba(255,255,255,0.04);
            }}
            
            QCheckBox::indicator:checked {{
                background: {accent};
                border-color: {accent};
            }}
            
            QSlider::groove:horizontal {{
                background: rgba(255,255,255,0.06);
                height: 4px;
                border-radius: 2px;
            }}
            
            QSlider::handle:horizontal {{
                background: {accent};
                width: 14px; height: 14px;
                margin: -5px 0;
                border-radius: 7px;
            }}
        """
        # Добавляем пользовательский CSS
        stylesheet += self.settings.get("custom_css", "")
        
        return stylesheet
    
    def darken_color(self, color, percent):
        """Затемнение цвета"""
        from PyQt6.QtGui import QColor
        c = QColor(color)
        return c.darker(100 + percent).name()
    
    def lighten_color(self, color, percent):
        """Осветление цвета"""
        from PyQt6.QtGui import QColor
        c = QColor(color)
        return c.lighter(100 + percent).name()
    
    def create_theme_presets(self):
        """Создание пресетов тем"""
        return {
            "dark_default": {
                "theme": "dark",
                "accent_color": "#4facfe",
                "gradient_start": "#1a1a2e",
                "gradient_end": "#16213e"
            },
            "light_modern": {
                "theme": "light",
                "accent_color": "#667eea",
                "gradient_start": "#f5f7fa",
                "gradient_end": "#c3cfe2"
            }
        }
    
    def apply_theme_preset(self, preset_name):
        """Применение пресета темы"""
        presets = self.create_theme_presets()
        if preset_name in presets:
            self.settings.update(presets[preset_name])
            self.save_settings()
            return True
        return False
    
# =========== ДОБАВИТЬ ПОСЛЕ CustomizableUI ===========
class CrossPlatformSupport:
    @staticmethod
    def get_platform_info():
        """Получение информации о платформе"""
        system = platform.system()
        info = {
            "system": system,
            "release": platform.release(),
            "version": platform.version(),
            "architecture": platform.architecture()[0],
            "processor": platform.processor() or "Unknown",
            "python_version": platform.python_version(),
            "machine": platform.machine()
        }
        
        # Дополнительная информация для конкретных ОС
        if system == "Darwin":  # macOS
            try:
                import subprocess
                mac_version = subprocess.check_output(
                    ["sw_vers", "-productVersion"], 
                    text=True
                ).strip()
                info["mac_version"] = mac_version
            except:
                pass
        
        elif system == "Windows":
            info["windows_version"] = platform.win32_ver()
        
        elif system == "Linux":
            try:
                import distro
                info["distro"] = distro.name(pretty=True)
                info["distro_version"] = distro.version()
            except:
                pass
        
        return info
    
    @staticmethod
    def get_minecraft_path():
        """Получение пути к Minecraft для текущей ОС"""
        system = platform.system()
        
        if system == "Darwin":  # macOS
            return os.path.expanduser("~/Library/Application Support/minecraft")
        
        elif system == "Windows":
            return os.path.join(os.getenv('APPDATA'), '.minecraft')
        
        elif system == "Linux":
            return os.path.expanduser("~/.minecraft")
        
        else:
            return os.path.expanduser("~/.minecraft")
    
    @staticmethod
    def get_app_data_path():
        """Получение пути для данных приложения"""
        system = platform.system()
        app_name = "SuperLauncher"
        
        if system == "Darwin":  # macOS
            return os.path.expanduser(f"~/Library/Application Support/{app_name}")
        
        elif system == "Windows":
            return os.path.join(os.getenv('APPDATA'), app_name)
        
        elif system == "Linux":
            return os.path.expanduser(f"~/.config/{app_name}")
        
        else:
            return "."
    
    @staticmethod
    def get_java_path():
        """Поиск пути к Java"""
        system = platform.system()
        
        # Общие пути для поиска Java
        common_paths = []
        
        if system == "Darwin":  # macOS
            common_paths = [
                "/usr/bin/java",
                "/Library/Internet Plug-Ins/JavaAppletPlugin.plugin/Contents/Home/bin/java",
                "/System/Library/Frameworks/JavaVM.framework/Versions/Current/Commands/java",
                "/opt/homebrew/opt/openjdk/bin/java",
                "/usr/local/opt/openjdk/bin/java"
            ]
        
        elif system == "Windows":
            program_files = os.getenv("ProgramFiles", "C:\\Program Files")
            program_files_x86 = os.getenv("ProgramFiles(x86)", "C:\\Program Files (x86)")
            
            common_paths = [
                os.path.join(program_files, "Java", "jdk-*", "bin", "java.exe"),
                os.path.join(program_files, "Java", "jre-*", "bin", "java.exe"),
                os.path.join(program_files_x86, "Java", "jdk-*", "bin", "java.exe"),
                os.path.join(program_files_x86, "Java", "jre-*", "bin", "java.exe"),
                "C:\\ProgramData\\Oracle\\Java\\javapath\\java.exe"
            ]
        
        elif system == "Linux":
            common_paths = [
                "/usr/bin/java",
                "/usr/lib/jvm/default-java/bin/java",
                "/usr/lib/jvm/java-*-openjdk/bin/java",
                "/opt/jdk-*/bin/java"
            ]
        
        # Проверка каждого пути
        for path in common_paths:
            if "*" in path:
                # Поиск по шаблону
                import glob
                matches = glob.glob(path)
                if matches:
                    return matches[0]
            else:
                if os.path.exists(path):
                    return path
        
        # Проверка переменной PATH
        import shutil
        java_path = shutil.which("java")
        if java_path:
            return java_path
        
        return ""
    
    @staticmethod
    def is_mac_arm():
        """Проверка Apple Silicon (M1/M2/M3)"""
        if platform.system() == "Darwin":
            try:
                import subprocess
                result = subprocess.run(
                    ["sysctl", "-n", "machdep.cpu.brand_string"],
                    capture_output=True,
                    text=True
                )
                return "Apple" in result.stdout
            except:
                pass
        return False
    
    @staticmethod
    def optimize_for_platform():
        """Оптимизация для конкретной платформы"""
        system = platform.system()
        recommendations = []
        
        if system == "Darwin":
            recommendations = [
                "Используйте ARM-версию Java для лучшей производительности на Apple Silicon",
                "Включите Metal API в настройках Minecraft для улучшения FPS",
                "Проверьте доступность обновлений через App Store"
            ]
        
        elif system == "Windows":
            recommendations = [
                "Убедитесь, что установлены последние драйверы видеокарты",
                "Включите игровой режим в настройках Windows",
                "Проверьте антивирус на предмет блокировки лаунчера"
            ]
        
        elif system == "Linux":
            recommendations = [
                "Установите проприетарные драйверы NVIDIA для лучшей производительности",
                "Используйте OpenJDK 17 или новее",
                "Проверьте права доступа к папке .minecraft"
            ]
        
        return recommendations
    
# =========== ДОБАВИТЬ ПОСЛЕ CrossPlatformSupport ===========
class InstallCancelled(Exception):
    """Исключение для отмены установки сборки"""
    pass


class BuildsManager:
    def __init__(self):
        self.modrinth_api = "https://api.modrinth.com/v2"
        self.curseforge_api = "https://api.curseforge.com/v1"
        self.modpacks_cache = {}

    def search_modrinth(self, query="", limit=20):
        try:
            params = {
                "limit": limit,
                "index": "downloads",
                "facets": '[["project_type:modpack"]]'
            }
            if query:
                params["query"] = query
            resp = requests.get(f"{self.modrinth_api}/search", params=params, timeout=15,
                                headers={"User-Agent": "SuperLauncher/2.0"})
            data = resp.json()
            modpacks = []
            for hit in data.get("hits", []):
                modpacks.append({
                    "id": hit["project_id"], "slug": hit.get("slug"),
                    "name": hit["title"], "description": hit.get("description", ""),
                    "icon_url": hit.get("icon_url"), "downloads": hit.get("downloads", 0),
                    "author": hit.get("author", "Unknown"),
                    "versions": hit.get("versions", []), "loaders": hit.get("loaders", []),
                    "source": "modrinth"
                })
            return modpacks
        except Exception as e:
            print(f"Modrinth search error: {e}")
            return []

    def search_curseforge(self, query="", limit=30):
        try:
            params = {
                "gameId": 432, "classId": 4471, "searchFilter": query,
                "pageSize": limit, "sortField": 2, "sortOrder": "desc"
            }
            resp = requests.get(f"{self.curseforge_api}/mods/search", params=params,
                                headers={"x-api-key": get_cf_api_key(), "Accept": "application/json"}, timeout=15)
            data = resp.json()
            modpacks = []
            for mod in data.get("data", []):
                modpacks.append({
                    "id": mod["id"], "name": mod.get("name", ""),
                    "description": mod.get("summary", ""),
                    "icon_url": (mod.get("logo") or {}).get("url"),
                    "downloads": mod.get("downloadCount", 0),
                    "author": (mod.get("authors") or [{}])[0].get("name", "Unknown") if mod.get("authors") else "Unknown",
                    "source": "curseforge"
                })
            return modpacks
        except Exception as e:
            print(f"CurseForge search error: {e}")
            return []

    def get_modpack_versions(self, project_id, source="modrinth"):
        if source == "modrinth":
            try:
                resp = requests.get(f"{self.modrinth_api}/project/{project_id}/version", timeout=15,
                                    headers={"User-Agent": "SuperLauncher/2.0"})
                return resp.json()
            except:
                return []
        else:
            try:
                resp = requests.get(f"{self.curseforge_api}/mods/{project_id}/files",
                                    headers={"x-api-key": get_cf_api_key(), "Accept": "application/json"}, timeout=15)
                data = resp.json()
                return data.get("data", [])
            except:
                return []

    def backup_mods(self, mc_dir):
        mods_dir = os.path.join(mc_dir, "mods")
        if not os.path.exists(mods_dir):
            return
        import time
        backup = os.path.join(mc_dir, f"mods_backup_{int(time.time())}")
        shutil.copytree(mods_dir, backup)
        return backup

    def restore_mods(self, mc_dir):
        import glob, re
        backups = sorted(glob.glob(os.path.join(mc_dir, "mods_backup_*")))
        if not backups:
            return False
        backup = backups[-1]
        mods_dir = os.path.join(mc_dir, "mods")
        if os.path.exists(mods_dir):
            shutil.rmtree(mods_dir, ignore_errors=True)
        shutil.copytree(backup, mods_dir)
        shutil.rmtree(backup, ignore_errors=True)
        return True

    def deduplicate_mods(self, mc_dir):
        mods_dir = os.path.join(mc_dir, "mods")
        if not os.path.isdir(mods_dir):
            return
        import re

        def _parse_version(ver_str):
            parts = ver_str.replace("-", ".").split(".")
            nums = []
            for p in parts:
                try:
                    nums.append(int(p))
                except ValueError:
                    nums.append(0)
            return tuple(nums)

        def _read_meta(path):
            with zipfile.ZipFile(path, 'r') as z:
                if "META-INF/mods.toml" in z.namelist():
                    text = z.read("META-INF/mods.toml").decode("utf-8", errors="replace")
                    m = re.search(r'^\s*modId\s*=\s*"([^"]+)"', text, re.MULTILINE)
                    v = re.search(r'^\s*version\s*=\s*"([^"]+)"', text, re.MULTILINE)
                    return (m.group(1), v.group(1) if v else "0") if m else None
                if "fabric.mod.json" in z.namelist():
                    data = json.loads(z.read("fabric.mod.json"))
                    mid = data.get("id")
                    return (mid, data.get("version", "0")) if mid else None
                if "quilt.mod.json" in z.namelist():
                    data = json.loads(z.read("quilt.mod.json"))
                    mid = data.get("quilt_loader", {}).get("id")
                    return (mid, data.get("version", "0") or "0") if mid else None
            return None

        entries = []
        for fn in os.listdir(mods_dir):
            if not fn.endswith(".jar"):
                continue
            path = os.path.join(mods_dir, fn)
            try:
                meta = _read_meta(path)
                if meta:
                    mid, ver = meta
                    # loader_priority: 0=Forge (mods.toml), 1=Fabric, 2=Quilt
                    with zipfile.ZipFile(path, 'r') as z:
                        if "META-INF/mods.toml" in z.namelist():
                            lp = 0
                        elif "fabric.mod.json" in z.namelist():
                            lp = 1
                        else:
                            lp = 2
                    entries.append((mid, fn, path, ver, lp))
            except Exception:
                pass

        mod_groups = {}
        for mid, fn, path, ver, lp in entries:
            mod_groups.setdefault(mid, []).append((fn, path, ver, lp))

        removed = 0
        for mid, group in mod_groups.items():
            if len(group) > 1:
                group.sort(key=lambda x: (x[3], tuple(-n for n in _parse_version(x[2]))))
                for fn, path, ver, lp in group[1:]:
                    try:
                        os.remove(path)
                        removed += 1
                        loader_name = ["Forge", "Fabric", "Quilt"][lp]
                        print(f"Удалён дубликат: {fn} (modId={mid}, версия={ver}, {loader_name})")
                    except Exception:
                        pass
        if removed:
            print(f"Дедупликация завершена: удалено {removed} дубликатов модов")

    # Известные конфликтные Fabric-моды, которые ломают RegistryDataLoader через Sinytra Connector
    CONFLICTING_MODS = {
        "betterend": "BetterEnd (Fabric) — ломает загрузку регистров через Connector",
        "bclib": "BCLib (Fabric, библиотека BetterEnd) — конфликтует с fabric-registry-sync-v0",
        "betterendisland": "BetterEnd Island (Fabric) — зависит от BCLib",
    }

    def detect_conflicting_mods(self, mc_dir):
        import re
        mods_dir = os.path.join(mc_dir, "mods")
        if not os.path.isdir(mods_dir):
            return []
        found = []
        for fn in os.listdir(mods_dir):
            if not fn.endswith(".jar"):
                continue
            path = os.path.join(mods_dir, fn)
            try:
                with zipfile.ZipFile(path, 'r') as z:
                    if "fabric.mod.json" in z.namelist():
                        data = json.loads(z.read("fabric.mod.json"))
                        mid = data.get("id", "")
                        if mid in self.CONFLICTING_MODS:
                            found.append((fn, mid, self.CONFLICTING_MODS[mid]))
                    elif "META-INF/mods.toml" in z.namelist():
                        text = z.read("META-INF/mods.toml").decode("utf-8", errors="replace")
                        m = re.search(r'^\s*modId\s*=\s*"([^"]+)"', text, re.MULTILINE)
                        if m:
                            mid = m.group(1)
                            if mid in self.CONFLICTING_MODS:
                                found.append((fn, mid, self.CONFLICTING_MODS[mid]))
            except Exception:
                pass
        return found

    def download_file(self, url, save_path, callback=None):
        resp = requests.get(url, stream=True, timeout=120)
        resp.raise_for_status()
        total = int(resp.headers.get("content-length", 0))
        written = 0
        with open(save_path, "wb") as f:
            for chunk in resp.iter_content(8192):
                if chunk:
                    f.write(chunk)
                    written += len(chunk)
                    if callback and total > 0:
                        callback(int(written * 100 / total))
        if callback and total > 0:
            callback(100)

    def _install_modrinth_pack(self, version_data, mc_dir, callback=None):
        files = version_data.get("files", [])
        if not files:
            return None, "Нет файлов для скачивания"
        primary = next((f for f in files if f.get("primary")), files[0])
        if not primary.get("url"):
            return None, "Нет ссылки на файл"

        ver_num = version_data.get("version_number", "?")
        import tempfile, zipfile, json as j, shutil
        tmp = tempfile.mkdtemp(prefix="mrpack-")
        try:
            mrpack_path = os.path.join(tmp, primary["filename"])
            if callback:
                callback(0)
            print(f"Бекап старых модов перед установкой сборки...")
            self.backup_mods(mc_dir)
            self.download_file(primary["url"], mrpack_path, callback)

            if callback:
                callback(50)

            with zipfile.ZipFile(mrpack_path, 'r') as z:
                z.extractall(tmp)

            index_path = os.path.join(tmp, "modrinth.index.json")
            if not os.path.exists(index_path):
                return None, "modrinth.index.json не найден в .mrpack"
            with open(index_path, encoding="utf-8") as f:
                idx = j.load(f)

            deps = idx.get("dependencies", {})
            mc_version = deps.get("minecraft", "unknown")
            loader_type = "vanilla"
            for k in deps:
                if k in ("fabric-loader", "quilt-loader"):
                    loader_type = k.replace("-loader", "")
                elif k == "forge":
                    loader_type = "forge"
                elif k == "neoforge":
                    loader_type = "neoforge"

            pack_name = idx.get("name", version_data.get("name", "modpack")).strip()
            safe_name = "".join(c for c in pack_name if c.isalnum() or c in " _-")

            idx_files = idx.get("files", [])
            total_files = len(idx_files)
            installed = []
            for i, entry in enumerate(idx_files):
                path = entry.get("path", "")
                downloads = entry.get("downloads", [])
                if not path or not downloads:
                    continue
                target = os.path.normpath(os.path.join(mc_dir, path))
                if not target.startswith(os.path.normpath(mc_dir) + os.sep):
                    continue
                os.makedirs(os.path.dirname(target), exist_ok=True)
                if not os.path.exists(target):
                    try:
                        self.download_file(downloads[0], target, callback)
                    except InstallCancelled:
                        raise
                    except Exception:
                        if os.path.exists(target):
                            os.remove(target)
                installed.append(target)
                if callback and total_files > 0:
                    callback(50 + int(40 * (i + 1) / total_files))

            for odir in ("overrides", "client-overrides"):
                sdir = os.path.join(tmp, odir)
                if os.path.exists(sdir):
                    for root, dirs, flist in os.walk(sdir):
                        rel = os.path.relpath(root, sdir)
                        for fn in flist:
                            src = os.path.join(root, fn)
                            dst = os.path.join(mc_dir, rel, fn)
                            os.makedirs(os.path.dirname(dst), exist_ok=True)
                            shutil.copy2(src, dst)
                            installed.append(dst)

            if callback:
                callback(95)
            self.deduplicate_mods(mc_dir)
            if callback:
                callback(100)
            return safe_name, {"mc_version": mc_version, "loader": loader_type,
                               "_source": "modrinth", "_version_id": ver_num,
                               "_installed_files": installed}
        except Exception as e:
            return None, str(e)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def _install_curseforge_pack(self, version_data, mc_dir, callback=None):
        dl_url = version_data.get("downloadUrl", "")
        if not dl_url:
            try:
                resp = requests.get(
                    f"{self.curseforge_api}/mods/{version_data['modId']}/files/{version_data['id']}/download-url",
                    headers={"x-api-key": get_cf_api_key(), "Accept": "application/json"}, timeout=15)
                dl_url = resp.json().get("data", "")
            except Exception:
                pass
        if not dl_url:
            return None, "CurseForge: не удалось получить ссылку"

        import tempfile, zipfile, json as j, shutil
        tmp = tempfile.mkdtemp(prefix="cfpack-")
        try:
            filename = version_data.get("fileName", "pack.zip")
            zip_path = os.path.join(tmp, filename)
            if callback:
                callback(0)
            print(f"Бекап старых модов перед установкой сборки...")
            self.backup_mods(mc_dir)
            self.download_file(dl_url, zip_path, callback)

            if callback:
                callback(30)

            with zipfile.ZipFile(zip_path, 'r') as z:
                z.extractall(tmp)

            manifest_path = os.path.join(tmp, "manifest.json")
            installed = []
            if not os.path.exists(manifest_path):
                mc_version = "unknown"
                loader_type = "vanilla"
                for root, dirs, flist in os.walk(tmp):
                    for fn in flist:
                        if fn.endswith((".jar", ".litemod")):
                            rel = os.path.relpath(os.path.join(root, fn), tmp)
                            dst = os.path.join(mc_dir, rel)
                            os.makedirs(os.path.dirname(dst), exist_ok=True)
                            shutil.copy2(os.path.join(root, fn), dst)
                            installed.append(dst)
                if callback:
                    callback(100)
                return "curseforge-pack", {"mc_version": mc_version, "loader": loader_type, "_source": "curseforge", "_version_id": str(version_data.get("id", "")), "_installed_files": installed}

            with open(manifest_path, encoding="utf-8") as f:
                manifest = j.load(f)

            mc_version = manifest.get("minecraft", {}).get("version", "unknown")
            loader_data = manifest.get("minecraft", {}).get("modLoaders", [{}])[0] if manifest.get("minecraft", {}).get("modLoaders") else {}
            loader_id = loader_data.get("id", "")
            loader_type = "forge"
            if "fabric" in loader_id.lower():
                loader_type = "fabric"
            elif "quilt" in loader_id.lower():
                loader_type = "quilt"
            elif "neoforge" in loader_id.lower():
                loader_type = "neoforge"

            cf_files = manifest.get("files", [])
            for i, fentry in enumerate(cf_files):
                project_id = fentry.get("projectID", 0)
                file_id = fentry.get("fileID", 0)
                fpath = fentry.get("filePathOverride", fentry.get("path", ""))
                if not fpath:
                    continue
                try:
                    fresp = requests.get(
                        f"{self.curseforge_api}/mods/{project_id}/files/{file_id}/download-url",
                        headers={"x-api-key": get_cf_api_key(), "Accept": "application/json"}, timeout=15)
                    furl = fresp.json().get("data", "")
                    if furl:
                        target = os.path.normpath(os.path.join(mc_dir, fpath))
                        if not target.startswith(os.path.normpath(mc_dir) + os.sep):
                            continue
                        os.makedirs(os.path.dirname(target), exist_ok=True)
                        if not os.path.exists(target):
                            try:
                                self.download_file(furl, target, callback)
                            except InstallCancelled:
                                raise
                            except Exception:
                                if os.path.exists(target):
                                    os.remove(target)
                        installed.append(target)
                except InstallCancelled:
                    raise
                except Exception:
                    pass
                if callback and cf_files:
                    callback(30 + int(60 * (i + 1) / len(cf_files)))

            for odir in ("overrides",):
                sdir = os.path.join(tmp, odir)
                if os.path.exists(sdir):
                    for root, dirs, flist in os.walk(sdir):
                        rel = os.path.relpath(root, sdir)
                        for fn in flist:
                            src = os.path.join(root, fn)
                            dst = os.path.join(mc_dir, rel, fn)
                            os.makedirs(os.path.dirname(dst), exist_ok=True)
                            shutil.copy2(src, dst)
                            installed.append(dst)

            if callback:
                callback(95)
            self.deduplicate_mods(mc_dir)
            if callback:
                callback(100)
            return manifest.get("name", "curseforge-pack"), {"mc_version": mc_version, "loader": loader_type, "_source": "curseforge", "_version_id": str(version_data.get("id", "")), "_installed_files": installed}
        except Exception as e:
            return None, str(e)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def download_and_install(self, version_data, source, install_base, callback=None):
        if source == "modrinth":
            return self._install_modrinth_pack(version_data, install_base, callback)
        elif source == "curseforge":
            return self._install_curseforge_pack(version_data, install_base, callback)
        return None, "Неизвестный источник"

    def create_install_config(self, pack_folder, source, version_id, mc_versions, loaders):
        os.makedirs(pack_folder, exist_ok=True)
        config = {
            "type": f"{source}_modpack",
            "source": source,
            "version_id": version_id,
            "mc_versions": mc_versions if isinstance(mc_versions, list) else [mc_versions],
            "loaders": loaders if isinstance(loaders, list) else [loaders],
            "install_path": pack_folder,
            "installed_at": datetime.datetime.now().isoformat()
        }
        with open(os.path.join(pack_folder, "superlauncher_config.json"), "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)

    def get_installed_packs(self, install_base):
        installed = []
        if os.path.exists(install_base):
            for folder in os.listdir(install_base):
                cfg = os.path.join(install_base, folder, "superlauncher_config.json")
                if os.path.exists(cfg):
                    try:
                        with open(cfg, encoding="utf-8") as f:
                            conf = json.load(f)
                            conf["name"] = folder
                            installed.append(conf)
                    except:
                        pass
        return installed

    def _install_local_mrpack(self, mrpack_path, mc_dir, callback=None):
        import tempfile, zipfile, json as j, shutil
        tmp = tempfile.mkdtemp(prefix="import-")
        try:
            if callback:
                callback(0)
            print(f"Бекап старых модов перед импортом сборки...")
            self.backup_mods(mc_dir)
            with zipfile.ZipFile(mrpack_path, 'r') as z:
                z.extractall(tmp)
            if callback:
                callback(10)
            index_path = os.path.join(tmp, "modrinth.index.json")
            if not os.path.exists(index_path):
                return None, "modrinth.index.json не найден"
            with open(index_path, encoding="utf-8") as f:
                idx = j.load(f)
            deps = idx.get("dependencies", {})
            mc_version = deps.get("minecraft", "unknown")
            loader_type = "vanilla"
            for k in deps:
                if k in ("fabric-loader", "quilt-loader"):
                    loader_type = k.replace("-loader", "")
                elif k == "forge":
                    loader_type = "forge"
                elif k == "neoforge":
                    loader_type = "neoforge"
            pack_name = idx.get("name", "imported").strip()
            safe_name = "".join(c for c in pack_name if c.isalnum() or c in " _-")
            idx_files = idx.get("files", [])
            installed = []
            for i, entry in enumerate(idx_files):
                path = entry.get("path", "")
                downloads = entry.get("downloads", [])
                if not path or not downloads:
                    continue
                target = os.path.normpath(os.path.join(mc_dir, path))
                if not target.startswith(os.path.normpath(mc_dir) + os.sep):
                    continue
                os.makedirs(os.path.dirname(target), exist_ok=True)
                if not os.path.exists(target):
                    try:
                        self.download_file(downloads[0], target, callback)
                    except InstallCancelled:
                        raise
                    except Exception:
                        if os.path.exists(target):
                            os.remove(target)
                installed.append(target)
                if callback and idx_files:
                    callback(10 + int(80 * (i + 1) / len(idx_files)))
            for odir in ("overrides", "client-overrides"):
                sdir = os.path.join(tmp, odir)
                if os.path.exists(sdir):
                    for root, dirs, flist in os.walk(sdir):
                        rel = os.path.relpath(root, sdir)
                        for fn in flist:
                            src = os.path.join(root, fn)
                            dst = os.path.join(mc_dir, rel, fn)
                            os.makedirs(os.path.dirname(dst), exist_ok=True)
                            shutil.copy2(src, dst)
                            installed.append(dst)
            if callback:
                callback(95)
            self.deduplicate_mods(mc_dir)
            if callback:
                callback(100)
            return safe_name, {"mc_version": mc_version, "loader": loader_type, "_installed_files": installed}
        except Exception as e:
            return None, str(e)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    
    def _cf_cache_path(self, mc_dir, slug, mc_ver, loader_type):
        cache_dir = os.path.join(mc_dir, "cache", "curseforge")
        os.makedirs(cache_dir, exist_ok=True)
        return os.path.join(cache_dir, f"{slug}_{mc_ver}_{loader_type}.jar")

    def download_curseforge_mods_from_modlist(self, mc_dir, callback=None, mc_ver=None, loader_type="forge"):
        import re, hashlib
        from concurrent.futures import ThreadPoolExecutor, as_completed
        modlist_path = os.path.join(mc_dir, "modlist.html")
        if not os.path.exists(modlist_path):
            return 0, "modlist.html не найден"
        with open(modlist_path, encoding="utf-8") as f:
            html = f.read()
        urls = re.findall(r'href="(https://www\.curseforge\.com/minecraft/[^"]+)"', html)
        if not urls:
            return 0, "Нет CurseForge ссылок в modlist.html"
        total = len(urls)
        if not mc_ver:
            mc_ver = "1.20.1"
        loader_map = {"forge": 1, "fabric": 4, "quilt": 5, "neoforge": 6}
        mod_loader_type = loader_map.get(loader_type.lower(), 1)
        cf_key = get_cf_api_key()

        # Подготовка списка задач: (slug, dest_dir, cache_path)
        tasks = []
        for url in urls:
            parts = url.split("/")
            cat = parts[-2] if len(parts) >= 2 else "mc-mods"
            slug = parts[-1] if parts else ""
            if not slug:
                continue
            dest_dir = os.path.join(mc_dir, "mods")
            if "texture" in cat:
                dest_dir = os.path.join(mc_dir, "resourcepacks")
            elif "shader" in cat:
                dest_dir = os.path.join(mc_dir, "shaderpacks")
            os.makedirs(dest_dir, exist_ok=True)
            exists = any(slug.replace("-", "").lower() in f.replace("-", "").lower()
                         for f in os.listdir(dest_dir) if f.endswith((".jar", ".zip")))
            if exists:
                continue
            cache_path = self._cf_cache_path(mc_dir, slug, mc_ver, loader_type)
            if os.path.exists(cache_path):
                # копируем из кэша
                fname = os.path.basename(cache_path)
                import shutil
                shutil.copy2(cache_path, os.path.join(dest_dir, fname))
                print(f"✓ {slug} (из кэша)")
                continue
            tasks.append((slug, dest_dir, cache_path))

        if not tasks:
            if callback:
                callback(100)
            return 0, "Всё уже скачано"

        completed = [0]
        lock = __import__("threading").Lock()
        results = {"downloaded": 0, "skipped": 0}

        def process_one(slug, dest_dir, cache_path):
            try:
                search = requests.get(
                    f"{self.curseforge_api}/mods/search?gameId=432&slug={slug}",
                    headers={"x-api-key": cf_key, "Accept": "application/json"}, timeout=10)
                if search.status_code != 200:
                    return False, slug, "search fail"
                mods_list = search.json().get("data", [])
                if not mods_list:
                    return False, slug, "not found"
                mod_id = mods_list[0]["id"]
                files_resp = requests.get(
                    f"{self.curseforge_api}/mods/{mod_id}/files?gameVersion={mc_ver}&modLoaderType={mod_loader_type}",
                    headers={"x-api-key": cf_key, "Accept": "application/json"}, timeout=10)
                if files_resp.status_code != 200:
                    return False, slug, "files list fail"
                files_data = files_resp.json().get("data", [])
                if not files_data:
                    return False, slug, "no files"
                file_id = files_data[0]["id"]
                dl_resp = requests.get(
                    f"{self.curseforge_api}/mods/{mod_id}/files/{file_id}/download-url",
                    headers={"x-api-key": cf_key, "Accept": "application/json"}, timeout=10)
                if dl_resp.status_code != 200:
                    return False, slug, "dl-url fail"
                dl_url = dl_resp.json().get("data", "")
                if not dl_url:
                    return False, slug, "no dl-url"
                fname = files_data[0].get("fileName", f"{slug}.jar")
                save_path = os.path.join(dest_dir, fname)
                dl_resp2 = requests.get(dl_url, timeout=60, stream=True)
                if dl_resp2.status_code != 200:
                    return False, slug, "download fail"
                with open(save_path, "wb") as f:
                    for chunk in dl_resp2.iter_content(65536):
                        if chunk:
                            f.write(chunk)
                # кэшируем
                import shutil
                shutil.copy2(save_path, cache_path)
                return True, slug, fname
            except Exception as e:
                return False, slug, str(e)

        max_workers = min(5, len(tasks))
        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            futures = {pool.submit(process_one, slug, d, c): slug for slug, d, c in tasks}
            for fut in as_completed(futures):
                ok, slug, info = fut.result()
                with lock:
                    completed[0] += 1
                    if callback:
                        callback(int(90 * completed[0] / len(tasks)))
                    if ok:
                        results["downloaded"] += 1
                        print(f"✓ {slug} -> {info}")
                    else:
                        results["skipped"] += 1
                        print(f"× {slug}: {info}")

        if callback:
            callback(100)
        return (results["downloaded"],
                f"Загружено: {results['downloaded']}/{len(tasks)}, пропущено: {results['skipped']}")

# =========== ДОБАВИТЬ ПОСЛЕ BuildsManager ===========
class SkinsManager:
    def __init__(self, account_system):
        self.account_system = account_system
        self.skins_dir = "assets/skins"
        os.makedirs(self.skins_dir, exist_ok=True)
        
        self.load_skin_library()
    
    def load_skin_library(self):
        """Загрузка библиотеки скинов"""
        self.skin_library = {
            "default": {
                "name": "Стандартный",
                "file": "default.png",
                "rarity": "common",
                "unlocked_by_default": True,
                "price": 0
            },
            "santa_hat": {
                "name": "Шапка Санты",
                "file": "santa_hat.png",
                "rarity": "holiday",
                "unlocked_by_default": False,
                "price": 0,  # Бесплатно в праздники
                "holiday_only": True
            },
            "santa_suit": {
                "name": "Костюм Санты",
                "file": "santa_suit.png",
                "rarity": "epic",
                "unlocked_by_default": False,
                "price": 500,  # XP или валюта
                "holiday_only": True
            },
            "new_year_2026": {
                "name": "2026 Новый Год",
                "file": "new_year_2026.png",
                "rarity": "legendary",
                "unlocked_by_default": False,
                "price": 1000,
                "event": "new_year_2026"
            },
            "reindeer": {
                "name": "Олень Рудольф",
                "file": "reindeer.png",
                "rarity": "rare",
                "unlocked_by_default": False,
                "price": 300,
                "holiday_only": True
            },
            "snowman": {
                "name": "Снеговик",
                "file": "snowman.png",
                "rarity": "rare",
                "unlocked_by_default": False,
                "price": 250,
                "holiday_only": True
            }
        }
    
    def get_available_skins(self, user=None):
        """Получение доступных скинов для пользователя"""
        if not user and self.account_system.current_user:
            user = self.account_system.current_user
        
        available_skins = []
        
        for skin_id, skin_data in self.skin_library.items():
            # Проверяем условия доступа
            if self.can_access_skin(skin_id, user):
                available_skins.append({
                    "id": skin_id,
                    **skin_data,
                    "unlocked": self.is_skin_unlocked(skin_id, user)
                })
        
        return available_skins
    
    def can_access_skin(self, skin_id, user):
        """Проверка доступа к скину"""
        skin_data = self.skin_library.get(skin_id)
        if not skin_data:
            return False
        
        # Проверка праздничных ограничений
        if skin_data.get("holiday_only"):
            # HolidayTheme пока не реализован — пропускаем проверку
            pass
        
        # Проверка ивентов
        if skin_data.get("event"):
            pass
        
        return True
    
    def is_skin_unlocked(self, skin_id, user):
        """Проверка разблокирован ли скин"""
        if not user:
            return False
        
        # По умолчанию разблокированы
        if skin_id == "default":
            return True
        
        # Проверяем в списке скинов пользователя
        user_skins = user.get("skins", ["default"])
        return skin_id in user_skins
    
    def unlock_skin(self, skin_id, user):
        """Разблокировка скина"""
        if self.is_skin_unlocked(skin_id, user):
            return False, "Скин уже разблокирован"
        
        skin_data = self.skin_library.get(skin_id)
        if not skin_data:
            return False, "Скин не найден"
        
        # Проверяем условия
        if not self.can_access_skin(skin_id, user):
            return False, "Скин недоступен"
        
        # Проверяем цену
        price = skin_data.get("price", 0)
        if price > 0:
            user_xp = user.get("xp", 0)
            if user_xp < price:
                return False, f"Недостаточно XP (нужно {price})"
            
            # Списываем XP
            user["xp"] = user_xp - price
        
        # Добавляем скин
        if "skins" not in user:
            user["skins"] = []
        
        user["skins"].append(skin_id)
        
        # Сохраняем обновления
        self.account_system.save_accounts(
            self.account_system.load_accounts()
        )
        
        return True, f"Скин '{skin_data['name']}' разблокирован!"
    
    def apply_skin_to_minecraft(self, skin_id):
        """Применение скина в Minecraft"""
        if not self.account_system.current_user:
            return False, "Требуется вход в аккаунт"
        
        skin_data = self.skin_library.get(skin_id)
        if not skin_data:
            return False, "Скин не найден"
        
        # Проверяем разблокирован ли скин
        if not self.is_skin_unlocked(skin_id, self.account_system.current_user):
            return False, "Скин не разблокирован"
        
        # Путь к файлу скина
        skin_file = os.path.join(self.skins_dir, skin_data["file"])
        if not os.path.exists(skin_file):
            return False, "Файл скина не найден"
        
        # Копируем скин в папку Minecraft
        minecraft_path = CrossPlatformSupport.get_minecraft_path()
        skins_path = os.path.join(minecraft_path, "skins")
        os.makedirs(skins_path, exist_ok=True)
        
        # Копируем файл
        import shutil
        shutil.copy2(skin_file, os.path.join(skins_path, "custom_skin.png"))
        
        # Обновляем настройки пользователя
        self.account_system.current_user["current_skin"] = skin_id
        
        return True, f"Скин '{skin_data['name']}' применен!"
    
    def upload_custom_skin(self, image_path):
        """Загрузка кастомного скина"""
        if not self.account_system.current_user:
            return False, "Требуется вход в аккаунт"
        
        # Проверяем файл
        if not os.path.exists(image_path):
            return False, "Файл не найден"
        
        # Проверяем размер и формат
        try:
            from PIL import Image
            img = Image.open(image_path)
            
            # Minecraft скины обычно 64x64 или 64x32
            if img.size not in [(64, 64), (64, 32)]:
                return False, "Неверный размер скина (должен быть 64x64 или 64x32)"
            
            # Сохраняем в папку пользователя
            user_folder = self.account_system.get_user_folder()
            user_skins_dir = os.path.join(user_folder, "skins")
            os.makedirs(user_skins_dir, exist_ok=True)
            
            # Генерируем имя файла
            skin_id = f"custom_{secrets.token_hex(8)}"
            skin_filename = f"{skin_id}.png"
            skin_path = os.path.join(user_skins_dir, skin_filename)
            
            # Копируем/конвертируем
            img.save(skin_path)
            
            # Добавляем в библиотеку пользователя
            self.account_system.current_user.setdefault("custom_skins", []).append({
                "id": skin_id,
                "name": "Мой скин",
                "file": skin_filename,
                "uploaded_at": datetime.datetime.now().isoformat()
            })
            
            return True, skin_id
            
        except Exception as e:
            return False, f"Ошибка обработки изображения: {e}"
        
# =========== ДОБАВИТЬ ПОСЛЕ SkinsManager ===========
class LoginDialog(QDialog):
    def __init__(self, account_system, parent=None):
        super().__init__(parent)
        self.account_system = account_system
        self.user_data = None

        self.setWindowTitle("👤 Вход / Регистрация")
        self.setFixedSize(440, 520)
        self.setStyleSheet("""
            QDialog {
                background: #121218;
                border-radius: 12px;
            }
            QLabel {
                color: #e8e8ee;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("⚡  SuperLauncher")
        title.setStyleSheet("""
            font-size: 20px; font-weight: 700; color: white;
            border: none; padding: 4px 0;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.tab_widget = QTabWidget()

        # Вкладка: Microsoft
        ms_tab = QWidget()
        self._setup_ms_tab(ms_tab)
        self.tab_widget.addTab(ms_tab, "Microsoft")

        # Вкладка: Ely.by
        ely_tab = QWidget()
        self._setup_ely_tab(ely_tab)
        self.tab_widget.addTab(ely_tab, "Ely.by")

        # Вкладка: Локальный вход
        login_tab = QWidget()
        self._setup_login_tab(login_tab)
        self.tab_widget.addTab(login_tab, "Вход")

        # Вкладка: Регистрация
        register_tab = QWidget()
        self._setup_register_tab(register_tab)
        self.tab_widget.addTab(register_tab, "Регистрация")

        # Вкладка: Офлайн
        offline_tab = QWidget()
        self._setup_offline_tab(offline_tab)
        self.tab_widget.addTab(offline_tab, "Офлайн")

        layout.addWidget(self.tab_widget)

        self.btn_cancel = QPushButton("Отмена")
        self.btn_cancel.setStyleSheet("background:#555; color:white; border:none; border-radius:4px; padding:8px;")
        self.btn_cancel.clicked.connect(self.reject)
        layout.addWidget(self.btn_cancel, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def _setup_ms_tab(self, tab):
        layout = QVBoxLayout(tab)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon = QLabel("🟦")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setStyleSheet("font-size: 48px;")
        layout.addWidget(icon)

        lbl = QLabel("Войди через Microsoft, чтобы играть\nс настоящим скином и достижениями")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet("color: #aaa; font-size: 13px;")
        layout.addWidget(lbl)

        self.ms_btn = QPushButton("🔵 Войти через Microsoft (код)")
        self.ms_btn.setStyleSheet("background:#2f2f2f; color:white; border:2px solid #4facfe; border-radius:8px; padding:12px; font-size:14px; font-weight:bold;")
        self.ms_btn.clicked.connect(self._ms_auth)
        layout.addWidget(self.ms_btn)

        self.ms_oauth_btn = QPushButton("🔵 Войти через браузер (OAuth 2.0 PKCE)")
        self.ms_oauth_btn.setStyleSheet("background:#2f2f2f; color:white; border:2px solid #4facfe; border-radius:8px; padding:12px; font-size:14px; font-weight:bold; margin-top:6px;")
        self.ms_oauth_btn.clicked.connect(self._ms_oauth_auth)
        layout.addWidget(self.ms_oauth_btn)

        self.ms_status = QLabel("")
        self.ms_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ms_status.setStyleSheet("color: #888; font-size: 12px;")
        self.ms_status.setWordWrap(True)
        layout.addWidget(self.ms_status)

        layout.addStretch()

    def _setup_ely_tab(self, tab):
        layout = QVBoxLayout(tab)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon = QLabel("🌿")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setStyleSheet("font-size: 48px;")
        layout.addWidget(icon)

        lbl = QLabel("Ely.by — бесплатная альтернатива\nMicrosoft-аккаунта для Minecraft")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet("color: #aaa; font-size: 13px;")
        layout.addWidget(lbl)

        self.ely_btn = QPushButton("🌿 Войти через Ely.by")
        self.ely_btn.setStyleSheet("background:#2f2f2f; color:white; border:2px solid #4caf50; border-radius:8px; padding:12px; font-size:14px; font-weight:bold;")
        self.ely_btn.clicked.connect(self._ely_auth)
        layout.addWidget(self.ely_btn)

        self.ely_status = QLabel("")
        self.ely_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ely_status.setStyleSheet("color: #888; font-size: 12px;")
        self.ely_status.setWordWrap(True)
        layout.addWidget(self.ely_status)

        layout.addStretch()

    def _setup_login_tab(self, tab):
        layout = QFormLayout(tab)

        self.login_username = QLineEdit()
        self.login_username.setPlaceholderText("Имя пользователя или Email")
        self.login_username.setStyleSheet("background:#2f2f2f; color:white; border:1px solid #444; border-radius:4px; padding:6px;")
        layout.addRow("Логин:", self.login_username)

        self.login_password = QLineEdit()
        self.login_password.setPlaceholderText("Пароль")
        self.login_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_password.setStyleSheet("background:#2f2f2f; color:white; border:1px solid #444; border-radius:4px; padding:6px;")
        layout.addRow("Пароль:", self.login_password)

        btn = QPushButton("Войти")
        btn.setStyleSheet("background:#4facfe; color:white; border:none; border-radius:4px; padding:8px; font-weight:bold;")
        btn.clicked.connect(self._perform_login)
        layout.addRow(btn)

    def _setup_register_tab(self, tab):
        layout = QFormLayout(tab)

        self.register_username = QLineEdit()
        self.register_username.setPlaceholderText("Придумайте имя")
        self.register_username.setStyleSheet("background:#2f2f2f; color:white; border:1px solid #444; border-radius:4px; padding:6px;")
        layout.addRow("Имя:", self.register_username)

        self.register_email = QLineEdit()
        self.register_email.setPlaceholderText("Ваш email")
        self.register_email.setStyleSheet("background:#2f2f2f; color:white; border:1px solid #444; border-radius:4px; padding:6px;")
        layout.addRow("Email:", self.register_email)

        self.register_password = QLineEdit()
        self.register_password.setPlaceholderText("Пароль")
        self.register_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.register_password.setStyleSheet("background:#2f2f2f; color:white; border:1px solid #444; border-radius:4px; padding:6px;")
        layout.addRow("Пароль:", self.register_password)

        self.register_password_confirm = QLineEdit()
        self.register_password_confirm.setPlaceholderText("Повторите пароль")
        self.register_password_confirm.setEchoMode(QLineEdit.EchoMode.Password)
        self.register_password_confirm.setStyleSheet("background:#2f2f2f; color:white; border:1px solid #444; border-radius:4px; padding:6px;")
        layout.addRow("Подтверждение:", self.register_password_confirm)

        btn = QPushButton("Зарегистрироваться")
        btn.setStyleSheet("background:#4facfe; color:white; border:none; border-radius:4px; padding:8px; font-weight:bold;")
        btn.clicked.connect(self._perform_register)
        layout.addRow(btn)

    def _setup_offline_tab(self, tab):
        layout = QVBoxLayout(tab)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon = QLabel("👤")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setStyleSheet("font-size: 48px;")
        layout.addWidget(icon)

        lbl = QLabel("Офлайн режим — без привязки к аккаунту.\nВведи любой ник и играй.")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet("color: #aaa; font-size: 13px;")
        layout.addWidget(lbl)

        self.offline_name = QLineEdit()
        self.offline_name.setPlaceholderText("Твой ник в игре")
        self.offline_name.setStyleSheet("background:#2f2f2f; color:white; border:1px solid #444; border-radius:6px; padding:10px; font-size:16px;")
        layout.addWidget(self.offline_name)

        btn = QPushButton("▶ Играть офлайн")
        btn.setStyleSheet("background:#ff9800; color:white; border:none; border-radius:6px; padding:10px; font-size:14px; font-weight:bold;")
        btn.clicked.connect(self._perform_offline)
        layout.addWidget(btn)

        layout.addStretch()

    def _ms_auth(self):
        cfg = load_config()
        client_id = cfg.get("azure_client_id", "").strip()
        if not client_id:
            client_id = "239ba7ac-4b4c-4597-82c2-c0c56735dba6"

        self.ms_btn.setEnabled(False)
        self.ms_status.setText("Запуск авторизации...")

        def task():
            try:
                dc = requests.post(
                    "https://login.microsoftonline.com/consumers/oauth2/v2.0/devicecode",
                    data={"client_id": client_id, "scope": "XboxLive.signin offline_access"},
                    timeout=10,
                )
                if dc.status_code != 200:
                    raise Exception(dc.json().get("error_description", dc.text[:100]))
                dc_data = dc.json()
                self.ms_status.setText(
                    f"Код: {dc_data['user_code']}\n"
                    f"Открой {dc_data['verification_uri']} и введи код\n"
                    f"Жду подтверждения..."
                )

                token = None
                for _ in range(120):
                    time.sleep(2)
                    tr = requests.post(
                        "https://login.microsoftonline.com/consumers/oauth2/v2.0/token",
                        data={
                            "client_id": client_id,
                            "device_code": dc_data["device_code"],
                            "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                        },
                        timeout=10,
                    )
                    if tr.status_code == 200:
                        token = tr.json()["access_token"]
                        break
                    elif tr.status_code == 400:
                        err = tr.json().get("error", "")
                        if err == "authorization_pending":
                            continue
                        elif err == "expired_token":
                            raise Exception("Время истекло, попробуй снова")
                        elif err == "authorization_declined":
                            raise Exception("Отменено пользователем")
                        else:
                            raise Exception(err)

                if not token:
                    raise Exception("Превышено время ожидания")

                # XBL auth
                xbl_r = requests.post(
                    "https://user.auth.xboxlive.com/user/authenticate",
                    json={
                        "Properties": {
                            "AuthMethod": "RPS",
                            "SiteName": "user.auth.xboxlive.com",
                            "RpsTicket": f"d={token}",
                        },
                        "RelyingParty": "http://auth.xboxlive.com",
                        "TokenType": "JWT",
                    },
                    timeout=10,
                )
                xbl_r.raise_for_status()
                xbl_data = xbl_r.json()

                # XSTS auth
                xsts_r = requests.post(
                    "https://xsts.auth.xboxlive.com/xsts/authorize",
                    json={
                        "Properties": {
                            "SandboxId": "RETAIL",
                            "UserTokens": [xbl_data["Token"]],
                        },
                        "RelyingParty": "rp://api.minecraftservices.com/",
                        "TokenType": "JWT",
                    },
                    timeout=10,
                )
                xsts_r.raise_for_status()
                xsts_token = xsts_r.json()["Token"]
                uhs = xbl_data["DisplayClaims"]["xui"][0]["uhs"]

                # Minecraft auth
                mc_r = requests.post(
                    "https://api.minecraftservices.com/authentication/login_with_xbox",
                    json={"identityToken": f"XBL3.0 x={uhs};{xsts_token}"},
                    timeout=10,
                )
                if mc_r.status_code == 403:
                    raise Exception(
                        "У этого Microsoft-аккаунта нет лицензии Minecraft.\n"
                        "Купи игру на minecraft.net, чтобы использовать Microsoft-скин и UUID.\n"
                        "Либо используй вкладку «Офлайн» для игры без лицензии."
                    )
                mc_r.raise_for_status()
                mc_token = mc_r.json()["access_token"]

                prof_r = requests.get(
                    "https://api.minecraftservices.com/minecraft/profile",
                    headers={"Authorization": f"Bearer {mc_token}"},
                    timeout=10,
                )
                if prof_r.status_code == 404:
                    raise Exception("Профиль Minecraft не найден")
                prof_r.raise_for_status()
                prof = prof_r.json()

                self.user_data = {
                    "user_id": prof["id"],
                    "username": prof["name"],
                    "email": f"msa_{prof['id'][:8]}@minecraft",
                    "auth_type": "microsoft",
                    "mc_token": mc_token,
                    "created_at": datetime.datetime.now().isoformat(),
                    "last_login": datetime.datetime.now().isoformat(),
                    "license_tier": "premium",
                    "xp": 0,
                    "level": 1,
                }
                QMetaObject.invokeMethod(self, "accept", Qt.ConnectionType.QueuedConnection)

            except Exception as e:
                self.ms_status.setText(f"Ошибка: {str(e)[:150]}")
            finally:
                self.ms_btn.setEnabled(True)

        threading.Thread(target=task, daemon=True).start()

    def _ms_oauth_auth(self):
        cfg = load_config()
        client_id = cfg.get("azure_client_id", "").strip()
        if not client_id:
            client_id = "239ba7ac-4b4c-4597-82c2-c0c56735dba6"

        self.ms_oauth_btn.setEnabled(False)
        self.ms_status.setText("Запуск браузерной авторизации...")

        def task():
            import socket
            from http.server import HTTPServer, BaseHTTPRequestHandler
            import urllib.parse
            import hashlib
            import base64

            try:
                # Find a free port
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.bind(("127.0.0.1", 0))
                port = s.getsockname()[1]
                s.close()

                # PKCE
                code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b"=").decode()
                code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest()).rstrip(b"=").decode()
                redirect_uri = f"http://127.0.0.1:{port}/callback"

                auth_url = (
                    f"https://login.microsoftonline.com/consumers/oauth2/v2.0/authorize"
                    f"?client_id={client_id}"
                    f"&response_type=code"
                    f"&redirect_uri={urllib.parse.quote(redirect_uri)}"
                    f"&scope={urllib.parse.quote('XboxLive.signin offline_access')}"
                    f"&code_challenge={code_challenge}"
                    f"&code_challenge_method=S256"
                    f"&response_mode=query"
                )

                result = {"code": None, "error": None}

                class CallbackHandler(BaseHTTPRequestHandler):
                    def log_message(self, fmt, *args):
                        pass
                    def do_GET(self):
                        parsed = urllib.parse.urlparse(self.path)
                        qs = urllib.parse.parse_qs(parsed.query)
                        if "code" in qs:
                            result["code"] = qs["code"][0]
                            self.send_response(200)
                            self.send_header("Content-Type", "text/html; charset=utf-8")
                            self.end_headers()
                            self.wfile.write("<html><body><h2>Авторизация завершена!</h2><p>Можешь закрыть это окно.</p></body></html>".encode("utf-8"))
                        elif "error" in qs:
                            result["error"] = qs.get("error_description", [qs["error"][0]])[0]
                            self.send_response(400)
                            self.send_header("Content-Type", "text/html; charset=utf-8")
                            self.end_headers()
                            self.wfile.write("<html><body><h2>Ошибка</h2><p>{}</p></body></html>".format(result['error']).encode("utf-8"))
                        else:
                            self.send_response(400)
                            self.end_headers()

                server = HTTPServer(("127.0.0.1", port), CallbackHandler)
                server.timeout = 120

                QTimer.singleShot(0, lambda: (webbrowser.open(auth_url), self.ms_status.setText("Ожидание подтверждения в браузере...")))

                while result["code"] is None and result["error"] is None:
                    server.handle_request()

                server.server_close()

                if result["error"]:
                    raise Exception(result["error"])

                auth_code = result["code"]

                # Exchange code for tokens
                tr = requests.post(
                    "https://login.microsoftonline.com/consumers/oauth2/v2.0/token",
                    data={
                        "client_id": client_id,
                        "code": auth_code,
                        "code_verifier": code_verifier,
                        "redirect_uri": redirect_uri,
                        "grant_type": "authorization_code",
                    },
                    timeout=10,
                )
                if tr.status_code != 200:
                    raise Exception(f"Token exchange error: {tr.json().get('error_description', tr.text[:200])}")
                token = tr.json()["access_token"]

                # XBL auth
                xbl_r = requests.post(
                    "https://user.auth.xboxlive.com/user/authenticate",
                    json={
                        "Properties": {"AuthMethod": "RPS", "SiteName": "user.auth.xboxlive.com", "RpsTicket": f"d={token}"},
                        "RelyingParty": "http://auth.xboxlive.com", "TokenType": "JWT",
                    },
                    timeout=10,
                )
                xbl_r.raise_for_status()
                xbl_data = xbl_r.json()

                # XSTS auth
                xsts_r = requests.post(
                    "https://xsts.auth.xboxlive.com/xsts/authorize",
                    json={
                        "Properties": {"SandboxId": "RETAIL", "UserTokens": [xbl_data["Token"]]},
                        "RelyingParty": "rp://api.minecraftservices.com/", "TokenType": "JWT",
                    },
                    timeout=10,
                )
                xsts_r.raise_for_status()
                xsts_data = xsts_r.json()

                # Minecraft login
                mc_r = requests.post(
                    "https://api.minecraftservices.com/authentication/login_with_xbox",
                    json={"identityToken": f"XBL3.0 x={xbl_data['DisplayClaims']['xui'][0]['uhs']};{xsts_data['Token']}"},
                    timeout=10,
                )
                mc_r.raise_for_status()
                mc_token = mc_r.json()["access_token"]

                # Profile
                prof_r = requests.get("https://api.minecraftservices.com/minecraft/profile",
                    headers={"Authorization": f"Bearer {mc_token}"}, timeout=10)
                if prof_r.status_code == 404:
                    raise Exception("Профиль Minecraft не найден (нет лицензии)")
                prof_r.raise_for_status()
                prof = prof_r.json()

                self.user_data = {
                    "user_id": prof["id"],
                    "username": prof["name"],
                    "email": f"msa_{prof['id'][:8]}@minecraft",
                    "auth_type": "microsoft",
                    "mc_token": mc_token,
                    "created_at": datetime.datetime.now().isoformat(),
                    "last_login": datetime.datetime.now().isoformat(),
                    "license_tier": "premium",
                    "xp": 0, "level": 1,
                }
                QMetaObject.invokeMethod(self, "accept", Qt.ConnectionType.QueuedConnection)

            except Exception as e:
                self.ms_status.setText(f"Ошибка: {str(e)[:150]}")
            finally:
                self.ms_oauth_btn.setEnabled(True)

        threading.Thread(target=task, daemon=True).start()

    def _ely_auth(self):
        self.ely_btn.setEnabled(False)
        self.ely_status.setText("Открываю браузер для авторизации...")
        def task():
            try:
                # OAuth2 device flow for Ely.by
                client_id = "superlauncher"
                r = requests.post("https://auth.ely.by/oauth2/device",
                    data={"client_id": client_id, "scope": "auth"})
                if r.status_code != 200:
                    raise Exception("Ely.by не отвечает")
                resp = r.json()
                device_code = resp["device_code"]
                user_code = resp["user_code"]
                verification_uri = resp["verification_uri"]

                self.ely_status.setText(f"Код: {user_code}\nОткрой {verification_uri} и введи код")

                # Poll
                for _ in range(120):
                    time.sleep(2)
                    pr = requests.post("https://auth.ely.by/oauth2/token",
                        data={
                            "client_id": client_id,
                            "device_code": device_code,
                            "grant_type": "urn:ietf:params:oauth:grant-type:device_code"
                        })
                    if pr.status_code == 200:
                        token_data = pr.json()
                        access_token = token_data["access_token"]
                        # Get profile
                        prof = requests.get("https://auth.ely.by/api/users/profile",
                            headers={"Authorization": f"Bearer {access_token}"})
                        if prof.status_code == 200:
                            p = prof.json()
                            user_data = {
                                "user_id": str(p["id"]),
                                "username": p["username"],
                                "email": p.get("email", f"ely_{p['id']}@ely.by"),
                                "auth_type": "elyby",
                                "ely_token": access_token,
                                "created_at": datetime.datetime.now().isoformat(),
                                "last_login": datetime.datetime.now().isoformat(),
                                "license_tier": "premium",
                                "xp": 0, "level": 1,
                            }
                            self.user_data = user_data
                            QMetaObject.invokeMethod(self, "accept", Qt.ConnectionType.QueuedConnection)
                            return
                        break
                    elif pr.status_code == 400:
                        err = pr.json().get("error", "")
                        if err == "authorization_pending":
                            continue
                        elif err == "expired_token":
                            raise Exception("Время вышло, попробуй снова")
                        else:
                            raise Exception(f"Ошибка: {err}")
                else:
                    raise Exception("Превышено время ожидания")
            except Exception as e:
                self.ely_status.setText(f"Ошибка: {str(e)[:100]}")
            finally:
                self.ely_btn.setEnabled(True)
        threading.Thread(target=task, daemon=True).start()

    def _perform_login(self):
        username = self.login_username.text().strip()
        password = self.login_password.text()
        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return
        success, result = self.account_system.login(username, password)
        if success:
            self.user_data = result
            self.accept()
        else:
            QMessageBox.critical(self, "Ошибка входа", result)

    def _perform_register(self):
        username = self.register_username.text().strip()
        email = self.register_email.text().strip()
        password = self.register_password.text()
        password_confirm = self.register_password_confirm.text()
        if not all([username, email, password, password_confirm]):
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return
        if password != password_confirm:
            QMessageBox.warning(self, "Ошибка", "Пароли не совпадают")
            return
        if len(password) < 6:
            QMessageBox.warning(self, "Ошибка", "Пароль должен быть не менее 6 символов")
            return
        success, result = self.account_system.register_user(username, email, password)
        if success:
            self.user_data = result
            self.accept()
        else:
            QMessageBox.critical(self, "Ошибка регистрации", result)

    def _perform_offline(self):
        name = self.offline_name.text().strip() or "Player"
        self.user_data = {
            "user_id": f"offline_{hashlib.md5(name.encode()).hexdigest()[:8]}",
            "username": name,
            "email": "",
            "auth_type": "offline",
            "created_at": datetime.datetime.now().isoformat(),
            "last_login": datetime.datetime.now().isoformat(),
            "license_tier": "free",
            "xp": 0, "level": 1,
        }
        self.accept()

    def get_user(self):
        return self.user_data
    
class AnimatedButton(QPushButton):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self._animation_progress = 0
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(45)

        self.animation = QPropertyAnimation(self, b"animation_progress")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)

    def get_animation_progress(self):
        return self._animation_progress

    def set_animation_progress(self, value):
        self._animation_progress = value
        self.update()

    animation_progress = pyqtProperty(float, get_animation_progress, set_animation_progress)

    def enterEvent(self, event):
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()
        super().leaveEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0, QColor("#667eea"))
        gradient.setColorAt(1, QColor("#764ba2"))

        if self._animation_progress > 0:
            bg_color = QColor(47, 47, 47)
            painter.setBrush(QBrush(bg_color))
            painter.setPen(QPen(QColor(79, 172, 254), 2))
            painter.drawRoundedRect(1, 1, self.width() - 2, self.height() - 2, 8, 8)

            fill_width = int(self.width() * self._animation_progress)
            painter.setBrush(QBrush(gradient))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(1, 1, fill_width, self.height() - 2, 8, 8)
        else:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(QColor(79, 172, 254), 2))
            painter.drawRoundedRect(1, 1, self.width() - 2, self.height() - 2, 8, 8)

        painter.setPen(QPen(QColor(255, 255, 255)))
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.text())
        painter.end()


class _SignalBridge(QObject):
    append = pyqtSignal(str, str)


class ContentManagerPage(QWidget):
    SOURCES = ["Локально", "Modrinth", "CurseForge"]
    _search_done = pyqtSignal(object, object, object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self._search_done.connect(self._show_results)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("📁 Управление контентом")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: white;")
        layout.addWidget(title)

        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; }
            QTabBar::tab { background: rgba(255,255,255,0.05); color: #ccc; padding: 10px 20px; border-radius: 6px; margin: 2px; }
            QTabBar::tab:selected { background: #4facfe; color: white; }
        """)
        layout.addWidget(tabs)

        # ─── Resourcepacks ───
        rp_tab = QWidget()
        rp_layout = QVBoxLayout(rp_tab)
        rp_header = QHBoxLayout()
        rp_open = QPushButton("📂 Открыть папку")
        rp_open.setStyleSheet("background:#444; color:white; padding:8px 16px; border-radius:6px;")
        rp_open.clicked.connect(lambda: self._open_dir("resourcepacks"))
        rp_header.addWidget(rp_open)
        rp_header.addStretch()
        rp_layout.addLayout(rp_header)
        rp_search_row = QHBoxLayout()
        self.rp_src = QComboBox()
        self.rp_src.addItems(self.SOURCES)
        self.rp_src.setStyleSheet("background:rgba(255,255,255,0.08); border:1px solid #555; border-radius:6px; padding:4px; color:white;")
        rp_search_row.addWidget(self.rp_src)
        self.rp_input = QLineEdit()
        self.rp_input.setPlaceholderText("🔍 Поиск ресурспаков...")
        self.rp_input.setStyleSheet("background:rgba(255,255,255,0.08); border:1px solid #555; border-radius:6px; padding:8px; color:white;")
        self.rp_input.returnPressed.connect(self._search_rp)
        rp_search_row.addWidget(self.rp_input, 1)
        rp_btn = QPushButton("Поиск")
        rp_btn.setStyleSheet("background:#4facfe; color:white; padding:8px 16px; border-radius:6px; font-weight:bold;")
        rp_btn.clicked.connect(self._search_rp)
        rp_search_row.addWidget(rp_btn)
        rp_layout.addLayout(rp_search_row)
        self.rp_list = QListWidget()
        self.rp_list.setStyleSheet("QListWidget{background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.1);border-radius:8px;color:white;}")
        self.rp_list.itemDoubleClicked.connect(lambda item: self._install_content_item(item, "resourcepacks"))
        rp_layout.addWidget(self.rp_list)
        tabs.addTab(rp_tab, "🎨 Ресурспаки")

        # ─── Shaders ───
        sh_tab = QWidget()
        sh_layout = QVBoxLayout(sh_tab)
        sh_header = QHBoxLayout()
        sh_open = QPushButton("📂 Открыть папку")
        sh_open.setStyleSheet("background:#444; color:white; padding:8px 16px; border-radius:6px;")
        sh_open.clicked.connect(lambda: self._open_dir("shaderpacks"))
        sh_header.addWidget(sh_open)
        sh_header.addStretch()
        sh_layout.addLayout(sh_header)
        sh_search_row = QHBoxLayout()
        self.sh_src = QComboBox()
        self.sh_src.addItems(self.SOURCES)
        self.sh_src.setStyleSheet("background:rgba(255,255,255,0.08); border:1px solid #555; border-radius:6px; padding:4px; color:white;")
        sh_search_row.addWidget(self.sh_src)
        self.sh_input = QLineEdit()
        self.sh_input.setPlaceholderText("🔍 Поиск шейдеров...")
        self.sh_input.setStyleSheet("background:rgba(255,255,255,0.08); border:1px solid #555; border-radius:6px; padding:8px; color:white;")
        self.sh_input.returnPressed.connect(self._search_sh)
        sh_search_row.addWidget(self.sh_input, 1)
        sh_btn = QPushButton("Поиск")
        sh_btn.setStyleSheet("background:#4facfe; color:white; padding:8px 16px; border-radius:6px; font-weight:bold;")
        sh_btn.clicked.connect(self._search_sh)
        sh_search_row.addWidget(sh_btn)
        sh_layout.addLayout(sh_search_row)
        self.sh_list = QListWidget()
        self.sh_list.setStyleSheet("QListWidget{background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.1);border-radius:8px;color:white;}")
        self.sh_list.itemDoubleClicked.connect(lambda item: self._install_content_item(item, "shaderpacks"))
        sh_layout.addWidget(self.sh_list)
        tabs.addTab(sh_tab, "🌈 Шейдеры")

        # ─── Worlds ───
        w_tab = QWidget()
        w_layout = QVBoxLayout(w_tab)
        w_header = QHBoxLayout()
        w_open = QPushButton("📂 Открыть папку")
        w_open.setStyleSheet("background:#444; color:white; padding:8px 16px; border-radius:6px;")
        w_open.clicked.connect(lambda: self._open_dir("saves"))
        w_header.addWidget(w_open)
        w_header.addStretch()
        w_layout.addLayout(w_header)
        w_search_row = QHBoxLayout()
        self.w_src = QComboBox()
        self.w_src.addItems(self.SOURCES)
        self.w_src.setStyleSheet("background:rgba(255,255,255,0.08); border:1px solid #555; border-radius:6px; padding:4px; color:white;")
        w_search_row.addWidget(self.w_src)
        self.w_input = QLineEdit()
        self.w_input.setPlaceholderText("🔍 Поиск миров...")
        self.w_input.setStyleSheet("background:rgba(255,255,255,0.08); border:1px solid #555; border-radius:6px; padding:8px; color:white;")
        self.w_input.returnPressed.connect(self._search_w)
        w_search_row.addWidget(self.w_input, 1)
        w_btn = QPushButton("Поиск")
        w_btn.setStyleSheet("background:#4facfe; color:white; padding:8px 16px; border-radius:6px; font-weight:bold;")
        w_btn.clicked.connect(self._search_w)
        w_search_row.addWidget(w_btn)
        w_layout.addLayout(w_search_row)
        self.w_list = QListWidget()
        self.w_list.setStyleSheet("QListWidget{background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.1);border-radius:8px;color:white;}")
        self.w_list.itemDoubleClicked.connect(lambda item: self._install_content_item(item, "saves"))
        self.w_list.itemClicked.connect(self._show_world_info)
        w_layout.addWidget(self.w_list)
        self.w_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.w_list.customContextMenuRequested.connect(self._world_context_menu)
        self.w_info = QLabel("")
        self.w_info.setStyleSheet("color: #aaa; font-size: 12px; padding: 8px; border: 1px solid rgba(255,255,255,0.1); border-radius: 6px;")
        self.w_info.setWordWrap(True)
        w_layout.addWidget(self.w_info)
        tabs.addTab(w_tab, "🌍 Миры")

        # ─── Skins ───
        sk_tab = QWidget()
        sk_layout = QVBoxLayout(sk_tab)
        sk_top = QHBoxLayout()
        self.skin_preview = QLabel("🎭")
        self.skin_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.skin_preview.setStyleSheet("font-size: 100px; background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.1); border-radius: 12px; min-width: 160px; min-height: 200px;")
        sk_top.addWidget(self.skin_preview)
        sk_info = QVBoxLayout()
        self.skin_name_label = QLabel("Скин не загружен")
        self.skin_name_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        sk_info.addWidget(self.skin_name_label)
        self.skin_upload_btn = QPushButton("📤 Загрузить скин")
        self.skin_upload_btn.setStyleSheet("background:#444; color:white; padding:8px 16px; border-radius:6px;")
        self.skin_upload_btn.clicked.connect(self._upload_skin)
        sk_info.addWidget(self.skin_upload_btn)
        self.skin_clear_btn = QPushButton("🗑 Сбросить скин")
        self.skin_clear_btn.setStyleSheet("background:#d9534f; color:white; padding:8px 16px; border-radius:6px;")
        self.skin_clear_btn.clicked.connect(self._clear_skin)
        sk_info.addWidget(self.skin_clear_btn)
        sk_info.addStretch()
        sk_top.addLayout(sk_info)
        sk_layout.addLayout(sk_top)
        tabs.addTab(sk_tab, "🎭 Скины")

        # ─── Screenshots ───
        sc_tab = QWidget()
        sc_layout = QVBoxLayout(sc_tab)
        sc_header = QHBoxLayout()
        sc_open = QPushButton("📂 Открыть папку скриншотов")
        sc_open.setStyleSheet("background:#444; color:white; padding:8px 16px; border-radius:6px;")
        sc_open.clicked.connect(lambda: self._open_dir("screenshots"))
        sc_header.addWidget(sc_open)
        sc_refresh = QPushButton("🔄 Обновить")
        sc_refresh.setStyleSheet("background:#444; color:white; padding:8px 16px; border-radius:6px;")
        sc_refresh.clicked.connect(lambda: self._refresh_local(self.sc_list, "screenshots"))
        sc_header.addWidget(sc_refresh)
        self.sc_upload_btn = QPushButton("🌐 Upload to Imgur")
        self.sc_upload_btn.setStyleSheet("background:#444; color:white; padding:8px 16px; border-radius:6px;")
        self.sc_upload_btn.clicked.connect(self._upload_screenshot_imgur)
        sc_header.addWidget(self.sc_upload_btn)
        sc_header.addStretch()
        sc_layout.addLayout(sc_header)
        self.sc_list = QListWidget()
        self.sc_list.setStyleSheet("QListWidget{background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.1);border-radius:8px;color:white;}")
        sc_layout.addWidget(self.sc_list)
        self.sc_preview = QLabel()
        self.sc_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sc_preview.setStyleSheet("font-size: 14px; color: #888; border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; min-height: 200px;")
        self.sc_preview.setText("Выберите скриншот для предпросмотра")
        sc_layout.addWidget(self.sc_preview)
        self.sc_list.itemClicked.connect(self._show_screenshot_preview)
        tabs.addTab(sc_tab, "📸 Скриншоты")

        QTimer.singleShot(200, self._refresh_all)

    def _show_screenshot_preview(self, item):
        data = item.data(Qt.ItemDataRole.UserRole)
        if data and data[0] == "local":
            fpath = data[1]
            if fpath.lower().endswith((".png", ".jpg", ".jpeg")):
                pixmap = QPixmap(fpath)
                if not pixmap.isNull():
                    pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                    self.sc_preview.setPixmap(pixmap)
                    return
        self.sc_preview.setText("Предпросмотр недоступен")

    def _upload_screenshot_imgur(self):
        item = self.sc_list.currentItem()
        if not item:
            QMessageBox.warning(self, "Upload", "Выберите скриншот из списка")
            return
        data = item.data(Qt.ItemDataRole.UserRole)
        if not data or data[0] != "local":
            QMessageBox.warning(self, "Upload", "Выберите локальный скриншот")
            return
        fpath = data[1]
        try:
            with open(fpath, "rb") as f:
                img_data = base64.b64encode(f.read()).decode()
            resp = requests.post(
                "https://api.imgur.com/3/image",
                headers={"Authorization": "Client-ID c1a8d1e48e5e4c7"},
                data={"image": img_data, "type": "base64"},
                timeout=30
            )
            if resp.status_code == 200:
                url = resp.json()["data"]["link"]
                QMessageBox.information(self, "Imgur", f"URL: {url}")
            else:
                QMessageBox.critical(self, "Ошибка", f"Imgur error: {resp.status_code}\n{resp.text[:200]}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить: {e}")

    def _show_world_info(self, item):
        data = item.data(Qt.ItemDataRole.UserRole)
        if not data or data[0] != "local":
            self.w_info.setText("")
            return
        world_path = data[1]
        name = os.path.basename(world_path)
        try:
            total_size = 0
            file_count = 0
            latest_mtime = 0
            if os.path.isdir(world_path):
                for root, dirs, files in os.walk(world_path):
                    for fn in files:
                        fp = os.path.join(root, fn)
                        try:
                            st = os.stat(fp)
                            total_size += st.st_size
                            file_count += 1
                            if st.st_mtime > latest_mtime:
                                latest_mtime = st.st_mtime
                        except:
                            pass
            else:
                st = os.stat(world_path)
                total_size = st.st_size
                file_count = 1
                latest_mtime = st.st_mtime
            sz_str = f"{total_size/1024/1024:.1f} MB" if total_size > 1024*1024 else f"{total_size/1024:.1f} KB"
            modified = datetime.datetime.fromtimestamp(latest_mtime).strftime("%d.%m.%Y %H:%M") if latest_mtime else "?"
            self.w_info.setText(f"📁 {name}\nРазмер: {sz_str}  |  Файлов: {file_count}  |  Изменён: {modified}")
        except Exception as e:
            self.w_info.setText(f"Ошибка: {e}")

    def _world_context_menu(self, pos):
        item = self.w_list.itemAt(pos)
        if not item:
            return
        data = item.data(Qt.ItemDataRole.UserRole)
        if not data or data[0] != "local":
            return
        world_path = data[1]
        world_name = os.path.basename(world_path)
        menu = QMenu(self)
        backup_action = menu.addAction("🗜 Backup world")
        action = menu.exec(self.w_list.mapToGlobal(pos))
        if action == backup_action:
            os.makedirs("user_data/backups", exist_ok=True)
            date_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_name = "".join(c for c in world_name if c.isalnum() or c in " _-").strip()
            backup_path = os.path.join("user_data", "backups", f"world_{safe_name}_{date_str}.zip")
            with zipfile.ZipFile(backup_path, "w", zipfile.ZIP_DEFLATED) as zf:
                for root, dirs, files in os.walk(world_path):
                    for fn in files:
                        fpath = os.path.join(root, fn)
                        arc = os.path.relpath(fpath, os.path.dirname(world_path))
                        zf.write(fpath, arc)
            QMessageBox.information(self, "Готово", f"Мир сохранён:\n{backup_path}")

    def _mc_dir(self):
        inst_id = getattr(self.parent_window, 'active_instance_id', None)
        if inst_id:
            return os.path.join(INSTANCES_DIR, inst_id, "game")
        return minecraft_directory

    def _open_dir(self, subdir):
        path = os.path.join(self._mc_dir(), subdir)
        os.makedirs(path, exist_ok=True)
        os.startfile(path)

    def _refresh_local(self, list_widget, subdir):
        list_widget.clear()
        path = os.path.join(self._mc_dir(), subdir)
        if not os.path.isdir(path):
            list_widget.addItem("(пусто)")
            return
        entries = sorted(os.listdir(path))
        if not entries:
            list_widget.addItem("(пусто)")
            return
        for entry in entries:
            full = os.path.join(path, entry)
            size = ""
            if os.path.isfile(full):
                sz = os.path.getsize(full)
                if sz > 1024*1024:
                    size = f" ({sz//1024//1024} MB)"
                elif sz > 1024:
                    size = f" ({sz//1024} KB)"
            elif os.path.isdir(full):
                size = " (папка)"
            item = QListWidgetItem(f"{entry}{size}")
            item.setData(Qt.ItemDataRole.UserRole, ("local", full))
            list_widget.addItem(item)

    def _search_rp(self):
        self._search_online("resourcepacks", self.rp_src, self.rp_input, self.rp_list)

    def _search_sh(self):
        self._search_online("shaderpacks", self.sh_src, self.sh_input, self.sh_list)

    def _search_w(self):
        self._search_online("saves", self.w_src, self.w_input, self.w_list)

    def _search_online(self, subdir, src_combo, search_input, list_widget):
        query = search_input.text().strip()
        source = src_combo.currentText()
        if source == "Локально":
            self._refresh_local(list_widget, subdir)
            return
        if not query:
            return

        list_widget.clear()
        list_widget.addItem("⏳ Поиск...")
        QApplication.processEvents()

        def task():
            lst = list_widget
            sd = subdir
            src = source
            q = query
            try:
                results = []
                if src == "Modrinth":
                    cat = "resourcepack" if sd == "resourcepacks" else ("shader" if sd == "shaderpacks" else "world")
                    facets = '[["project_type:' + cat + '"]]'
                    url = f"{MODRINTH_API}/search?query={urllib.parse.quote(q)}&facets={urllib.parse.quote(facets)}&limit=30"
                    r = requests.get(url, headers={"User-Agent": "SuperLauncher/2.0"}, timeout=10)
                    if r.status_code == 200:
                        for hit in r.json().get("hits", []):
                            results.append({
                                "id": hit["project_id"],
                                "name": hit["title"],
                                "desc": hit.get("description", "")[:120],
                                "downloads": hit.get("downloads", 0),
                                "author": hit.get("author", ""),
                                "icon": hit.get("icon_url", ""),
                                "source": "modrinth",
                            })
                else:
                    cat_map = {"resourcepacks": 12, "shaderpacks": 6552, "saves": 17}
                    class_id = cat_map.get(sd, 12)
                    r = requests.get(f"{CURSEFORGE_API}/mods/search?searchFilter={urllib.parse.quote(q)}&gameId=432&classId={class_id}&pageSize=25",
                        headers={"x-api-key": get_cf_api_key() or "default"}, timeout=10)
                    if r.status_code == 200:
                        for d in r.json().get("data", []):
                            results.append({
                                "id": d["id"],
                                "name": d["name"],
                                "desc": d.get("summary", "")[:120],
                                "downloads": d.get("downloadCount", 0),
                                "author": d.get("authors", [{}])[0].get("name", ""),
                                "icon": d.get("logo", {}).get("url", ""),
                                "source": "curseforge",
                            })
                self._search_done.emit(lst, results, sd)
            except Exception as e:
                self._search_done.emit(lst, [{"error": str(e)}], sd)

        threading.Thread(target=task, daemon=True).start()

    def _show_results(self, list_widget, results, subdir):
        list_widget.clear()
        if not results:
            list_widget.addItem("Ничего не найдено")
            return
        if len(results) == 1 and "error" in results[0]:
            list_widget.addItem(f"Ошибка: {results[0]['error']}")
            return
        for r in results:
            dl = r.get("downloads", 0)
            text = f"{r['name']}  ⬇ {dl:,}  👤 {r.get('author','?')}  — {r.get('desc','')}"
            item = QListWidgetItem(text)
            item.setData(Qt.ItemDataRole.UserRole, ("online", r, subdir))
            list_widget.addItem(item)

    def _install_content_item(self, item, subdir):
        data = item.data(Qt.ItemDataRole.UserRole)
        if not data:
            return
        kind = data[0]
        if kind == "local":
            return  # local items just for viewing
        content = data[1]
        target_subdir = data[2] if len(data) > 2 else subdir
        name = content.get("name", "Unknown")
        source = content.get("source", "modrinth")
        pid = content.get("id", "")

        self.rp_list.setFocus()  # just to dismiss any selection

        def fetch_and_install():
            try:
                file_url = None
                mc_ver = None
                if source == "modrinth":
                    r = requests.get(f"{MODRINTH_API}/project/{pid}/version", timeout=10)
                    if r.status_code == 200:
                        vers = r.json()
                        if vers:
                            v = vers[0]
                            for f in v.get("files", []):
                                if f.get("primary", False) or True:
                                    file_url = f["url"]
                                    break
                            if not file_url and v.get("files"):
                                file_url = v["files"][0]["url"]
                else:
                    r = requests.get(f"{CURSEFORGE_API}/mods/{pid}/files?pageSize=1",
                        headers={"x-api-key": get_cf_api_key() or "default"}, timeout=10)
                    if r.status_code == 200:
                        files = r.json().get("data", [])
                        if files:
                            file_url = files[0].get("downloadUrl", "")
                if not file_url:
                    raise Exception("Нет ссылки на скачивание")

                target_dir = os.path.join(self._mc_dir(), target_subdir)
                os.makedirs(target_dir, exist_ok=True)

                resp = requests.get(file_url, stream=True, timeout=120)
                resp.raise_for_status()

                fname = f"{name.replace(' ', '_').replace('/', '_')}.zip"
                save_path = os.path.join(target_dir, fname)
                with open(save_path, "wb") as f:
                    for chunk in resp.iter_content(8192):
                        if chunk:
                            f.write(chunk)

                QTimer.singleShot(0, lambda: (
                    QMessageBox.information(self, "Готово", f"«{name}» установлен в {target_subdir}"),
                    self._refresh_local(self._get_list_for(subdir), subdir)
                ))
            except Exception as e:
                QTimer.singleShot(0, lambda: QMessageBox.critical(self, "Ошибка", str(e)))

        threading.Thread(target=fetch_and_install, daemon=True).start()

    def _get_list_for(self, subdir):
        return {"resourcepacks": self.rp_list, "shaderpacks": self.sh_list, "saves": self.w_list}.get(subdir, self.rp_list)

    def _refresh_all(self):
        self._refresh_local(self.rp_list, "resourcepacks")
        self._refresh_local(self.sh_list, "shaderpacks")
        self._refresh_local(self.w_list, "saves")
        self._refresh_local(self.sc_list, "screenshots")
        self._load_skin()

    def _load_skin(self):
        skin_path = os.path.join(self._mc_dir(), "skins", "skin.png")
        if os.path.exists(skin_path):
            self.skin_name_label.setText("Скин установлен")
            pix = QPixmap(skin_path)
            if not pix.isNull():
                self.skin_preview.setPixmap(pix.scaled(140, 180, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            self.skin_name_label.setText("Скин не загружен")

    def _upload_skin(self):
        path, _ = QFileDialog.getOpenFileName(self, "Выбери скин (PNG)", "", "PNG (*.png)")
        if not path:
            return
        skin_dir = os.path.join(self._mc_dir(), "skins")
        os.makedirs(skin_dir, exist_ok=True)
        shutil.copy2(path, os.path.join(skin_dir, "skin.png"))
        self._load_skin()
        QMessageBox.information(self, "Готово", "Скин сохранён. Он будет использоваться в офлайн-режиме.")

    def _clear_skin(self):
        skin_path = os.path.join(self._mc_dir(), "skins", "skin.png")
        if os.path.exists(skin_path):
            os.remove(skin_path)
        self._load_skin()
        QMessageBox.information(self, "Готово", "Скин сброшен.")


class AIAgentPage(QWidget):
    OLLAMA_DEFAULT = "http://localhost:11434/v1"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.config = load_config()
        self._bridge = _SignalBridge()
        self._bridge.append.connect(self._on_append)
        self._quantum = False
        self._quantum_timer = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        title_row = QHBoxLayout()
        title = QLabel("🤖 AI Агент")
        title.setStyleSheet("font-size: 26px; font-weight: bold; color: white;")
        title_row.addWidget(title)

        self.quantum_btn = QPushButton("🧪 Квантовый режим")
        self.quantum_btn.setCheckable(True)
        self.quantum_btn.setFixedHeight(30)
        self.quantum_btn.setStyleSheet(
            "QPushButton { background: rgba(100,60,200,0.2); border: 1px solid #643cc8; "
            "border-radius: 14px; padding: 4px 14px; color: #b088ff; font-size: 11px; }"
            "QPushButton:checked { background: rgba(100,60,200,0.5); color: #d0bbff; }")
        self.quantum_btn.clicked.connect(self._toggle_quantum)
        title_row.addStretch()
        title_row.addWidget(self.quantum_btn)
        layout.addLayout(title_row)

        sf = QFrame()
        sf.setStyleSheet("QFrame { background: rgba(255,255,255,0.05); border-radius: 8px; padding: 8px; }")
        sl = QVBoxLayout(sf)

        r1 = QHBoxLayout()
        r1.addWidget(QLabel("API URL:"))
        saved = self.config.get("ai_api_url")
        if not saved:
            self.config["ai_api_url"] = self.OLLAMA_DEFAULT
            save_config(self.config)
        self.api_url = QLineEdit(self.config.get("ai_api_url", self.OLLAMA_DEFAULT))
        self.api_url.setStyleSheet("background: #2f2f2f; color: white; border: 1px solid #444; border-radius: 4px; padding: 4px;")
        r1.addWidget(self.api_url)
        sl.addLayout(r1)

        r2 = QHBoxLayout()
        r2.addWidget(QLabel("Model:"))
        self.model_box = QComboBox()
        self.model_box.setEditable(True)
        self.model_box.setStyleSheet("background: #2f2f2f; color: white; border: 1px solid #444; border-radius: 4px; padding: 3px;")
        self.model_box.addItems(["llama3.2:latest", "mistral:latest", "codellama:latest", "qwen2.5:latest"])
        self.model_box.setCurrentText(self.config.get("ai_model", "llama3.2:latest"))
        r2.addWidget(self.model_box)

        scan_btn = QPushButton("Scan")
        scan_btn.setFixedWidth(50)
        scan_btn.setStyleSheet("QPushButton { background: rgba(79,172,254,0.2); border: none; border-radius: 4px; color: #4facfe; font-size: 11px; } QPushButton:hover { background: rgba(79,172,254,0.3); }")
        scan_btn.clicked.connect(self._scan_ollama)
        r2.addWidget(scan_btn)

        key_lbl = QLabel("Key:")
        self.api_key = QLineEdit(self.config.get("ai_api_key", ""))
        self.api_key.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key.setStyleSheet("background: #2f2f2f; color: white; border: 1px solid #444; border-radius: 4px; padding: 4px;")
        self.api_key.setPlaceholderText("только для OpenAI/API")
        r2.addWidget(key_lbl)
        r2.addWidget(self.api_key, 1)
        sl.addLayout(r2)

        r3 = QVBoxLayout()
        sp_lbl = QLabel("System prompt (что ИИ знать должен):")
        sp_lbl.setStyleSheet("color: #aaa; font-size: 11px;")
        r3.addWidget(sp_lbl)
        self.system_prompt = QTextEdit()
        default_sp = self.config.get("ai_system_prompt",
            "Ты эксперт по Minecraft Java Edition. Отвечай только про Minecraft: "
            "моды, версии, краши, сервера, сборки, оптимизацию. "
            "Если советуешь мод — пиши его название в формате [MOD:НазваниеМода]. "
            "Если вопрос не про Minecraft — отвечай 'Я знаю только про Minecraft'.")
        self.system_prompt.setPlainText(default_sp)
        self.system_prompt.setMaximumHeight(50)
        self.system_prompt.setStyleSheet("background: #2f2f2f; color: white; border: 1px solid #444; border-radius: 4px; padding: 4px; font-size: 11px;")
        r3.addWidget(self.system_prompt)
        sl.addLayout(r3)

        btn_save = QPushButton("💾 Сохранить")
        btn_save.setStyleSheet("background: #4facfe; color: white; border: none; border-radius: 4px; padding: 6px;")
        btn_save.clicked.connect(self._save_settings)
        sl.addWidget(btn_save)
        layout.addWidget(sf)

        self.chat_browser = QTextBrowser()
        self.chat_browser.setStyleSheet("""
            QTextBrowser { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1);
                border-radius: 8px; color: #ccc; font-size: 13px; padding: 8px; }
        """)
        self.chat_browser.setOpenExternalLinks(False)
        self.chat_browser.setReadOnly(True)
        self.chat_browser.anchorClicked.connect(self._on_link_click)
        layout.addWidget(self.chat_browser, 1)

        inp = QHBoxLayout()
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Спроси у ИИ...")
        self.input_text.setMaximumHeight(60)
        self.input_text.setStyleSheet("background: #2f2f2f; color: white; border: 1px solid #444; border-radius: 8px; padding: 6px;")
        inp.addWidget(self.input_text)

        send_btn = QPushButton("➤")
        send_btn.setFixedSize(50, 50)
        send_btn.setStyleSheet("background: #4facfe; color: white; border: none; border-radius: 8px; font-size: 20px;")
        send_btn.clicked.connect(self._send_message)
        inp.addWidget(send_btn)
        layout.addLayout(inp)

        install_row = QHBoxLayout()
        self.install_input = QLineEdit()
        self.install_input.setPlaceholderText("Название мода (Iris, Sodium...)")
        self.install_input.setStyleSheet("background: #2f2f2f; color: white; border: 1px solid #444; border-radius: 6px; padding: 6px;")
        install_row.addWidget(self.install_input, 2)

        self.loader_box = QComboBox()
        self.loader_box.setStyleSheet("QComboBox { background: #2f2f2f; color: white; border: 1px solid #444; border-radius: 4px; padding: 4px; } QComboBox QAbstractItemView { background: #1a1a2e; color: white; }")
        self.loader_box.addItems(["fabric", "forge", "neoforge", "quilt"])
        install_row.addWidget(self.loader_box)

        self.mcver_box = QComboBox()
        self.mcver_box.setEditable(True)
        self.mcver_box.setStyleSheet("QComboBox { background: #2f2f2f; color: white; border: 1px solid #444; border-radius: 4px; padding: 4px; min-width: 70px; } QComboBox QAbstractItemView { background: #1a1a2e; color: white; }")
        self.mcver_box.addItems(["1.21.4", "1.21.1", "1.20.6", "1.20.4", "1.20.1", "1.19.4", "1.19.2", "1.18.2", "1.16.5"])
        install_row.addWidget(self.mcver_box)

        install_btn = QPushButton("⬇")
        install_btn.setFixedSize(36, 36)
        install_btn.setStyleSheet("QPushButton { background: #4caf50; color: white; border: none; border-radius: 6px; font-size: 16px; } QPushButton:hover { background: #5cbf60; }")
        install_btn.clicked.connect(self._install_mod)
        install_row.addWidget(install_btn)
        layout.addLayout(install_row)

        self._add_msg("system", "AI готов. Ollama: " + self.api_url.text().strip())

    def _add_msg(self, role, text):
        escaped = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
        if role == "ai":
            html = f'<div style="color: #8ab4ff; margin-bottom: 8px;"><b>🧠 AI:</b><br>{escaped}</div>'
        elif role == "user":
            html = f'<div style="color: #a8d8a8; margin-bottom: 8px;"><b>👤 Вы:</b><br>{escaped}</div>'
        else:
            html = f'<div style="color: #aaa; margin-bottom: 6px; font-style: italic;">⚡ {escaped}</div>'
        self.chat_browser.append(html)
        self.chat_browser.verticalScrollBar().setValue(self.chat_browser.verticalScrollBar().maximum())

    def _on_append(self, role, text):
        self._add_msg(role, text)
        if role == "ai":
            import re
            m = re.search(r'\[MOD:([^\]]+)\]', text)
            if m:
                self.install_input.setText(m.group(1).strip())
            else:
                matches = re.findall(r'\b[A-Z][a-z]+[A-Z][a-zA-Z0-9]+\b', text)
                for match in matches:
                    if len(match) > 3 and match.lower() not in ["the", "this", "that", "with", "from", "what", "have"]:
                        self.install_input.setText(match)
                        break

    def _remove_last_system(self):
        html = self.chat_browser.toHtml()
        idx = html.rfind('⚡ Думаю')
        if idx < 0:
            return
        end_idx = html.find('</div>', idx)
        if end_idx < 0:
            return
        html = html[:idx] + html[end_idx+6:]
        self.chat_browser.setHtml(html)
        self.chat_browser.verticalScrollBar().setValue(self.chat_browser.verticalScrollBar().maximum())

    def _save_settings(self):
        config = load_config()
        config["ai_api_url"] = self.api_url.text().strip()
        config["ai_api_key"] = self.api_key.text().strip()
        config["ai_model"] = self.model_box.currentText().strip()
        config["ai_system_prompt"] = self.system_prompt.toPlainText().strip()
        save_config(config)
        QMessageBox.information(self, "Готово", "Настройки AI сохранены")

    def _send_message(self):
        text = self.input_text.toPlainText().strip()
        if not text:
            return
        if hasattr(self, '_stream_timer') and self._stream_timer and self._stream_timer.isActive():
            self._stream_timer.stop()
        self.input_text.clear()
        self._add_msg("user", text)

        if self._quantum:
            prefixes = [
                "Представь что ты квантовый компьютер и ",
                "В контексте квантовой суперпозиции, ",
                "С точки зрения многомировой интерпретации, ",
            ]
            suffixes = [
                " в квантовом состоянии",
                " с учётом планковской длины",
                " в параллельной вселенной",
            ]
            import random
            text = random.choice(prefixes) + text + random.choice(suffixes)

        url = self.api_url.text().strip().rstrip("/") + "/chat/completions"
        model = self.model_box.currentText().strip()

        # Streaming state: thread puts chunks into _stream_chunks, timer drains them
        self._stream_chunks = []
        self._stream_done = False
        self._stream_error = ""
        self._add_msg("ai", "█")

        self._stream_timer = QTimer(self)
        self._stream_timer.timeout.connect(self._stream_tick)
        self._stream_timer.start(25)

        def task():
            try:
                headers = {"Content-Type": "application/json"}
                k = self.api_key.text().strip()
                if k:
                    headers["Authorization"] = f"Bearer {k}"
                sp = self.system_prompt.toPlainText().strip()
                msgs = []
                if sp:
                    msgs.append({"role": "system", "content": sp})
                msgs.append({"role": "user", "content": text})
                payload = {"model": model, "messages": msgs, "temperature": 0.7, "stream": True}
                r = requests.post(url, headers=headers, json=payload, timeout=300, stream=True)
                r.raise_for_status()
                for raw_line in r.iter_lines(decode_unicode=False):
                    if not raw_line:
                        continue
                    line = raw_line.decode('utf-8', errors='replace')
                    if line.startswith(":"):
                        continue
                    if line.startswith("data: "):
                        raw = line[6:]
                        if raw.strip() == "[DONE]":
                            break
                        try:
                            chunk = json.loads(raw)
                            delta = chunk.get("choices", [{}])[0].get("delta", {}).get("content", "")
                            if delta:
                                self._stream_chunks.append(delta)
                        except Exception:
                            pass
                self._stream_done = True
            except requests.exceptions.ConnectionError:
                self._stream_error = "Ошибка: Ollama не запущен. Запусти `ollama serve`"
                self._stream_done = True
            except Exception as e:
                self._stream_error = f"Ошибка: {str(e)[:120]}"
                self._stream_done = True

        threading.Thread(target=task, daemon=True).start()

    def _stream_tick(self):
        if self._stream_error:
            self._stream_timer.stop()
            html = self.chat_browser.toHtml().replace("█", "")
            self.chat_browser.setHtml(html)
            cursor = self.chat_browser.textCursor()
            cursor.movePosition(cursor.MoveOperation.End)
            cursor.insertText(self._stream_error)
            self._stream_error = ""
            self.chat_browser.verticalScrollBar().setValue(self.chat_browser.verticalScrollBar().maximum())
            return
        if not self._stream_chunks and not self._stream_done:
            return
        batch = []
        while self._stream_chunks:
            batch.append(self._stream_chunks.pop(0))
        if batch:
            text = "".join(batch)
            escaped = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            cursor = self.chat_browser.textCursor()
            cursor.movePosition(cursor.MoveOperation.End)
            cursor.insertText(escaped)
            self.chat_browser.verticalScrollBar().setValue(self.chat_browser.verticalScrollBar().maximum())
        if self._stream_done and not self._stream_chunks:
            self._stream_timer.stop()
            self._finalize_stream()

    def _finalize_stream(self):
        html = self.chat_browser.toHtml().replace("█", "")
        # Find the last AI response block and add clickable install links
        known = [
            "All the Mods", "ATM9", "ATMod", "Enigmatica", "RLCraft", "Valhelsia",
            "Create: Above", "SkyFactory", "FTB", "BetterF3", "OptiFine", "Sodium",
            "Iris", "Lithium", "Phosphor", "Starlight", "Mekanism", "Create",
            "Botania", "Twilight Forest", "JEI", "REI", "Hwyla", "Jade",
            "Modern UI", "Smooth Boot", "FerriteCore", "Krypton", "LazyDFU",
            "Cull Leaves", "Entity Culling", "Dynamic FPS",
        ]
        for name in known:
            if name in html:
                html = html.replace(name, f'<a href="install:{name}" style="color: #4facfe; text-decoration: underline;">{name}</a>', 1)
        self.chat_browser.setHtml(html)
        self.chat_browser.verticalScrollBar().setValue(self.chat_browser.verticalScrollBar().maximum())

    def _on_link_click(self, url):
        full = url.toString()
        if full.startswith("install:"):
            name = full[8:]
            self.install_input.setText(name)
            self._install_mod()
        elif full.startswith(("http://", "https://")):
            import webbrowser
            webbrowser.open(full)

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
                        self._bridge.append.emit("ai", f"Найдено: {', '.join(models[:5])}{'...' if len(models) > 5 else ''}")
                    else:
                        self._bridge.append.emit("ai", "Модели не найдены. Запусти `ollama pull llama3.2`")
                else:
                    self._bridge.append.emit("ai", f"Ollama ответил кодом {r.status_code}")
            except Exception as e:
                self._bridge.append.emit("ai", f"Ollama недоступен ({str(e)[:60]}). Убедись что ollama запущен")
        threading.Thread(target=task, daemon=True).start()

    def _install_mod(self):
        name = self.install_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введи название мода")
            return
        loader = self.loader_box.currentText().strip()
        mcver = self.mcver_box.currentText().strip()
        self.install_input.clear()
        self._add_msg("system", f"🔍 Ищу {name} для {loader} {mcver}...")

        def task():
            try:
                r = requests.get(
                    "https://api.modrinth.com/v2/search",
                    params={"query": name, "limit": 5, "facets": json.dumps([["project_type:mod"]])},
                    timeout=15
                )
                if r.status_code != 200:
                    self._bridge.append.emit("system", f"Modrinth ответил кодом {r.status_code}")
                    return
                hits = r.json().get("hits", [])
                if not hits:
                    self._bridge.append.emit("system", f"Мод '{name}' не найден на Modrinth")
                    return
                mod = hits[0]
                slug = mod.get("slug", "")
                self._bridge.append.emit("system", f"📦 {mod.get('title', name)} — {mod.get('description', '')[:100]}")

                if not slug:
                    return
                vr = requests.get(f"https://api.modrinth.com/v2/project/{slug}/version", timeout=10)
                if vr.status_code != 200:
                    return
                versions = vr.json()
                for v in versions:
                    ver_loaders = [l.lower() for l in v.get("loaders", [])]
                    ver_mc = v.get("game_versions", [])
                    if loader.lower() not in ver_loaders:
                        continue
                    if mcver not in ver_mc:
                        continue
                    for f in v.get("files", []):
                        url = f.get("url", "")
                        filename = f.get("filename", f"{slug}.jar")
                        if url:
                            self._bridge.append.emit("system", f"⬇ {filename}...")
                            dl = requests.get(url, timeout=60)
                            if dl.status_code == 200:
                                base = os.path.dirname(os.path.abspath(__file__))
                                mods_dir = os.path.join(base, "user_data", "mods")
                                os.makedirs(mods_dir, exist_ok=True)
                                with open(os.path.join(mods_dir, filename), "wb") as fh:
                                    fh.write(dl.content)
                                self._bridge.append.emit("system", f"✅ {filename} ({len(dl.content)//1024} KB)")
                            else:
                                self._bridge.append.emit("system", f"Ошибка {dl.status_code}")
                            return
                # Fallback: try first compatible loader
                for v in versions:
                    for f in v.get("files", []):
                        url = f.get("url", "")
                        filename = f.get("filename", f"{slug}.jar")
                        if url and filename.endswith(".jar"):
                            self._bridge.append.emit("system", f"⬇ {filename} ({', '.join(v.get('loaders',[]))} {', '.join(v.get('game_versions',[]))})...")
                            dl = requests.get(url, timeout=60)
                            if dl.status_code == 200:
                                base = os.path.dirname(os.path.abspath(__file__))
                                mods_dir = os.path.join(base, "user_data", "mods")
                                os.makedirs(mods_dir, exist_ok=True)
                                with open(os.path.join(mods_dir, filename), "wb") as fh:
                                    fh.write(dl.content)
                                self._bridge.append.emit("system", f"✅ {filename} ({len(dl.content)//1024} KB)")
                            else:
                                self._bridge.append.emit("system", f"Ошибка {dl.status_code}")
                            return
                self._bridge.append.emit("system", f"Нет версии {loader} {mcver} для этого мода")
            except Exception as e:
                self._bridge.append.emit("system", f"Ошибка: {str(e)[:100]}")

        threading.Thread(target=task, daemon=True).start()

    def _toggle_quantum(self, checked):
        self._quantum = checked
        if checked:
            self.quantum_btn.setText("🔮 Квантовый: ВКЛ")
            self._quantum_timer = QTimer(self)
            self._quantum_timer.timeout.connect(self._quantum_flash)
            self._quantum_timer.start(2000)
        else:
            self.quantum_btn.setText("🧪 Квантовый режим")
            if self._quantum_timer:
                self._quantum_timer.stop()
                self._quantum_timer = None

    def _quantum_flash(self):
        states = [
            "🌀 Суперпозиция: лаунчер одновременно открыт и закрыт",
            "⚛️ Квантовая запутанность: версия майнкрафта зависит от наблюдения",
            "🔬 Эффект наблюдателя: моды загружаются только если на них смотреть",
            "🌌 Туннелирование: скин проходит сквозь текстуры",
            "⚡ Планковская частота: тиков в секунду — 10⁴³",
            "🌀 Декогеренция: мир схлопнулся в волновую функцию",
        ]
        import random
        self._add_msg("system", random.choice(states))


class GlassFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("GlassFrame")
        self.setStyleSheet("""
            GlassFrame#GlassFrame {
                background: rgba(10, 10, 26, 0.75);
                border: 1px solid rgba(102, 126, 234, 0.15);
                border-radius: 24px;
            }
        """)


class InstanceDialog(QDialog):
    def __init__(self, parent=None, instance=None):
        super().__init__(parent)
        self.instance = instance
        self.setWindowTitle("Создать инстанс" if not instance else "Настройки инстанса")
        self.setFixedSize(520, 440)
        self.setStyleSheet("""
            QDialog { 
                background: #121218;
            } 
            QLabel { color: #e8e8ee; } 
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.name_edit = QLineEdit(instance["name"] if instance else "")
        self.name_edit.setStyleSheet("background:rgba(255,255,255,0.05); color:white; border:1px solid rgba(255,255,255,0.1); border-radius:8px; padding:8px;")
        form.addRow("Название:", self.name_edit)

        self.icon_edit = QLineEdit(instance["icon"] if instance else "📦")
        self.icon_edit.setStyleSheet("background:#2f2f2f; color:white; border:1px solid #444; border-radius:4px; padding:6px;")
        self.icon_edit.setMaxLength(2)
        form.addRow("Иконка:", self.icon_edit)

        self.version_combo = QComboBox()
        self.version_combo.setStyleSheet("background:#2f2f2f; color:white; border:1px solid #444; border-radius:4px; padding:4px;")
        try:
            from minecraft_launcher_lib.minecraft_utils import get_available_versions
            vers = get_available_versions(minecraft_directory)
            release_vers = [v["id"] for v in vers if v["type"] == "release"]
            snapshot_vers = [v["id"] for v in vers if v["type"] == "snapshot"]
            for v in release_vers:
                self.version_combo.addItem(v)
            if snapshot_vers:
                self.version_combo.insertSeparator(len(release_vers))
                for v in snapshot_vers:
                    self.version_combo.addItem(v)
        except Exception:
            self.version_combo.addItem("latest_release")
        if instance and instance["mc_version"]:
            idx = self.version_combo.findText(instance["mc_version"])
            if idx >= 0:
                self.version_combo.setCurrentIndex(idx)
        form.addRow("Версия MC:", self.version_combo)

        self.loader_combo = QComboBox()
        self.loader_combo.addItems(["Vanilla", "Fabric", "Forge", "Quilt", "NeoForge", "OptiFine"])
        self.loader_combo.setStyleSheet("background:#2f2f2f; color:white; border:1px solid #444; border-radius:4px; padding:4px;")
        if instance and instance["loader"]:
            idx = self.loader_combo.findText(instance["loader"])
            if idx >= 0:
                self.loader_combo.setCurrentIndex(idx)
        form.addRow("Загрузчик:", self.loader_combo)

        self.ram_spin = QSpinBox()
        self.ram_spin.setRange(512, 32768)
        self.ram_spin.setSingleStep(512)
        self.ram_spin.setValue(instance["max_ram"] if instance else 4096)
        self.ram_spin.setSuffix(" MB")
        self.ram_spin.setStyleSheet("background:#2f2f2f; color:white; border:1px solid #444; border-radius:4px; padding:4px;")
        form.addRow("ОЗУ:", self.ram_spin)

        layout.addLayout(form)

        self.java_edit = QLineEdit(instance["java_path"] if instance else "")
        self.java_edit.setPlaceholderText("Путь к Java (оставь пустым для авто)")
        self.java_edit.setStyleSheet("background:#2f2f2f; color:white; border:1px solid #444; border-radius:4px; padding:6px;")
        layout.addWidget(QLabel("Путь к Java:"))
        layout.addWidget(self.java_edit)

        self.jvm_edit = QLineEdit(instance["jvm_args"] if instance else "")
        self.jvm_edit.setPlaceholderText("Доп. JVM аргументы (например -XX:+UseG1GC)")
        self.jvm_edit.setStyleSheet("background:#2f2f2f; color:white; border:1px solid #444; border-radius:4px; padding:6px;")
        layout.addWidget(QLabel("JVM аргументы:"))
        layout.addWidget(self.jvm_edit)

        btns = QHBoxLayout()
        cancel_btn = QPushButton("Отмена")
        cancel_btn.setStyleSheet("background:#444; color:white; border:none; border-radius:4px; padding:8px;")
        cancel_btn.clicked.connect(self.reject)

        ok_btn = QPushButton("Сохранить" if instance else "Создать")
        ok_btn.setStyleSheet("background:#4facfe; color:white; border:none; border-radius:4px; padding:8px; font-weight:bold;")
        ok_btn.clicked.connect(self.accept)

        btns.addStretch()
        btns.addWidget(cancel_btn)
        btns.addWidget(ok_btn)
        layout.addLayout(btns)

    def get_data(self):
        return {
            "name": self.name_edit.text().strip() or "Новый инстанс",
            "icon": self.icon_edit.text().strip() or "📦",
            "mc_version": self.version_combo.currentText(),
            "loader": self.loader_combo.currentText(),
            "max_ram": self.ram_spin.value(),
            "java_path": self.java_edit.text().strip(),
            "jvm_args": self.jvm_edit.text().strip(),
        }


class InstanceCard(QFrame):
    play_clicked = pyqtSignal(object)
    settings_clicked = pyqtSignal(object)
    delete_clicked = pyqtSignal(object)
    export_clicked = pyqtSignal(object)
    publish_clicked = pyqtSignal(object)
    clone_clicked = pyqtSignal(object)
    backup_clicked = pyqtSignal(object)
    restore_clicked = pyqtSignal(object)

    def __init__(self, instance, parent=None):
        super().__init__(parent)
        self.instance = instance
        self.setFixedSize(180, 180)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setStyleSheet("""
            InstanceCard {
                background: #1a1a24;
                border: 1px solid rgba(255,255,255,0.04);
                border-radius: 8px;
            }
            InstanceCard:hover {
                background: #1e1e2a;
                border-color: rgba(168,85,247,0.08);
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(3)
        layout.setContentsMargins(8, 8, 8, 8)

        self.icon_label = QLabel(instance.get("icon", "📦"))
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setStyleSheet("font-size: 28px; background: transparent; padding: 2px;")
        layout.addWidget(self.icon_label)

        self.name_label = QLabel(instance["name"])
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_label.setStyleSheet("font-size: 12px; font-weight: 600; color: white; background: transparent;")
        self.name_label.setWordWrap(True)
        layout.addWidget(self.name_label)

        info = f"{instance['mc_version']} · {instance['loader']}"
        self.info_label = QLabel(info)
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label.setStyleSheet("font-size: 10px; color: rgba(255,255,255,0.25); background: transparent;")
        layout.addWidget(self.info_label)

        last = instance.get("last_played", "")
        if last:
            try:
                dt = datetime.datetime.fromisoformat(last)
                days = (datetime.datetime.now() - dt).days
                last_str = f"{days}d" if days > 0 else "today"
            except Exception:
                last_str = ""
        else:
            last_str = "never"
        self.last_label = QLabel(last_str)
        self.last_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.last_label.setStyleSheet("font-size: 9px; color: rgba(255,255,255,0.15); background: transparent;")
        layout.addWidget(self.last_label)

        btn_row = QHBoxLayout()
        btn_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        btn_row.setSpacing(3)
        btn_row.setContentsMargins(0, 3, 0, 0)

        def make_btn(text, tip):
            b = QPushButton(text)
            b.setFixedSize(24, 22)
            b.setToolTip(tip)
            b.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            b.setStyleSheet("""
                QPushButton {
                    background: rgba(255,255,255,0.03);
                    color: rgba(255,255,255,0.45);
                    border: none;
                    border-radius: 4px;
                    font-size: 10px;
                }
                QPushButton:hover {
                    background: rgba(168,85,247,0.08);
                    color: white;
                }
            """)
            return b

        play_btn = make_btn("▶", "Launch")
        play_btn.clicked.connect(lambda: self.play_clicked.emit(self.instance))
        set_btn = make_btn("⚙", "Settings")
        set_btn.clicked.connect(lambda: self.settings_clicked.emit(self.instance))
        clone_btn = make_btn("📋", "Clone")
        clone_btn.clicked.connect(lambda: self.clone_clicked.emit(self.instance))
        backup_btn = make_btn("💾", "Backup")
        backup_btn.clicked.connect(lambda: self.backup_clicked.emit(self.instance))
        del_btn = make_btn("✕", "Delete")
        del_btn.clicked.connect(lambda: self.delete_clicked.emit(self.instance))

        btn_row.addWidget(play_btn)
        btn_row.addWidget(set_btn)
        btn_row.addWidget(clone_btn)
        btn_row.addWidget(backup_btn)
        btn_row.addWidget(del_btn)
        layout.addLayout(btn_row)


class ModrinthPublishDialog(QDialog):
    def __init__(self, instance, parent=None):
        super().__init__(parent)
        self.instance = instance
        self.setWindowTitle("Опубликовать на Modrinth")
        self.setFixedSize(500, 480)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        title = QLabel(f"📦 {instance['name']}")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
        layout.addWidget(title)

        layout.addWidget(QLabel("API токен (создай на modrinth.com/settings/feeds)"))
        self.token_input = QLineEdit()
        self.token_input.setPlaceholderText("mrp_...")
        layout.addWidget(self.token_input)

        layout.addWidget(QLabel("Project ID (оставь пустым для новой публикации)"))
        self.project_input = QLineEdit()
        self.project_input.setPlaceholderText("AABBCCDD (необязательно)")
        layout.addWidget(self.project_input)

        layout.addWidget(QLabel("Название версии"))
        self.name_input = QLineEdit()
        self.name_input.setText(f"{instance['name']} {datetime.datetime.now().strftime('%Y-%m-%d')}")
        layout.addWidget(self.name_input)

        layout.addWidget(QLabel("Номер версии"))
        self.version_input = QLineEdit()
        self.version_input.setText("1.0.0")
        layout.addWidget(self.version_input)

        layout.addWidget(QLabel("Тип релиза"))
        self.release_combo = QComboBox()
        self.release_combo.addItems(["Release", "Beta", "Alpha"])
        layout.addWidget(self.release_combo)

        layout.addWidget(QLabel("Список изменений"))
        self.changelog_input = QTextEdit()
        self.changelog_input.setPlaceholderText("Описание изменений...")
        self.changelog_input.setMaximumHeight(100)
        layout.addWidget(self.changelog_input)

        btn_layout = QHBoxLayout()
        btn_cancel = QPushButton("Отмена")
        btn_cancel.clicked.connect(self.reject)
        btn_ok = QPushButton("📤 Опубликовать")
        btn_ok.clicked.connect(self.accept)
        btn_ok.setStyleSheet("background:#7b1fa2; color:white; padding:8px 16px; border-radius:6px;")
        btn_layout.addStretch()
        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_ok)
        layout.addLayout(btn_layout)

        style = """
            QLineEdit, QTextEdit, QComboBox {
                background: rgba(255,255,255,0.08);
                border: 1px solid #555;
                border-radius: 6px;
                padding: 8px;
                color: white;
                font-size: 13px;
            }
            QLabel {
                color: #ccc;
                font-size: 12px;
            }
        """
        self.setStyleSheet(style)


class InstancesPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        header = QHBoxLayout()
        title = QLabel("📦 Инстансы")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: white;")
        header.addWidget(title)
        header.addStretch()

        self.log_btn = QPushButton("📋 Логи")
        self.log_btn.setStyleSheet("background:#5bc0de; color:white; border:none; border-radius:6px; padding:8px 14px; font-weight:bold;")
        self.log_btn.clicked.connect(self._open_log_viewer)
        header.addWidget(self.log_btn)

        self.import_btn = QPushButton("📂 Импорт")
        self.import_btn.setStyleSheet("background:#f0ad4e; color:white; border:none; border-radius:6px; padding:8px 14px; font-weight:bold;")
        self.import_btn.clicked.connect(self._import_modpack)
        header.addWidget(self.import_btn)

        self.create_btn = QPushButton("＋ Создать")
        self.create_btn.setStyleSheet("background:#4facfe; color:white; border:none; border-radius:6px; padding:8px 14px; font-weight:bold;")
        self.create_btn.clicked.connect(self._create_instance)
        header.addWidget(self.create_btn)

        layout.addLayout(header)

        # Search panel
        search_row = QHBoxLayout()
        self.search_source = QComboBox()
        self.search_source.addItems(["Modrinth", "CurseForge", "FTB", "Technic"])
        self.search_source.setStyleSheet("background:#2f2f2f; color:white; border:1px solid #444; border-radius:4px; padding:4px;")
        search_row.addWidget(self.search_source)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Найти сборку (All the Mods, RLCraft...)")
        self.search_input.setStyleSheet("background:#2f2f2f; color:white; border:1px solid #444; border-radius:6px; padding:8px;")
        self.search_input.returnPressed.connect(self._search_builds)
        search_row.addWidget(self.search_input, 1)

        self.search_btn = QPushButton("Поиск")
        self.search_btn.setStyleSheet("background:#4facfe; color:white; border:none; border-radius:6px; padding:8px 16px; font-weight:bold;")
        self.search_btn.clicked.connect(self._search_builds)
        search_row.addWidget(self.search_btn)

        self.search_results = QListWidget()
        self.search_results.setStyleSheet("""
            QListWidget { background: rgba(0,0,0,0.3); border: 1px solid #444; border-radius:6px; color:white; font-size:13px; }
            QListWidget::item { padding:8px; border-bottom:1px solid #333; }
            QListWidget::item:hover { background: rgba(79,172,254,0.15); }
        """)
        self.search_results.setMaximumHeight(300)
        self.search_results.setVisible(False)
        self.search_results.itemDoubleClicked.connect(self._install_build_from_search)

        layout.addLayout(search_row)
        layout.addWidget(self.search_results)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        self.container = QWidget()
        self.container.setStyleSheet("background: transparent;")
        self.grid = QGridLayout(self.container)
        self.grid.setSpacing(12)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.scroll.setWidget(self.container)
        layout.addWidget(self.scroll, 1)

    def showEvent(self, event):
        super().showEvent(event)
        self._refresh()

    def _search_builds(self):
        query = self.search_input.text().strip()
        if not query:
            return
        source = self.search_source.currentText().lower()
        self.search_results.clear()
        self.search_btn.setEnabled(False)
        self.search_btn.setText("Поиск...")

        def task():
            try:
                results = []
                if source == "modrinth":
                    r = requests.get(f"https://api.modrinth.com/v2/search?query={urllib.parse.quote(query)}&facets=[[%22project_type:modpack%22]]&limit=25", timeout=10)
                    if r.status_code == 200:
                        for hit in r.json().get("hits", []):
                            results.append({
                                "id": hit["project_id"],
                                "name": hit["title"],
                                "desc": hit.get("description", "")[:120],
                                "downloads": hit.get("downloads", 0),
                                "icon": hit.get("icon_url", ""),
                                "author": hit.get("author", ""),
                                "source": "modrinth",
                            })
                elif source == "curseforge":
                    r = requests.get(f"https://api.curseforge.com/v1/mods/search?searchFilter={urllib.parse.quote(query)}&gameId=432&classId=4471&pageSize=25",
                        headers={"x-api-key": get_cf_api_key() or "default"}, timeout=10)
                    if r.status_code == 200:
                        for d in r.json().get("data", []):
                            results.append({
                                "id": d["id"],
                                "name": d["name"],
                                "desc": d.get("summary", "")[:120],
                                "downloads": d.get("downloadCount", 0),
                                "icon": d.get("logo", {}).get("url", ""),
                                "author": d.get("authors", [{}])[0].get("name", ""),
                                "source": "curseforge",
                            })
                elif source == "ftb":
                    # FTB modpacks via modpacks.ch API
                    r = requests.get(f"https://api.modpacks.ch/public/modpack/search/{urllib.parse.quote(query)}", timeout=10)
                    if r.status_code == 200:
                        data = r.json()
                        packs = data if isinstance(data, list) else data.get("packs", [])
                        for p in packs[:25]:
                            results.append({
                                "id": str(p.get("id", "")),
                                "name": p.get("name", "Unknown"),
                                "desc": p.get("synopsis", "")[:120],
                                "downloads": p.get("downloads", 0),
                                "icon": f"https://api.modpacks.ch/public/modpack/{p.get('id')}/icon/256",
                                "author": "FTB Team",
                                "source": "ftb",
                            })
                elif source == "technic":
                    # Technic platform
                    r = requests.get(f"https://api.technicpack.net/feed/search?q={urllib.parse.quote(query)}", timeout=10)
                    if r.status_code == 200:
                        data = r.json()
                        for p in data.get("results", [])[:25]:
                            results.append({
                                "id": p.get("slug", ""),
                                "name": p.get("name", p.get("slug", "Unknown")),
                                "desc": (p.get("description", "") or "")[:120],
                                "downloads": p.get("downloads", 0),
                                "icon": p.get("icon", {}).get("url", ""),
                                "author": p.get("author", ""),
                                "source": "technic",
                            })
                # Emit results back to UI thread
                self._bridge = getattr(self, '_bridge', None)
                if not self._bridge:
                    class B(QObject):
                        done = pyqtSignal(list)
                    self._bridge = B()
                    self._bridge.done.connect(self._show_search_results)
                self._bridge.done.emit(results)
            except Exception as e:
                self._bridge.done.emit([{"error": str(e)}])

        threading.Thread(target=task, daemon=True).start()

    def _show_search_results(self, results):
        self.search_btn.setEnabled(True)
        self.search_btn.setText("Поиск")
        self.search_results.clear()
        if not results:
            self.search_results.addItem("Ничего не найдено")
            self.search_results.setVisible(True)
            return
        if len(results) == 1 and "error" in results[0]:
            self.search_results.addItem(f"Ошибка: {results[0]['error']}")
            self.search_results.setVisible(True)
            return
        for r in results:
            dl = r.get("downloads", 0)
            name = r["name"]
            desc = r.get("desc", "")
            author = r.get("author", "")
            text = f"{name}  ⬇{dl:,}  👤{author}"
            if desc:
                text += f"  — {desc}"
            item = QListWidgetItem(text)
            item.setData(Qt.ItemDataRole.UserRole, r)
            self.search_results.addItem(item)
        self.search_results.setVisible(True)

    def _install_build_from_search(self, item):
        data = item.data(Qt.ItemDataRole.UserRole)
        if not data or "error" in data:
            return
        name = data["name"]
        source = data["source"]
        pid = data["id"]

        # Fetch versions
        try:
            if source == "modrinth":
                r = requests.get(f"https://api.modrinth.com/v2/project/{pid}/version", timeout=10)
                if r.status_code != 200:
                    raise Exception("API error")
                versions = r.json()
                if not versions:
                    raise Exception("Нет версий")
                latest = versions[0]
                mc_vers = latest.get("game_versions", [])
                loaders = latest.get("loaders", [])
                mc_ver = mc_vers[0] if mc_vers else "latest_release"
                loader = loaders[0].capitalize() if loaders else "Vanilla"
                file_url = None
                for f in latest.get("files", []):
                    if f.get("primary", False):
                        file_url = f["url"]
                        break
                if not file_url and latest.get("files"):
                    file_url = latest["files"][0]["url"]
            elif source == "curseforge":
                r = requests.get(f"https://api.curseforge.com/v1/mods/{pid}/files?pageSize=1",
                    headers={"x-api-key": get_cf_api_key() or "default"}, timeout=10)
                if r.status_code != 200:
                    raise Exception("API error")
                files = r.json().get("data", [])
                if not files:
                    raise Exception("Нет файлов")
                f = files[0]
                mc_vers = [v for v in f.get("gameVersions", []) if v[0].isdigit()]
                loaders = []
                LOADER_MAP = {1: "Forge", 2: "Cauldron", 3: "LiteLoader", 4: "Fabric", 5: "Quilt", 6: "NeoForge"}
                for sgv in f.get("sortableGameVersions", []):
                    if sgv.get("gameVersionTypeId") == 2:
                        gv = sgv.get("gameVersionName", "")
                        if gv.isdigit():
                            loaders.append(LOADER_MAP.get(int(gv), "Forge"))
                mc_ver = mc_vers[0] if mc_vers else "latest_release"
                loader = loaders[0] if loaders else "Forge"
                file_url = f.get("downloadUrl", "")
            elif source == "ftb":
                # FTB: fetch modpack versions
                r = requests.get(f"https://api.modpacks.ch/public/modpack/{pid}", timeout=10)
                if r.status_code != 200:
                    raise Exception("API error")
                pack_data = r.json()
                versions = pack_data.get("versions", [])
                if not versions:
                    raise Exception("Нет версий")
                latest = versions[-1]
                mc_ver = latest.get("minecraft", "latest_release")
                loader = "Forge"
                file_id = latest.get("id", "")
                file_url = f"https://api.modpacks.ch/public/modpack/{pid}/{file_id}"
                name = pack_data.get("name", name)
            elif source == "technic":
                r = requests.get(f"https://api.technicpack.net/modpack/{pid}", timeout=10)
                if r.status_code != 200:
                    raise Exception("API error")
                pack_data = r.json()
                mc_ver = pack_data.get("minecraft", "latest_release")
                loader = pack_data.get("forge", "Forge")
                file_url = pack_data.get("url", "")
                if not file_url:
                    raise Exception("Нет ссылки на скачивание")

            if not file_url:
                raise Exception("Нет ссылки на скачивание")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось получить информацию о сборке:\n{e}")
            return

        # Create instance
        inst = create_instance(name=name, mc_version=mc_ver, loader=loader)
        inst_dir = os.path.join(INSTANCES_DIR, inst["id"], "game")

        # Download and extract
        QMessageBox.information(self, "Установка", f"Скачиваю и распаковываю «{name}»...\nЭто может занять время.")
        try:
            resp = requests.get(file_url, stream=True, timeout=120)
            resp.raise_for_status()
            import zipfile
            import io
            zf = zipfile.ZipFile(io.BytesIO(resp.content))
            zf.extractall(inst_dir)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось установить сборку:\n{e}")
            return

        instances = load_instances()
        instances.append(inst)
        save_instances(instances)
        self.search_results.setVisible(False)
        self._refresh()
        QMessageBox.information(self, "Готово", f"Сборка «{name}» установлена как инстанс!\nВерсия: {mc_ver}, загрузчик: {loader}")

    def _refresh(self):
        for i in reversed(range(self.grid.count())):
            w = self.grid.itemAt(i).widget()
            if w:
                w.deleteLater()
        instances = load_instances()
        if not instances:
            empty = QLabel("Нет инстансов. Нажми «＋ Создать» чтобы добавить.")
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty.setStyleSheet("color:#666; font-size:16px; padding:60px;")
            self.grid.addWidget(empty, 0, 0)
            return
        cols = max(1, (self.width() - 40) // 210)
        for i, inst in enumerate(instances):
            card = InstanceCard(inst)
            card.play_clicked.connect(self._play_instance)
            card.settings_clicked.connect(self._edit_instance)
            card.delete_clicked.connect(self._delete_instance)
            card.export_clicked.connect(self._export_instance)
            card.clone_clicked.connect(self._clone_instance)
            card.backup_clicked.connect(self._backup_instance)
            card.restore_clicked.connect(self._restore_instance)
            card.publish_clicked.connect(self._publish_modrinth)
            self.grid.addWidget(card, i // cols, i % cols)

    def _create_instance(self):
        dlg = InstanceDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            data = dlg.get_data()
            inst = create_instance(
                name=data["name"],
                mc_version=data["mc_version"],
                loader=data["loader"],
                icon=data["icon"],
            )
            inst["max_ram"] = data["max_ram"]
            inst["java_path"] = data["java_path"]
            inst["jvm_args"] = data["jvm_args"]
            instances = load_instances()
            instances.append(inst)
            save_instances(instances)
            self._refresh()

    def _edit_instance(self, inst):
        instances = load_instances()
        found = None
        for i, x in enumerate(instances):
            if x["id"] == inst["id"]:
                found = i
                break
        if found is None:
            return
        dlg = InstanceDialog(self, instance=instances[found])
        if dlg.exec() == QDialog.DialogCode.Accepted:
            data = dlg.get_data()
            instances[found].update(data)
            save_instances(instances)
            self._refresh()

    def _delete_instance(self, inst):
        ok = QMessageBox.question(self, "Удаление",
            f"Удалить инстанс «{inst['name']}»?\nВсе файлы игры будут удалены безвозвратно.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if ok != QMessageBox.StandardButton.Yes:
            return
        instances = load_instances()
        instances = [x for x in instances if x["id"] != inst["id"]]
        save_instances(instances)
        inst_dir = os.path.join(INSTANCES_DIR, inst["id"])
        if os.path.exists(inst_dir):
            import shutil
            shutil.rmtree(inst_dir, ignore_errors=True)
        self._refresh()

    def _clone_instance(self, inst):
        import copy
        new_inst = copy.deepcopy(inst)
        import uuid
        new_inst["id"] = str(uuid.uuid4())[:8]
        new_inst["name"] = inst["name"] + " (копия)"
        new_inst["created"] = datetime.datetime.now().isoformat()
        new_inst["last_played"] = ""
        inst_dir = os.path.join(INSTANCES_DIR, new_inst["id"], "game")
        os.makedirs(inst_dir, exist_ok=True)
        src_dir = os.path.join(INSTANCES_DIR, inst["id"], "game")
        if os.path.exists(src_dir):
            import shutil
            for item in os.listdir(src_dir):
                s = os.path.join(src_dir, item)
                d = os.path.join(inst_dir, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, dirs_exist_ok=True)
                else:
                    shutil.copy2(s, d)
        instances = load_instances()
        instances.append(new_inst)
        save_instances(instances)
        self._refresh()

    def _backup_instance(self, inst):
        import datetime
        os.makedirs("user_data/backups", exist_ok=True)
        date_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{inst['id']}_{date_str}.zip"
        backup_path = os.path.join("user_data", "backups", backup_name)
        inst_dir = os.path.join(INSTANCES_DIR, inst["id"], "game")
        if os.path.exists(inst_dir):
            with zipfile.ZipFile(backup_path, "w", zipfile.ZIP_DEFLATED) as zf:
                for root, dirs, files in os.walk(inst_dir):
                    for fn in files:
                        fpath = os.path.join(root, fn)
                        arc = os.path.relpath(fpath, os.path.join(INSTANCES_DIR, inst["id"]))
                        zf.write(fpath, arc)
            QMessageBox.information(self, "Готово", f"Бэкап создан:\n{backup_path}")

    def _restore_instance(self, inst):
        path, _ = QFileDialog.getOpenFileName(self, "Выберите ZIP бэкапа", "user_data/backups", "ZIP (*.zip)")
        if not path:
            return
        inst_dir = os.path.join(INSTANCES_DIR, inst["id"], "game")
        if os.path.exists(inst_dir):
            reply = QMessageBox.question(self, "Восстановление",
                "Текущие файлы игры будут заменены. Продолжить?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply != QMessageBox.StandardButton.Yes:
                return
            import shutil
            shutil.rmtree(inst_dir, ignore_errors=True)
        os.makedirs(inst_dir, exist_ok=True)
        with zipfile.ZipFile(path, "r") as zf:
            zf.extractall(os.path.join(INSTANCES_DIR, inst["id"]))
        QMessageBox.information(self, "Готово", "Бэкап восстановлен!")

    def _play_instance(self, inst):
        mw = self.parent_window
        if not mw:
            return
        mw._launch_instance(inst)

    def _export_instance(self, inst):
        name = inst["name"]
        default_name = name.replace(" ", "_") + ".mrpack"
        path, _ = QFileDialog.getSaveFileName(self, "Экспорт сборки", default_name,
            "Modpack (*.mrpack *.zip)")
        if not path:
            return
        self._do_export(inst, path)

    def _do_export(self, inst, path):
        import zipfile, json
        inst_dir = os.path.join(INSTANCES_DIR, inst["id"], "game")
        mods_dir = os.path.join(inst_dir, "mods")
        overrides_dir = os.path.join(inst_dir, "overrides") if os.path.exists(os.path.join(inst_dir, "overrides")) else inst_dir

        index = {
            "formatVersion": 1,
            "game": "minecraft",
            "versionId": inst["mc_version"],
            "name": inst["name"],
            "summary": "",
            "files": [],
            "dependencies": {
                "minecraft": inst["mc_version"],
            },
            "overrides": "overrides",
        }

        if inst["loader"] != "Vanilla":
            loader_lower = inst["loader"].lower()
            if loader_lower == "neoforge":
                loader_lower = "neoforge"
            index["dependencies"][loader_lower] = inst.get("loader_version", "")

        # Read mods from .minecraft/mods and create file entries
        file_refs = []
        if os.path.isdir(mods_dir):
            for fname in os.listdir(mods_dir):
                if fname.endswith(".jar"):
                    fpath = os.path.join(mods_dir, fname)
                    size = os.path.getsize(fpath)
                    import hashlib
                    h = hashlib.sha512()
                    with open(fpath, "rb") as f:
                        h.update(f.read())
                    file_refs.append({
                        "path": f"mods/{fname}",
                        "hashes": {"sha512": h.hexdigest()},
                        "env": {"client": "required", "server": "required"},
                        "downloads": [],
                        "fileSize": size,
                    })
        index["files"] = file_refs

        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("modrinth.index.json", json.dumps(index, indent=2))
            # Add override files
            for root, dirs, files in os.walk(overrides_dir):
                if "mods" in root.split(os.sep):
                    continue
                for fname in files:
                    fpath = os.path.join(root, fname)
                    arcname = os.path.relpath(fpath, overrides_dir)
                    zf.write(fpath, f"overrides/{arcname}")

        QMessageBox.information(self, "Готово", f"Сборка экспортирована:\n{path}")

    def _publish_modrinth(self, inst):
        dlg = ModrinthPublishDialog(inst, self)
        if dlg.exec() != QDialog.DialogCode.Accepted:
            return
        token = dlg.token_input.text().strip()
        ver_name = dlg.name_input.text().strip()
        ver_number = dlg.version_input.text().strip()
        release_type = dlg.release_combo.currentText().lower()
        changelog = dlg.changelog_input.toPlainText().strip()

        if not token or not ver_name:
            QMessageBox.warning(self, "Ошибка", "Заполни название и API токен")
            return

        # Create temp mrpack
        import tempfile
        tmp = tempfile.NamedTemporaryFile(suffix=".mrpack", delete=False)
        tmp_path = tmp.name
        tmp.close()
        self._do_export(inst, tmp_path)

        self.status_label.setText(f"⏳ Публикация {ver_name} на Modrinth...")
        QApplication.processEvents()

        def upload():
            try:
                headers = {"Authorization": token, "User-Agent": "SuperLauncher/2.0"}
                # Step 1: create version
                body = {
                    "name": ver_name,
                    "version_number": ver_number,
                    "dependencies": [],
                    "game_versions": [inst["mc_version"]],
                    "version_type": release_type,
                    "loaders": [inst["loader"].lower()] if inst["loader"] != "Vanilla" else [],
                    "featured": False,
                    "project_id": dlg.project_input.text().strip() or None,
                    "file_parts": ["file"],
                    "changelog": changelog or ver_name,
                }
                with open(tmp_path, "rb") as f:
                    files = {"file": f}
                    resp = requests.post(
                        "https://api.modrinth.com/v2/version",
                        headers=headers,
                        data={k: v for k, v in body.items() if k != "file_parts"},
                        files=files,
                        timeout=120)
                os.unlink(tmp_path)
                if resp.status_code in (200, 201):
                    QTimer.singleShot(0, lambda: (
                        QMessageBox.information(self, "Успех", f"✅ Сборка опубликована!\n{resp.json().get('id', '')}"),
                        self.status_label.setText("✅ Опубликовано на Modrinth")
                    ))
                else:
                    err = resp.text[:500]
                    QTimer.singleShot(0, lambda: (
                        QMessageBox.critical(self, "Ошибка", f"Modrinth API: {resp.status_code}\n{err}"),
                        self.status_label.setText("❌ Ошибка публикации")
                    ))
            except Exception as e:
                os.unlink(tmp_path)
                QTimer.singleShot(0, lambda: (
                    QMessageBox.critical(self, "Ошибка", str(e)),
                    self.status_label.setText("❌ Ошибка публикации")
                ))

        Thread(target=upload, daemon=True).start()

    def _import_modpack(self):
        path, _ = QFileDialog.getOpenFileName(self, "Выберите .mrpack или .zip",
            "", "Modpacks (*.mrpack *.zip)")
        if not path:
            return
        self._do_import(path)

    def _do_import(self, path):
        import zipfile, json, shutil
        try:
            with zipfile.ZipFile(path, "r") as zf:
                index_data = zf.read("modrinth.index.json")
                index = json.loads(index_data)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось прочитать .mrpack:\n{e}")
            return

        name = index.get("name", os.path.splitext(os.path.basename(path))[0])
        mc_ver = index.get("versionId", "latest_release")
        deps = index.get("dependencies", {})
        loader = "Vanilla"
        for l in ["fabric", "forge", "quilt", "neoforge"]:
            if l in deps:
                loader = l.capitalize()
                break

        inst = create_instance(name=name, mc_version=mc_ver, loader=loader)
        inst_dir = os.path.join(INSTANCES_DIR, inst["id"], "game")

        # Extract overrides
        if "overrides" in index:
            overrides_path = index["overrides"]
            with zipfile.ZipFile(path, "r") as zf:
                for entry in zf.namelist():
                    if entry.startswith(overrides_path + "/") or entry == overrides_path + "/":
                        rel = os.path.relpath(entry, overrides_path)
                        dest = os.path.join(inst_dir, rel)
                        if entry.endswith("/"):
                            os.makedirs(dest, exist_ok=True)
                        else:
                            os.makedirs(os.path.dirname(dest), exist_ok=True)
                            with zf.open(entry) as src, open(dest, "wb") as dst:
                                dst.write(src.read())

        instances = load_instances()
        instances.append(inst)
        save_instances(instances)
        self._refresh()
        QMessageBox.information(self, "Готово",
            f"Сборка «{name}» импортирована.\nВерсия: {mc_ver}, загрузчик: {loader}")

    def _open_log_viewer(self):
        dlg = LogViewerDialog(self)
        dlg.exec()


class LogViewerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Просмотр логов")
        self.resize(800, 600)
        self.setStyleSheet("QDialog { background: #1a1a2e; color: white; }")

        layout = QVBoxLayout(self)

        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane { background: #1a1a2e; border: 1px solid #333; }
            QTabBar::tab { background: #2f2f2f; color: #ccc; padding: 8px 16px; border: none; }
            QTabBar::tab:selected { background: #4facfe; color: white; }
        """)

        # Latest log tab
        log_tab = QWidget()
        log_layout = QVBoxLayout(log_tab)
        self.log_content = ""
        filter_row = QHBoxLayout()
        filter_row.addWidget(QLabel("Фильтр:"))
        self.log_filter = QComboBox()
        self.log_filter.addItems(["All", "INFO", "WARN", "ERROR", "FATAL"])
        self.log_filter.setStyleSheet("background:#2f2f2f; color:white; border:1px solid #444; border-radius:4px; padding:4px;")
        self.log_filter.currentTextChanged.connect(self._apply_log_filter)
        filter_row.addWidget(self.log_filter)
        filter_row.addStretch()
        log_layout.addLayout(filter_row)
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("background:#111; color:#0f0; font-family:Consolas,monospace; font-size:12px; border:none;")
        log_layout.addWidget(self.log_text)
        refresh_log_btn = QPushButton("🔄 Обновить")
        refresh_log_btn.setStyleSheet("background:#4facfe; color:white; border:none; border-radius:4px; padding:6px;")
        refresh_log_btn.clicked.connect(self._load_latest_log)
        log_layout.addWidget(refresh_log_btn)
        tabs.addTab(log_tab, "latest.log")

        # Crash reports tab
        crash_tab = QWidget()
        crash_layout = QVBoxLayout(crash_tab)
        self.crash_list = QListWidget()
        self.crash_list.setStyleSheet("background:#111; color:white; border:none; font-size:12px;")
        self.crash_list.itemClicked.connect(self._show_crash_report)
        crash_layout.addWidget(self.crash_list)
        refresh_crash_btn = QPushButton("🔄 Обновить")
        refresh_crash_btn.setStyleSheet("background:#4facfe; color:white; border:none; border-radius:4px; padding:6px;")
        refresh_crash_btn.clicked.connect(self._load_crash_reports)
        crash_layout.addWidget(refresh_crash_btn)
        tabs.addTab(crash_tab, "Crash Reports")

        # Instance picker
        picker_row = QHBoxLayout()
        picker_row.addWidget(QLabel("Инстанс:"))
        self.instance_combo = QComboBox()
        self.instance_combo.setStyleSheet("background:#2f2f2f; color:white; border:1px solid #444; border-radius:4px; padding:4px;")
        self.instance_combo.addItem("(глобальный .minecraft)", "")
        for inst in load_instances():
            self.instance_combo.addItem(f"{inst.get('icon','📦')} {inst['name']}", inst["id"])
        self.instance_combo.currentIndexChanged.connect(self._load_logs)
        picker_row.addWidget(self.instance_combo, 1)
        layout.addLayout(picker_row)

        layout.addWidget(tabs)

        self._load_logs()

    def _get_mc_dir(self):
        inst_id = self.instance_combo.currentData()
        if inst_id:
            inst_dir = os.path.join(INSTANCES_DIR, inst_id, "game")
            if os.path.exists(inst_dir):
                return inst_dir
        return minecraft_directory

    def _load_logs(self):
        self._load_latest_log()
        self._load_crash_reports()

    def _load_latest_log(self):
        mc_dir = self._get_mc_dir()
        log_path = os.path.join(mc_dir, "logs", "latest.log")
        if not os.path.exists(log_path):
            self.log_text.setPlainText("Лог-файл не найден. Запусти Minecraft хотя бы раз.")
            return
        try:
            with open(log_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            self.log_content = content[-50000:]  # last 50k chars
            self._apply_log_filter()
            self.log_text.moveCursor(QTextCursor.MoveOperation.End)
        except Exception as e:
            self.log_text.setPlainText(f"Ошибка чтения лога: {e}")

    def _apply_log_filter(self, *args):
        level = self.log_filter.currentText()
        if level == "All" or not self.log_content:
            self.log_text.setPlainText(self.log_content)
        else:
            filtered = "\n".join(line for line in self.log_content.split("\n") if level in line)
            self.log_text.setPlainText(filtered)

    def _load_crash_reports(self):
        self.crash_list.clear()
        mc_dir = self._get_mc_dir()
        crash_dir = os.path.join(mc_dir, "crash-reports")
        if not os.path.exists(crash_dir):
            self.crash_list.addItem("Папка crash-reports не найдена")
            return
        reports = sorted(
            [f for f in os.listdir(crash_dir) if f.endswith(".txt")],
            reverse=True
        )
        if not reports:
            self.crash_list.addItem("Крэш-репортов нет")
            return
        for r in reports[:20]:
            item = QListWidgetItem(r)
            item.setData(Qt.ItemDataRole.UserRole, os.path.join(crash_dir, r))
            self.crash_list.addItem(item)

    def _show_crash_report(self, item):
        path = item.data(Qt.ItemDataRole.UserRole)
        if not path or not os.path.exists(path):
            return
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
        except Exception as e:
            content = f"Ошибка: {e}"
        dlg = QDialog(self)
        dlg.setWindowTitle(os.path.basename(path))
        dlg.resize(700, 500)
        dlg.setStyleSheet("QDialog { background: #1a1a2e; color: white; }")
        lay = QVBoxLayout(dlg)
        txt = QTextEdit()
        txt.setReadOnly(True)
        txt.setPlainText(content)
        txt.setStyleSheet("background:#111; color:#f66; font-family:Consolas,monospace; font-size:12px; border:none;")
        lay.addWidget(txt)
        dlg.exec()

class ModernSidebar(QWidget):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.setFixedWidth(56)
        self.setMinimumWidth(56)
        self.setMaximumWidth(56)
        
        self.setStyleSheet("""
            ModernSidebar {
                background: #0e0e16;
                border-right: 1px solid rgba(255,255,255,0.03);
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(4, 8, 4, 8)
        layout.setSpacing(2)

        self.nav_buttons = []
        
        self.nav_items = [
            ("🏠", "Главная"),
            ("👤", "Аккаунт"),
            ("🧩", "Моды"),
            ("📦", "Инстансы"),
            ("🖼️", "Скины"),
            ("📢", "Новости"),
            ("🔄", "Обновления"),
            ("🖧", "Серверы"),
            ("⚙️", "Настройки"),
            ("⛏️", "Minecraft"),
            ("📁", "Контент"),
            ("🤖", "AI Агент")
        ]

        for icon, text in self.nav_items:
            btn = self.create_nav_button(icon, text)
            self.nav_buttons.append(btn)
            layout.addWidget(btn)

        layout.addStretch()

        self.setLayout(layout)

    def create_nav_button(self, icon, text):
        btn = QPushButton(icon)
        btn.setFixedSize(48, 48)
        btn.setCheckable(True)
        btn.setToolTip(text)
        btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                border-radius: 10px;
                font-size: 18px;
                color: rgba(255,255,255,0.3);
            }
            QPushButton:hover {
                background: rgba(255,255,255,0.04);
                color: rgba(255,255,255,0.7);
            }
            QPushButton:checked {
                background: rgba(168,85,247,0.1);
                color: white;
            }
        """)
        btn.clicked.connect(lambda checked, idx=len(self.nav_buttons): self.on_nav_clicked(idx))
        return btn

    def on_nav_clicked(self, index):
        if index < len(self.main_window.pages):
            self.main_window.pages.setCurrentIndex(index)
            for i, btn in enumerate(self.nav_buttons):
                btn.setChecked(i == index)
            # Update page title in top bar
            if hasattr(self.main_window, 'page_title'):
                titles = ["Главная", "Аккаунт", "Моды", "Инстансы", "Скины", 
                         "Новости", "Обновления", "Серверы", "Настройки", 
                         "Minecraft", "Контент", "AI Агент"]
                if index < len(titles):
                    self.main_window.page_title.setText(titles[index])

class GradientLabel(QLabel):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self._animation_progress = 0

        self.animation = QPropertyAnimation(self, b"animation_progress")
        self.animation.setDuration(2000)
        self.animation.setLoopCount(-1)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)

    def get_animation_progress(self):
        return self._animation_progress

    def set_animation_progress(self, value):
        self._animation_progress = value
        self.update()

    animation_progress = pyqtProperty(float, get_animation_progress, set_animation_progress)

    def showEvent(self, event):
        self.animation.start()
        super().showEvent(event)

    def hideEvent(self, event):
        self.animation.stop()
        super().hideEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0, QColor("#667eea"))
        gradient.setColorAt(0.5, QColor("#764ba2"))
        gradient.setColorAt(1, QColor("#667eea"))

        painter.setPen(QPen(QBrush(gradient), 2))
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.text())
        painter.end()


class LaunchThread(QThread):
    launch_setup_signal = pyqtSignal(str, str, str)  # version_id, username, loader_type
    progress_update_signal = pyqtSignal(int, int, str)
    state_update_signal = pyqtSignal(bool)
    error_signal = pyqtSignal(str)  # error message for UI

    def __init__(self):
        super().__init__()
        self.launch_setup_signal.connect(self.launch_setup)
        self.version_id = ''
        self.username = ''
        self.loader_type = 'vanilla'
        self.max_ram = 4096
        self.min_ram = 1024
        self.java_path = ''
        self.jvm_args = ''
        self.progress = 0
        self.progress_max = 100
        self.progress_label = ''
        self.mc_directory = None
        self.uuid = ''
        self.token = ''

    def launch_setup(self, version_id, username, loader_type):
        self.username = username
        self.loader_type = loader_type
        self.version_id = version_id

    def update_progress_label(self, value):
        self.progress_label = value
        self.progress_update_signal.emit(self.progress, self.progress_max, self.progress_label)

    def update_progress(self, value):
        self.progress = value
        self.progress_update_signal.emit(self.progress, self.progress_max, self.progress_label)

    def update_progress_max(self, value):
        self.progress_max = value
        self.progress_update_signal.emit(self.progress, self.progress_max, self.progress_label)

    def run(self):
        self.state_update_signal.emit(True)
        try:
            cfg = load_config()
            if cfg.get("proxy_host") and cfg.get("proxy_port"):
                proxy_url = f"http://{cfg['proxy_host']}:{cfg['proxy_port']}"
                if cfg.get("proxy_user"):
                    proxy_url = f"http://{cfg['proxy_user']}:{cfg.get('proxy_pass','')}@{cfg['proxy_host']}:{cfg['proxy_port']}"
                os.environ["HTTP_PROXY"] = proxy_url
                os.environ["HTTPS_PROXY"] = proxy_url
            mc_dir = self.mc_directory or minecraft_directory
            callback = {
                'setStatus': self.update_progress_label,
                'setProgress': self.update_progress,
                'setMax': self.update_progress_max
            }

            # 1. Устанавливаем загрузчик (только если ещё не установлен)
            loader = self.loader_type.lower()
            versions_dir = os.path.join(mc_dir, 'versions')

            def _is_installed(ver_id):
                return os.path.isdir(os.path.join(versions_dir, ver_id))

            if loader == "vanilla":
                if not _is_installed(self.version_id):
                    install_minecraft_version(version=self.version_id,
                        minecraft_directory=mc_dir, callback=callback)
            elif loader == "fabric":
                loader_ver = fabric_loader.get_latest_loader_version()
                installed_id = f"fabric-loader-{loader_ver}-{self.version_id}"
                if not _is_installed(installed_id):
                    fabric_loader.install_fabric(minecraft_version=self.version_id,
                        minecraft_directory=mc_dir, callback=callback)
            elif loader == "forge":
                forge_version = forge_loader.find_forge_version(self.version_id)
                if not forge_version:
                    raise Exception(f"Forge версия не найдена для {self.version_id}")
                installed_id = forge_loader.forge_to_installed_version(forge_version)
                if not _is_installed(installed_id):
                    forge_loader.install_forge_version(forge_version,
                        mc_dir, callback=callback)
            elif loader == "quilt":
                installed_id = f"quilt-loader-{self.version_id}"
                if not _is_installed(installed_id):
                    quilt_loader.install_quilt(minecraft_version=self.version_id,
                        minecraft_directory=mc_dir, callback=callback)
            elif loader == "neoforge":
                self._nf_installed_version = self._install_neoforge(callback)
            elif loader == "optifine":
                self._install_optifine()
            else:
                if not _is_installed(self.version_id):
                    install_minecraft_version(version=self.version_id,
                        minecraft_directory=mc_dir, callback=callback)

            # 2. Готовим опции запуска
            if self.username == '':
                self.username = generate_username()[0]

            options = {
                'username': self.username,
                'uuid': self.uuid or str(uuid1()),
                'token': self.token or '',
                'jvmArguments': [
                    f'-Xmx{self.max_ram}M',
                    f'-Xms{self.min_ram}M',
                ],
                'launcherName': 'SuperLauncher',
                'launcherVersion': '2.0',
            }

            if self.java_path and os.path.exists(self.java_path):
                options['executablePath'] = self.java_path

            if self.jvm_args:
                extra_args = self.jvm_args.split()
                options['jvmArguments'].extend(extra_args)

            # 3. Определяем ID версии для запуска (у Forge/Fabric он может отличаться)
            launch_version = self.version_id
            if loader == "forge":
                forge_ver = forge_loader.find_forge_version(self.version_id)
                if forge_ver:
                    launch_version = forge_loader.forge_to_installed_version(forge_ver)
            elif loader == "fabric":
                launch_version = self._find_installed_loader_version("fabric-loader", self.version_id)
                if not launch_version:
                    loader_ver = fabric_loader.get_latest_loader_version()
                    launch_version = f"fabric-loader-{loader_ver}-{self.version_id}"
            elif loader == "quilt":
                launch_version = f"quilt-loader-{self.version_id}"
            elif loader == "neoforge":
                launch_version = getattr(self, '_nf_installed_version', self.version_id)
                if launch_version == self.version_id:
                    raise Exception("NeoForge: не удалось определить версию для запуска")

            cmd = get_minecraft_command(
                version=launch_version,
                minecraft_directory=mc_dir,
                options=options
            )
            print("Запускаем команду:", cmd)
            proc = subprocess.Popen(cmd, cwd=mc_dir)
            proc.wait()
            print(f"Процесс Minecraft завершился с кодом: {proc.returncode}")
        except Exception as e:
            print("Ошибка при запуске Minecraft:", e)
            import traceback
            traceback.print_exc()
            self.error_signal.emit(str(e))
        finally:
            self.state_update_signal.emit(False)

    @staticmethod
    def _find_installed_loader_version(prefix, mc_version, mc_dir=None):
        """Поиск установленной в versions/ версии загрузчика (fabric-loader, quilt-loader)"""
        base = mc_dir or minecraft_directory
        versions_dir = os.path.join(base, 'versions')
        if not os.path.isdir(versions_dir):
            return None
        candidates = []
        for folder in os.listdir(versions_dir):
            if folder.startswith(f"{prefix}-") and folder.endswith(mc_version):
                candidates.append(folder)
        if not candidates:
            return None
        candidates.sort(reverse=True)
        return candidates[0]

    def _install_optifine(self):
        """Установка OptiFine через прямое скачивание и запуск установщика"""
        import urllib.request
        import zipfile

        mc_dir = self.mc_directory or minecraft_directory
        optifine_dir = os.path.join(mc_dir, "mods", "optifine")
        os.makedirs(optifine_dir, exist_ok=True)

        self.update_progress_label("Поиск OptiFine...")
        try:
            import requests as req
            resp = req.get("https://optifine.net/downloads", timeout=10)
            html = resp.text
            # Ищем ссылку на версию
            import re
            pattern = rf'/downloads/[^"]*{re.escape(self.version_id)}[^"]*\.jar'
            match = re.search(pattern, html)
            if not match:
                raise Exception(f"OptiFine для {self.version_id} не найден")
            dl_path = match.group(0)
            dl_url = f"https://optifine.net{dl_path}"

            jar_path = os.path.join(optifine_dir, f"OptiFine_{self.version_id}.jar")
            if not os.path.exists(jar_path):
                self.update_progress_label("Скачивание OptiFine...")
                urllib.request.urlretrieve(dl_url, jar_path)

            # Запускаем установщик OptiFine
            self.update_progress_label("Запуск установщика OptiFine...")
            java_exe = self.java_path or "java"
            subprocess.run([java_exe, "-jar", jar_path], cwd=optifine_dir, check=True)

            # После установки OptiFine версия будет как optifine_версия
            self.version_id = f"{self.version_id}_optifine"
            self.update_progress_label("OptiFine установлен!")
        except Exception as e:
            print(f"Ошибка установки OptiFine: {e}")
            raise

    def _install_neoforge(self, callback):
        NF_API = "https://maven.neoforged.net/api/maven/versions/releases/net/neoforged/neoforge"
        NF_MAVEN = "https://maven.neoforged.net/releases/net/neoforged/neoforge"
        self.update_progress_label("Поиск NeoForge...")
        try:
            r = requests.get(NF_API, timeout=15)
            r.raise_for_status()
            versions = r.json()["versions"]
        except Exception:
            self.update_progress_label("API NeoForge недоступен, пробуем GitHub...")
            try:
                r = requests.get("https://api.github.com/repos/neoforged/NeoForge/releases?per_page=50", timeout=15)
                r.raise_for_status()
                versions = []
                for rel in r.json():
                    tag = rel.get("tag_name", "")
                    parts = tag.split("-")
                    if len(parts) == 2:
                        versions.append(parts[1])
            except Exception:
                raise Exception("NeoForge недоступен (maven + GitHub). Проверь интернет или VPN.")

        ver_parts = self.version_id.split(".")
        mc_major = ver_parts[1]
        mc_minor = ver_parts[2] if len(ver_parts) > 2 else ""
        compatible = []
        for v in versions:
            vp = v.split(".")
            if len(vp) < 2:
                continue
            if vp[0] == mc_major and (not mc_minor or vp[1] == mc_minor):
                compatible.append(v)
        if not compatible:
            compatible = [v for v in versions if v.split(".")[0] == mc_major and len(v.split(".")) > 1]
        if not compatible:
            raise Exception(f"NeoForge не найдена для {self.version_id}")
        loader_ver = compatible[-1]

        installer_url = f"{NF_MAVEN}/{loader_ver}/neoforge-{loader_ver}-installer.jar"
        self.update_progress_label(f"Скачивание NeoForge {loader_ver}...")
        temp_dir = tempfile.mkdtemp(prefix="neoforge-")
        installer_path = os.path.join(temp_dir, "neoforge-installer.jar")
        try:
            dl_resp = requests.get(installer_url, timeout=60, stream=True)
            dl_resp.raise_for_status()
            total = int(dl_resp.headers.get("content-length", 0))
            written = 0
            with open(installer_path, "wb") as f:
                for chunk in dl_resp.iter_content(8192):
                    f.write(chunk)
                    written += len(chunk)
                    if total > 0:
                        self.update_progress(int(written * 100 / total))
            self.update_progress_label("Запуск установщика NeoForge...")
            java_exe = self.java_path or "java"
            mc_dir = self.mc_directory or minecraft_directory
            subprocess.run(
                [java_exe, "-jar", installer_path, "--install-client", mc_dir],
                check=True, timeout=120,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

        installed_ver = f"neoforge-{loader_ver}"
        install_minecraft_version(installed_ver, mc_dir, callback=callback)
        return installed_ver


# Функция возвращает все версии без фильтрации (Vanilla + Snapshots + Fabric + Forge)
def get_all_versions():
    versions = get_version_list()  # vanilla + snapshots
    versions_dir = os.path.join(minecraft_directory, 'versions')
    if os.path.exists(versions_dir):
        for folder in os.listdir(versions_dir):
            full_path = os.path.join(versions_dir, folder)
            if os.path.isdir(full_path):
                if not any(v['id'] == folder for v in versions):
                    versions.append({'id': folder})
    return versions


class MinecraftLauncherPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.config = load_config()

        # Логотип
        self.logo = QLabel()
        self.logo.setMaximumSize(QSize(256, 37))
        pixmap = QPixmap('assets/title.png')
        if not pixmap.isNull():
            self.logo.setPixmap(pixmap)
        self.logo.setScaledContents(True)

        # Spacer
        self.titlespacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        # Поле для имени пользователя
        self.username = QLineEdit()
        self.username.setPlaceholderText(self.tr("Username"))
        self.username.setStyleSheet("""
            background-color: #2f2f2f;
            color: white;
            border: 1px solid #444;
            border-radius: 5px;
            padding: 5px;
        """)

        # Список версий
        self.version_select = QComboBox()
        self.version_select.setStyleSheet("""
            background-color: #2f2f2f;
            color: white;
            border: 1px solid #444;
            border-radius: 5px;
            padding: 3px;
        """)
        self.update_versions_list()
        self.auto_select_profile_version()

        # Выбор загрузчика
        self.loader_select = QComboBox()
        self.loader_select.addItems(["Vanilla", "Fabric", "Forge", "Quilt", "OptiFine", "NeoForge"])
        self.loader_select.setStyleSheet("""
            background-color: #2f2f2f;
            color: white;
            border: 1px solid #444;
            border-radius: 5px;
            padding: 3px;
        """)
        self.restore_last_session()

        # Прогрессбар
        self.progress_spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.start_progress_label = QLabel('')
        self.start_progress_label.setVisible(False)
        self.start_progress = QProgressBar()
        self.start_progress.setValue(0)
        self.start_progress.setVisible(False)

        # Кнопка запуска
        self.start_button = QPushButton(self.tr("Play"))
        self.start_button.setStyleSheet("""
            background-color: #2f2f2f;
            color: white;
            border: 1px solid #4facfe;
            border-radius: 8px;
            padding: 8px;
            font-weight: bold;
        """)
        self.start_button.setCursor(Qt.CursorShape.PointingHandCursor)

        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.addWidget(self.logo, 0, Qt.AlignmentFlag.AlignHCenter)
        layout.addItem(self.titlespacer)
        layout.addWidget(self.username)
        layout.addWidget(self.version_select)
        layout.addWidget(self.loader_select)
        layout.addItem(self.progress_spacer)
        layout.addWidget(self.start_progress_label)
        layout.addWidget(self.start_progress)
        layout.addWidget(self.start_button)

    # --- Перевод ---
    def tr(self, key: str) -> str:
        lang = self.config.get("language", "ru")
        return translations.get(lang, {}).get(key, key)

    def auto_select_profile_version(self):
        """Автовыбор версии из launcher_profiles.json (как в Legacy Launcher)"""
        profile_path = os.path.join(get_minecraft_directory(), 'launcher_profiles.json')
        if not os.path.isfile(profile_path):
            return
        try:
            with open(profile_path, encoding='utf-8') as f:
                profiles_data = json.load(f)
            selected = profiles_data.get('selectedProfile')
            profiles = profiles_data.get('profiles', {})
            if selected and selected in profiles:
                prof = profiles[selected]
                last_ver = prof.get('lastVersionId', '')
                if last_ver:
                    idx = self.version_select.findText(last_ver)
                    if idx >= 0:
                        self.version_select.setCurrentIndex(idx)
        except Exception:
            pass

    def restore_last_session(self):
        """Восстановление ника, версии и загрузчика из последнего запуска"""
        config = load_config()
        username = config.get("last_username", "")
        if username:
            self.username.setText(username)
        version = config.get("last_version_id", "")
        if version:
            idx = self.version_select.findText(version)
            if idx >= 0:
                self.version_select.setCurrentIndex(idx)
        loader = config.get("last_loader_type", "")
        if loader:
            loader_map = {"vanilla": "Vanilla", "fabric": "Fabric", "forge": "Forge",
                          "quilt": "Quilt", "optifine": "OptiFine", "neoforge": "NeoForge"}
            display = loader_map.get(loader, loader.capitalize())
            idx = self.loader_select.findText(display)
            if idx >= 0:
                self.loader_select.setCurrentIndex(idx)

    def refresh_language(self):
        self.username.setPlaceholderText(self.tr("Username"))
        self.start_button.setText(self.tr("Play"))

    # --- Версии Minecraft ---
    def update_versions_list(self):
        self.version_select.clear()
        versions = self.get_all_versions()
        for version in versions:
            self.version_select.addItem(version['id'])

    @staticmethod
    def get_all_versions():
        from minecraft_launcher_lib.utils import get_version_list, get_minecraft_directory
        versions = []

        try:
            online_versions = get_version_list()
            versions.extend(online_versions)
        except Exception as e:
            print("Онлайн-версии недоступны, используем локальные:", e)

        versions_dir = os.path.join(get_minecraft_directory(), 'versions')
        if os.path.exists(versions_dir):
            for folder in os.listdir(versions_dir):
                full_path = os.path.join(versions_dir, folder)
                if os.path.isdir(full_path):
                    if not any(v['id'] == folder for v in versions):
                        versions.append({'id': folder})

        if not versions:
            versions.append({'id': 'No versions available'})
        return versions


class JavaDownloaderDialog(QDialog):
    ADOPTIUM_API = "https://api.adoptium.net/v3/assets/feature_releases/{version}/ga?image_type=jdk&architecture=x64&os=windows&page_size=5"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Скачать Java")
        self.setFixedSize(500, 450)
        self.selected_path = None

        layout = QVBoxLayout(self)

        title = QLabel("Выбери версию Java для скачивания")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
        layout.addWidget(title)

        self.version_combo = QComboBox()
        self.version_combo.addItems(["8", "11", "17", "21", "23"])
        self.version_combo.setCurrentText("17")
        layout.addWidget(self.version_combo)

        self.java_list = QListWidget()
        self.java_list.setStyleSheet("QListWidget{background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.1);border-radius:8px;color:white;}")
        layout.addWidget(self.java_list)

        btn_row = QHBoxLayout()
        self.fetch_btn = QPushButton("🔍 Найти сборки")
        self.fetch_btn.setStyleSheet("background:#4facfe; color:white; padding:8px 16px; border-radius:6px;")
        self.fetch_btn.clicked.connect(self._fetch)
        btn_row.addWidget(self.fetch_btn)

        self.dl_btn = QPushButton("⬇ Скачать и установить")
        self.dl_btn.setStyleSheet("background:#4caf50; color:white; padding:8px 16px; border-radius:6px;")
        self.dl_btn.setEnabled(False)
        self.dl_btn.clicked.connect(self._download_selected)
        btn_row.addWidget(self.dl_btn)

        btn_cancel = QPushButton("Отмена")
        btn_cancel.clicked.connect(self.reject)
        btn_row.addWidget(btn_cancel)
        layout.addLayout(btn_row)

        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #888; font-size: 12px;")
        layout.addWidget(self.status_label)

        self._assets = []

    def _fetch(self):
        self.java_list.clear()
        self.dl_btn.setEnabled(False)
        self.status_label.setText("Загрузка списка...")
        ver = self.version_combo.currentText()

        def task():
            try:
                resp = requests.get(self.ADOPTIUM_API.format(version=ver), timeout=15)
                if resp.status_code != 200:
                    QTimer.singleShot(0, lambda: self.status_label.setText(f"Ошибка: HTTP {resp.status_code}"))
                    return
                data = resp.json()
                self._assets = []
                for item in data:
                    binary = item.get("binary", {})
                    pkg = binary.get("package", {})
                    dl_url = pkg.get("link", "")
                    if not dl_url:
                        continue
                    release_name = binary.get("release_name", "")
                    image_type = binary.get("image_type", "jdk")
                    os_name = binary.get("os", "windows")
                    arch = binary.get("architecture", "x64")
                    self._assets.append({
                        "release_name": release_name,
                        "url": dl_url,
                        "image_type": image_type,
                        "os": os_name,
                        "arch": arch,
                    })
                QTimer.singleShot(0, self._populate)
            except Exception as e:
                QTimer.singleShot(0, lambda: self.status_label.setText(f"Ошибка: {e}"))

        Thread(target=task, daemon=True).start()

    def _populate(self):
        self.java_list.clear()
        for a in self._assets:
            item = QListWidgetItem(f"{a['release_name']} ({a['image_type']} - {a['os']}/{a['arch']})")
            item.setData(Qt.ItemDataRole.UserRole, self._assets.index(a))
            self.java_list.addItem(item)
        if self._assets:
            self.java_list.setCurrentRow(0)
            self.dl_btn.setEnabled(True)
        self.status_label.setText(f"Найдено {len(self._assets)} сборок")

    def _download_selected(self):
        row = self.java_list.currentRow()
        if row < 0 or row >= len(self._assets):
            return
        asset = self._assets[row]
        dl_url = asset["url"]
        self.dl_btn.setEnabled(False)
        self.status_label.setText(f"Скачивание {asset['release_name']}...")

        def task():
            try:
                resp = requests.get(dl_url, timeout=300, stream=True)
                if resp.status_code != 200:
                    QTimer.singleShot(0, lambda: self.status_label.setText(f"Ошибка: HTTP {resp.status_code}"))
                    return
                tmp = tempfile.NamedTemporaryFile(suffix=".msi", delete=False)
                tmp_path = tmp.name
                tmp.close()
                with open(tmp_path, "wb") as f:
                    for chunk in resp.iter_content(8192):
                        if chunk:
                            f.write(chunk)
                # Extract environment variable after install
                QTimer.singleShot(0, lambda: self._install_msi(tmp_path, asset))
            except Exception as e:
                QTimer.singleShot(0, lambda: self.status_label.setText(f"Ошибка: {e}"))

        Thread(target=task, daemon=True).start()

    def _install_msi(self, msi_path, asset):
        reply = QMessageBox.question(self, "Установка Java",
            f"Загружен {asset['release_name']}.\nЗапустить установщик? После установки выбери путь к java.exe.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.No:
            self.status_label.setText("Установка отменена")
            return
        try:
            subprocess.Popen(["msiexec", "/i", msi_path], close_fds=True)
            self.status_label.setText("Установщик запущен. После установки нажми «Обзор» и выбери java.exe")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось запустить установщик:\n{e}")


class SettingsPage(QWidget):
    def _make_card(self, title, icon, widget):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: #1a1a24;
                border: 1px solid rgba(255,255,255,0.04);
                border-radius: 8px;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(14, 10, 14, 10)
        card_layout.setSpacing(6)
        header = QLabel(f"{icon}   {title}")
        header.setStyleSheet("""
            font-size: 12px; font-weight: 600; color: rgba(255,255,255,0.45);
            background: transparent;
        """)
        card_layout.addWidget(header)
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background: rgba(255,255,255,0.03); max-height: 1px;")
        card_layout.addWidget(sep)
        card_layout.addWidget(widget)
        return card

    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = load_config()
        self.labels = {}
        self.buttons = {}

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { background: transparent; border: none; }")
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        content = QWidget()
        content.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(content)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(12)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Helper to add a card
        def add_card(title, icon, w):
            layout.addWidget(self._make_card(title, icon, w))
        
        # ===== GENERAL SETTINGS =====
        general_w = QWidget()
        general_w.setStyleSheet("background: transparent;")
        gl = QVBoxLayout(general_w)
        gl.setContentsMargins(0, 0, 0, 0)
        gl.setSpacing(8)
        
        row_lang = QHBoxLayout()
        self.labels["lang"] = QLabel()
        row_lang.addWidget(self.labels["lang"])
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(list(translations.keys()))
        self.lang_combo.setCurrentText(self.config.get("language", "ru"))
        self.lang_combo.currentTextChanged.connect(self.change_language)
        row_lang.addWidget(self.lang_combo, 1)
        gl.addLayout(row_lang)
        
        row_theme = QHBoxLayout()
        self.labels["theme"] = QLabel()
        row_theme.addWidget(self.labels["theme"])
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["dark", "light"])
        self.theme_combo.setCurrentText(self.config.get("theme", "dark"))
        row_theme.addWidget(self.theme_combo, 1)
        gl.addLayout(row_theme)
        
        self.buttons["accent_color"] = QPushButton("🎨  Pick Accent Color")
        self.buttons["accent_color"].clicked.connect(self.pick_accent_color)
        gl.addWidget(self.buttons["accent_color"])
        
        add_card("General", "⚙️", general_w)
        
        # ===== LAUNCH SETTINGS =====
        launch_w = QWidget()
        launch_w.setStyleSheet("background: transparent;")
        ll = QVBoxLayout(launch_w)
        ll.setContentsMargins(0, 0, 0, 0)
        ll.setSpacing(8)
        
        row_mode = QHBoxLayout()
        self.labels["launch_mode"] = QLabel()
        row_mode.addWidget(self.labels["launch_mode"])
        self.rb_launcher_lib = QRadioButton("Launcher Lib")
        self.rb_java = QRadioButton("Java Direct")
        row_mode.addWidget(self.rb_launcher_lib)
        row_mode.addWidget(self.rb_java)
        launch_mode = self.config.get("launch_mode", "launcher_lib")
        self.rb_java.setChecked(launch_mode == "java")
        self.rb_launcher_lib.setChecked(launch_mode != "java")
        ll.addLayout(row_mode)
        
        self.labels["java_path"] = QLabel()
        ll.addWidget(self.labels["java_path"])
        row_java = QHBoxLayout()
        self.java_path_input = QLineEdit(self.config.get("java_path", ""))
        self.java_path_input.setPlaceholderText("Путь к java.exe...")
        row_java.addWidget(self.java_path_input, 1)
        jrow = QHBoxLayout()
        self.buttons["browse_java"] = QPushButton("📂")
        self.buttons["browse_java"].setFixedWidth(40)
        self.buttons["browse_java"].clicked.connect(self.browse_java)
        jrow.addWidget(self.buttons["browse_java"])
        self.buttons["auto_java"] = QPushButton("🔍 Auto")
        self.buttons["auto_java"].clicked.connect(self.auto_detect_java)
        jrow.addWidget(self.buttons["auto_java"])
        self.buttons["dl_java"] = QPushButton("⬇ Download")
        self.buttons["dl_java"].clicked.connect(self._open_java_downloader)
        jrow.addWidget(self.buttons["dl_java"])
        ll.addLayout(row_java)
        ll.addLayout(jrow)
        
        self.java_path_input.setEnabled(self.rb_java.isChecked())
        self.buttons["browse_java"].setEnabled(self.rb_java.isChecked())
        self.rb_java.toggled.connect(self.java_path_input.setEnabled)
        self.rb_java.toggled.connect(self.buttons["browse_java"].setEnabled)
        
        self.buttons["test_java"] = QPushButton("🧪  Test Java Version")
        self.buttons["test_java"].clicked.connect(self.test_java_version)
        ll.addWidget(self.buttons["test_java"])
        
        add_card("Launch", "🚀", launch_w)
        
        # ===== MEMORY & JVM =====
        mem_w = QWidget()
        mem_w.setStyleSheet("background: transparent;")
        ml = QVBoxLayout(mem_w)
        ml.setContentsMargins(0, 0, 0, 0)
        ml.setSpacing(8)
        
        self.ram_label = QLabel()
        ml.addWidget(self.ram_label)
        ram_slider_row = QHBoxLayout()
        self.ram_slider = QSlider(Qt.Orientation.Horizontal)
        self.ram_slider.setRange(1024, 32768)
        self.ram_slider.setValue(self.config.get("max_ram", 4096))
        self.ram_slider.setTickInterval(1024)
        self.ram_slider.setSingleStep(512)
        self.ram_value_label = QLabel(f'{self.ram_slider.value()} MB')
        self.ram_value_label.setStyleSheet("font-weight: 600; color: white; min-width: 60px;")
        self.ram_slider.valueChanged.connect(lambda v: self.ram_value_label.setText(f'{v} MB'))
        ram_slider_row.addWidget(self.ram_slider, 1)
        ram_slider_row.addWidget(self.ram_value_label)
        ml.addLayout(ram_slider_row)
        
        self.buttons["ram_boost"] = QPushButton("⚡  RAM Boost (clear DNS cache)")
        self.buttons["ram_boost"].clicked.connect(self.ram_boost)
        ml.addWidget(self.buttons["ram_boost"])
        
        self.jvm_label = QLabel()
        ml.addWidget(self.jvm_label)
        self.jvm_input = QLineEdit(self.config.get("jvm_args", ""))
        self.jvm_input.setPlaceholderText("-XX:+UseG1GC -XX:+UnlockExperimentalVMOptions")
        ml.addWidget(self.jvm_input)
        
        self.jvm_presets = QComboBox()
        self.jvm_presets.addItems([
            "Custom",
            "Performance (-XX:+UseG1GC -XX:+UnlockExperimentalVMOptions -XX:G1NewSizePercent=20 -XX:+DisableExplicitGC)",
            "Vanilla (-Xincgc)",
            "Modded (-XX:+UseG1GC -XX:MaxGCPauseMillis=50 -XX:+DisableExplicitGC -XX:+ParallelRefProcEnabled)"
        ])
        self.jvm_presets.currentTextChanged.connect(self.on_jvm_preset_changed)
        ml.addWidget(self.jvm_presets)
        
        self.buttons["jvm_gen"] = QPushButton("⚙  JVM Args Generator")
        self.buttons["jvm_gen"].clicked.connect(self._open_jvm_generator)
        ml.addWidget(self.buttons["jvm_gen"])
        
        add_card("Memory & JVM", "💾", mem_w)
        
        # ===== BEHAVIOR =====
        beh_w = QWidget()
        beh_w.setStyleSheet("background: transparent;")
        bl = QVBoxLayout(beh_w)
        bl.setContentsMargins(0, 0, 0, 0)
        bl.setSpacing(8)
        
        self.tray_check = QCheckBox("🔽  Minimize to tray")
        self.tray_check.setChecked(self.config.get("minimize_to_tray", False))
        bl.addWidget(self.tray_check)
        
        self.autostart_check = QCheckBox("🚀  Launch with Windows")
        self.autostart_check.setChecked(self.config.get("autostart", False))
        bl.addWidget(self.autostart_check)
        
        self.rpc_status_label = QLabel("Discord RPC custom status:")
        bl.addWidget(self.rpc_status_label)
        self.rpc_status_input = QLineEdit(self.config.get("rpc_custom_status", ""))
        self.rpc_status_input.setPlaceholderText("SuperLauncher 2.0.0")
        bl.addWidget(self.rpc_status_input)
        
        self.buttons["proxy_settings"] = QPushButton("🌐  Proxy Settings")
        self.buttons["proxy_settings"].clicked.connect(self._open_proxy_settings)
        bl.addWidget(self.buttons["proxy_settings"])
        
        self.buttons["test_notif"] = QPushButton("🔔  Test Notification")
        self.buttons["test_notif"].clicked.connect(self.show_test_notification)
        bl.addWidget(self.buttons["test_notif"])
        
        add_card("Behavior", "🎮", beh_w)
        
        # ===== API KEYS =====
        api_w = QWidget()
        api_w.setStyleSheet("background: transparent;")
        al = QVBoxLayout(api_w)
        al.setContentsMargins(0, 0, 0, 0)
        al.setSpacing(8)
        
        self.labels["curseforge_key"] = QLabel()
        al.addWidget(self.labels["curseforge_key"])
        self.cf_key_input = QLineEdit(self.config.get("curseforge_api_key", ""))
        self.cf_key_input.setPlaceholderText("CurseForge API key...")
        al.addWidget(self.cf_key_input)
        self.buttons["test_cf_key"] = QPushButton("Test Key")
        al.addWidget(self.buttons["test_cf_key"])
        self.buttons["test_cf_key"].clicked.connect(self.test_cf_key)
        
        self.labels["azure_id"] = QLabel()
        al.addWidget(self.labels["azure_id"])
        self.azure_input = QLineEdit(self.config.get("azure_client_id", ""))
        self.azure_input.setPlaceholderText("Azure Application (client) ID...")
        al.addWidget(self.azure_input)
        
        add_card("API Keys", "🔑", api_w)
        
        # ===== BACKGROUND =====
        bg_w = QWidget()
        bg_w.setStyleSheet("background: transparent;")
        bgl = QVBoxLayout(bg_w)
        bgl.setContentsMargins(0, 0, 0, 0)
        bgl.setSpacing(8)
        
        self.labels["page_bg"] = QLabel()
        bgl.addWidget(self.labels["page_bg"])
        bg_btn_row = QHBoxLayout()
        self.bg_buttons = {}
        self.bg_options = {
            "dark": "assets/bg_dark.png",
            "gray": "assets/bg_gray.png"
        }
        for key, img in self.bg_options.items():
            btn = QPushButton()
            btn.setCheckable(True)
            btn.setIcon(QIcon(img))
            btn.setIconSize(QSize(100, 66))
            btn.setFixedSize(110, 74)
            btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            btn.setStyleSheet("""
                QPushButton {
                    border: 2px solid transparent;
                    border-radius: 10px;
                    background: rgba(255,255,255,0.05);
                }
                QPushButton:hover {
                    border: 2px solid rgba(255,255,255,0.2);
                }
                QPushButton:checked {
                    border: 2px solid #667eea;
                }
            """)
            btn.clicked.connect(lambda checked, k=key: self.select_bg(k))
            bg_btn_row.addWidget(btn)
            self.bg_buttons[key] = btn
        bgl.addLayout(bg_btn_row)
        current_bg = self.config.get("page_bg", "dark")
        self.select_bg(current_bg)
        
        self.buttons["select_bg_img"] = QPushButton("🖼  Select Custom Background Image")
        self.buttons["select_bg_img"].clicked.connect(self.select_custom_background)
        bgl.addWidget(self.buttons["select_bg_img"])
        
        add_card("Background", "🎨", bg_w)
        
        # ===== SAVE & SYNC =====
        save_w = QWidget()
        save_w.setStyleSheet("background: transparent;")
        sl = QVBoxLayout(save_w)
        sl.setContentsMargins(0, 0, 0, 0)
        sl.setSpacing(8)
        
        self.buttons["save"] = QPushButton("💾  Save Settings")
        sl.addWidget(self.buttons["save"])
        self.buttons["save"].clicked.connect(self.save_settings)
        
        sync_row = QHBoxLayout()
        self.buttons["export_settings"] = QPushButton("📤  Export Settings")
        self.buttons["export_settings"].setStyleSheet("background:rgba(255,255,255,0.06);")
        self.buttons["export_settings"].clicked.connect(self.export_settings)
        sync_row.addWidget(self.buttons["export_settings"])
        self.buttons["import_settings"] = QPushButton("📥  Import Settings")
        self.buttons["import_settings"].setStyleSheet("background:rgba(255,255,255,0.06);")
        self.buttons["import_settings"].clicked.connect(self.import_settings)
        sync_row.addWidget(self.buttons["import_settings"])
        sl.addLayout(sync_row)
        
        self.buttons["reset_config"] = QPushButton("⚠️  Reset Config")
        self.buttons["reset_config"].setStyleSheet("""
            QPushButton {
                background: rgba(231,76,60,0.15);
                border: 1px solid rgba(231,76,60,0.3);
            }
            QPushButton:hover {
                background: rgba(231,76,60,0.25);
            }
        """)
        self.buttons["reset_config"].clicked.connect(self.reset_config)
        sl.addWidget(self.buttons["reset_config"])
        
        add_card("Save & Sync", "💿", save_w)

        layout.addStretch()
        
        scroll.setWidget(content)
        
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)
        
        self.setLayout(outer)
        self.update_texts()

    def tr(self, key: str) -> str:
        lang = self.config.get("language", "ru")
        return translations.get(lang, {}).get(key, key)

    def update_texts(self):
        self.labels["theme"].setText(self.tr("Theme:"))
        self.labels["lang"].setText(self.tr("Language:"))
        self.labels["launch_mode"].setText(self.tr("Minecraft launch mode:"))
        self.rb_launcher_lib.setText(self.tr("minecraft-launcher-lib (default)"))
        self.rb_java.setText(self.tr("Java (specify path)"))
        self.labels["java_path"].setText(self.tr("Java path (if Java is selected):"))
        self.buttons["browse_java"].setText(self.tr("Browse Java path"))
        self.labels["curseforge_key"].setText(self.tr("CurseForge API Key:"))
        self.buttons["test_cf_key"].setText(self.tr("Test key"))
        self.labels["azure_id"].setText(self.tr("Azure Client ID (for Microsoft login):"))
        self.labels["page_bg"].setText(self.tr("Page backgrounds:"))
        self.buttons["save"].setText(self.tr("Save settings"))
        self.buttons["export_settings"].setText(self.tr("Export settings"))
        self.buttons["import_settings"].setText(self.tr("Import settings"))
        self.buttons["auto_java"].setText(self.tr("Auto-detect"))
        self.buttons["dl_java"].setText(self.tr("Download Java"))
        self.buttons["dl_java"].setText(self.tr("Download Java"))
        self.ram_label.setText(self.tr("RAM allocation:"))
        self.jvm_label.setText(self.tr("JVM arguments:"))
        self.buttons["accent_color"].setText(self.tr("Accent color"))
        self.buttons["ram_boost"].setText(self.tr("RAM Boost"))
        self.tray_check.setText(self.tr("Minimize to tray"))
        self.autostart_check.setText(self.tr("Launch with Windows"))
        self.buttons["test_java"].setText(self.tr("Test Java"))
        self.buttons["test_notif"].setText(self.tr("Test Notification"))
        self.buttons["reset_config"].setText(self.tr("Reset Config"))
        self.buttons["select_bg_img"].setText(self.tr("Select Background Image"))

        parent = self.parent()
        if parent and hasattr(parent, "refresh_language"):
            parent.refresh_language()

    def change_language(self, lang):
        self.config["language"] = lang
        self.update_texts()

    def select_bg(self, key):
        for k, btn in self.bg_buttons.items():
            if k == key:
                btn.setChecked(True)
                btn.setStyleSheet("border: 2px solid #4facfe; border-radius: 8px;")
            else:
                btn.setChecked(False)
                btn.setStyleSheet("border: 2px solid transparent; border-radius: 8px;")
        self.config["page_bg"] = key

    def browse_java(self):
        file, _ = QFileDialog.getOpenFileName(
            self, self.tr("Browse Java path"), "", "Executable Files (*.exe);;All Files (*)"
        )
        if file:
            self.java_path_input.setText(file)

    def _open_java_downloader(self):
        dlg = JavaDownloaderDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted and dlg.selected_path:
            self.java_path_input.setText(dlg.selected_path)

    def auto_detect_java(self):
        found = []
        candidates = [
            os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "Java"),
            os.path.join(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"), "Java"),
            os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "Adoptium"),
            os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "Zulu"),
            os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "Oracle"),
            os.path.expanduser("~\\AppData\\Local\\Packages\\*\\jre"),
            "C:\\Program Files\\Eclipse Adoptium",
            "C:\\Program Files\\Microsoft\\jdk",
        ]
        for base in candidates:
            if not os.path.isdir(base):
                continue
            for root, dirs, files in os.walk(base):
                for f in files:
                    if f.lower() == "javaw.exe" or f.lower() == "java.exe":
                        full = os.path.join(root, f)
                        try:
                            ver = subprocess.check_output([full, "-version"], stderr=subprocess.STDOUT, timeout=5).decode("utf-8", errors="replace")
                            if "version" in ver:
                                found.append(full)
                        except Exception:
                            pass
                        if len(found) >= 5:
                            break
                if len(found) >= 5:
                    break
            if len(found) >= 5:
                break

        if not found:
            QMessageBox.information(self, "Java", "Java не найдена. Установи Java 17+ с adoptium.net")
            return

        if len(found) == 1:
            self.java_path_input.setText(found[0])
            QMessageBox.information(self, "Java", f"Найдена: {found[0]}")
        else:
            items = "\n".join(f"{i+1}. {p}" for i, p in enumerate(found[:10]))
            QMessageBox.information(self, "Java",
                f"Найдено несколько:\n{items}\n\nВыбери через «Обзор» нужную.")
            self.java_path_input.setText(found[0])

    def test_cf_key(self):
        key = self.cf_key_input.text().strip()
        if not key:
            QMessageBox.warning(self, "Ошибка", "Введите API ключ")
            return
        try:
            resp = requests.get(
                f"{CURSEFORGE_API}/mods/search?gameId=432&classId=6&pageSize=1",
                headers={"x-api-key": key, "Accept": "application/json"}, timeout=10)
            if resp.status_code == 200:
                QMessageBox.information(self, "Успех", "✅ Ключ работает! CurseForge API отвечает.")
            else:
                QMessageBox.critical(self, "Ошибка",
                    f"❌ Ключ не работает. HTTP {resp.status_code}: {resp.text[:200]}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"❌ Не удалось проверить ключ:\n{e}")

    def save_settings(self):
        self.config["theme"] = self.theme_combo.currentText()
        self.config["language"] = self.lang_combo.currentText()
        self.config["launch_mode"] = "java" if self.rb_java.isChecked() else "launcher_lib"
        self.config["java_path"] = self.java_path_input.text()
        self.config["page_bg"] = self.config.get("page_bg", "dark")
        self.config["max_ram"] = self.ram_slider.value()
        self.config["jvm_args"] = self.jvm_input.text()
        self.config["curseforge_api_key"] = self.cf_key_input.text().strip()
        self.config["azure_client_id"] = self.azure_input.text().strip()
        self.config["minimize_to_tray"] = self.tray_check.isChecked()
        self.config["autostart"] = self.autostart_check.isChecked()
        self.config["rpc_custom_status"] = self.rpc_status_input.text()
        save_config(self.config)
        self._apply_autostart()
        invalidate_cf_api_key_cache()
        self.update_texts()

    def export_settings(self):
        path, _ = QFileDialog.getSaveFileName(self, "Экспорт настроек", "superlauncher_settings.json",
            "JSON (*.json)")
        if not path:
            return
        import shutil
        try:
            shutil.copy2(CONFIG_FILE, path)
            QMessageBox.information(self, "Готово", f"Настройки экспортированы:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось экспортировать:\n{e}")

    def import_settings(self):
        path, _ = QFileDialog.getOpenFileName(self, "Импорт настроек", "",
            "JSON (*.json)")
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            reply = QMessageBox.question(self, "Подтверждение",
                "Загрузить импортированные настройки? Текущие будут перезаписаны.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply != QMessageBox.StandardButton.Yes:
                return
            from shutil import copy2
            copy2(path, CONFIG_FILE)
            self.config = load_config()
            self.refresh_ui()
            QMessageBox.information(self, "Готово", "Настройки импортированы.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось импортировать:\n{e}")

    def refresh_ui(self):
        self.theme_combo.setCurrentText(self.config.get("theme", "dark"))
        self.lang_combo.setCurrentText(self.config.get("language", "ru"))
        self.java_path_input.setText(self.config.get("java_path", ""))
        self.ram_slider.setValue(self.config.get("max_ram", 4096))
        self.jvm_input.setText(self.config.get("jvm_args", ""))
        self.cf_key_input.setText(self.config.get("curseforge_api_key", ""))
        self.azure_input.setText(self.config.get("azure_client_id", ""))
        launch_mode = self.config.get("launch_mode", "launcher_lib")
        if launch_mode == "java":
            self.rb_java.setChecked(True)
        else:
            self.rb_launcher_lib.setChecked(True)
        self.select_bg(self.config.get("page_bg", "dark"))
        self.tray_check.setChecked(self.config.get("minimize_to_tray", False))
        self.autostart_check.setChecked(self.config.get("autostart", False))
        preset_text = self.jvm_presets.currentText()
        if "Custom" not in preset_text:
            self.jvm_input.setText(self.config.get("jvm_args", ""))

    def pick_accent_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            hex_color = color.name()
            self.config["accent_color"] = hex_color
            save_config(self.config)

    def ram_boost(self):
        try:
            subprocess.run("ipconfig /flushdns", shell=True, capture_output=True)
        except Exception:
            pass
        QMessageBox.information(self, "RAM Boost", "Готово!")

    def on_jvm_preset_changed(self, preset):
        if preset == "Custom":
            return
        args = preset.split(" ", 1)[1] if " " in preset else ""
        self.jvm_input.setText(args)

    def _open_jvm_generator(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("JVM Args Generator")
        layout = QVBoxLayout(dialog)
        flags = {
            "Use G1GC": "-XX:+UseG1GC",
            "Unlock Experimental": "-XX:+UnlockExperimentalVMOptions",
            "Disable Explicit GC": "-XX:+DisableExplicitGC",
            "Parallel Ref Proc": "-XX:+ParallelRefProcEnabled",
            "Aggressive Opts": "-XX:+AggressiveOpts",
            "Use Large Pages": "-XX:+UseLargePages",
        }
        checkboxes = {}
        for label, arg in flags.items():
            cb = QCheckBox(label)
            cb.setData(arg)
            layout.addWidget(cb)
            checkboxes[label] = cb
        def apply():
            parts = []
            for cb in checkboxes.values():
                if cb.isChecked():
                    parts.append(cb.data())
            self.jvm_input.setText(" ".join(parts))
            dialog.accept()
        btn = QPushButton("Apply")
        btn.clicked.connect(apply)
        layout.addWidget(btn)
        dialog.exec()

    def test_java_version(self):
        java_path = self.java_path_input.text().strip()
        if not java_path:
            QMessageBox.warning(self, "Ошибка", "Укажите путь к Java")
            return
        try:
            result = subprocess.run([java_path, "-version"], capture_output=True, text=True, timeout=15)
            output = result.stderr if result.stderr else result.stdout
            QMessageBox.information(self, "Java Version", output.strip())
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось запустить Java:\n{e}")

    def show_test_notification(self):
        QMessageBox.information(self, "🔔 Тест уведомления", "Это тестовое уведомление!")

    def _clean_old_versions(self):
        versions_dir = os.path.join(minecraft_directory, "versions")
        if not os.path.isdir(versions_dir):
            QMessageBox.information(self, "Clean", "Папка versions не найдена")
            return
        folders = []
        for entry in os.listdir(versions_dir):
            full = os.path.join(versions_dir, entry)
            if os.path.isdir(full):
                try:
                    mtime = os.path.getmtime(full)
                    folders.append((entry, full, mtime))
                except:
                    pass
        folders.sort(key=lambda x: x[2], reverse=True)
        if len(folders) <= 5:
            QMessageBox.information(self, "Clean", f"Всего {len(folders)} версий, чистить не нужно")
            return
        to_delete = folders[5:]
        deleted = 0
        for name, full, _ in to_delete:
            try:
                shutil.rmtree(full, ignore_errors=True)
                deleted += 1
            except:
                pass
        QMessageBox.information(self, "Clean", f"Удалено {deleted} старых версий")

    def reset_config(self):
        reply = QMessageBox.question(self, "Сброс настроек",
            "Вы уверены? Все настройки будут сброшены.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply != QMessageBox.StandardButton.Yes:
            return
        try:
            if os.path.exists(CONFIG_FILE):
                os.remove(CONFIG_FILE)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось удалить файл:\n{e}")
            return
        self.config = load_config()
        self.refresh_ui()
        QMessageBox.information(self, "Готово", "Настройки сброшены.")

    def select_custom_background(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Выберите изображение", "",
            "Images (*.png *.jpg *.jpeg *.bmp *.gif);;All Files (*)"
        )
        if path:
            self.config["custom_bg"] = path
            save_config(self.config)

    def _open_proxy_settings(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Proxy Settings")
        layout = QFormLayout(dialog)
        host_input = QLineEdit(self.config.get("proxy_host", ""))
        port_input = QLineEdit(self.config.get("proxy_port", ""))
        user_input = QLineEdit(self.config.get("proxy_user", ""))
        pass_input = QLineEdit(self.config.get("proxy_pass", ""))
        pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addRow("Host:", host_input)
        layout.addRow("Port:", port_input)
        layout.addRow("Username:", user_input)
        layout.addRow("Password:", pass_input)
        def save_proxy():
            self.config["proxy_host"] = host_input.text()
            self.config["proxy_port"] = port_input.text()
            self.config["proxy_user"] = user_input.text()
            self.config["proxy_pass"] = pass_input.text()
            save_config(self.config)
            dialog.accept()
        btn = QPushButton("Save")
        btn.clicked.connect(save_proxy)
        layout.addRow(btn)
        dialog.exec()

    def _apply_autostart(self):
        if self.autostart_check.isChecked():
            try:
                startup = os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
                vbs_path = os.path.join(startup, "SuperLauncher.vbs")
                exe_path = os.path.abspath(sys.argv[0])
                with open(vbs_path, "w", encoding="utf-8") as f:
                    f.write(f'CreateObject("WScript.Shell").Run """{exe_path}"", 0, False\n')
            except Exception:
                pass
        else:
            try:
                startup = os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
                vbs_path = os.path.join(startup, "SuperLauncher.vbs")
                if os.path.exists(vbs_path):
                    os.remove(vbs_path)
            except Exception:
                pass


class IconLoadThread(QThread):
    icon_data = pyqtSignal(object, bytes)

    def __init__(self, items):
        super().__init__()
        self.items = items

    def run(self):
        for item, icon_url in self.items:
            try:
                resp = requests.get(icon_url, timeout=5)
                if resp.status_code == 200:
                    self.icon_data.emit(item, resp.content)
            except Exception:
                pass


class ModDownloadThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)
    speed_signal = pyqtSignal(str)

    def __init__(self, url, save_path):
        super().__init__()
        self.url = url
        self.save_path = save_path

    def run(self):
        try:
            start_time = time.time()
            with requests.get(self.url, stream=True) as r:
                r.raise_for_status()
                total = int(r.headers.get("content-length", 0))
                downloaded = 0

                with open(self.save_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            elapsed = time.time() - start_time
                            if elapsed > 0 and downloaded > 0:
                                speed = downloaded / elapsed
                                if speed > 1024 * 1024:
                                    speed_str = f"{speed / 1024 / 1024:.1f} MB/s"
                                else:
                                    speed_str = f"{speed / 1024:.1f} KB/s"
                                self.speed_signal.emit(speed_str)
                            if total > 0:
                                self.progress.emit(int(downloaded * 100 / total))
            self.finished.emit(self.save_path)
        except Exception as e:
            self.finished.emit(f"ERROR: {e}")


class DiscordRPCThread(threading.Thread):
    def __init__(self, main_window):
        super().__init__()
        self.client_id = "1405145554027155456"
        self.rpc = None
        self.main_window = main_window
        self.running = True
        self.connected = False
        self._page_index = 0

    def update_page(self, index):
        self._page_index = index

    def run(self):
        try:
            self.rpc = Presence(self.client_id)
            try:
                self.rpc.connect()
                self.connected = True
                print("Discord RPC connected successfully.")
            except Exception as e:
                print(f"Discord RPC not connected: {e}")
                self.connected = False
                return

            while self.running:
                page_names = ["Home", "Mods", "News", "Updates", "Servers", "Settings", "Minecraft"]
                idx = min(self._page_index, len(page_names) - 1)
                details = f"На странице: {page_names[idx]}"
                try:
                    cfg = load_config()
                    custom = cfg.get("rpc_custom_status", "")
                except:
                    custom = ""
                state = custom or "Суперлаунчер 2.0.0"

                try:
                    self.rpc.update(
                        details=details,
                        state=state,
                        large_image="superlauncher",
                        small_image="minecraft",
                        start=time.time()
                    )
                except Exception as e:
                    print(f"Discord RPC update error: {e}")

                time.sleep(15)
        except Exception as e:
            print(f"Discord RPC thread error: {e}")

    def stop(self):
        self.running = False
        if self.rpc and self.connected:
            try:
                self.rpc.close()
                print("Discord RPC closed successfully.")
            except Exception as e:
                print(f"Error closing Discord RPC: {e}")


class ModsPage(QWidget):
    MOD_SOURCES = ["Modrinth", "CurseForge"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.config = load_config()

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15)

        self.mods_dir = os.path.join(minecraft_directory, "mods")
        os.makedirs(self.mods_dir, exist_ok=True)

        # Заголовок
        self.title = QLabel()
        self.title.setStyleSheet("font-size: 26px; font-weight: bold; margin-bottom: 10px; color: white;")
        self.layout.addWidget(self.title)

        # Источник и поиск в одной строке
        search_row = QHBoxLayout()

        self.source_combo = QComboBox()
        self.source_combo.addItems(self.MOD_SOURCES)
        self.source_combo.setStyleSheet("""
            background-color: #2f2f2f; color: white;
            border: 1px solid #444; border-radius: 5px; padding: 3px;
        """)
        search_row.addWidget(self.source_combo)

        self.search_input = QLineEdit()
        self.search_input.returnPressed.connect(self.search_mods)
        self.search_input.setStyleSheet("""
            background-color: #2f2f2f; color: white;
            border: 1px solid #444; border-radius: 5px; padding: 5px;
        """)
        search_row.addWidget(self.search_input, 1)
        self.layout.addLayout(search_row)

        # Список результатов
        self.results_list = QListWidget()
        self.results_list.setIconSize(QSize(64, 64))
        self.results_list.setStyleSheet("""
            background-color: #2f2f2f; color: white;
            border: 1px solid #444; border-radius: 5px;
        """)
        self.layout.addWidget(self.results_list)

        # Кнопки
        buttons_layout = QHBoxLayout()
        self.open_folder_button = QPushButton()
        self.open_folder_button.clicked.connect(self.open_mods_folder)
        buttons_layout.addWidget(self.open_folder_button)

        self.delete_all_button = QPushButton()
        self.delete_all_button.setStyleSheet("background-color: #d9534f; color: white;")
        self.delete_all_button.clicked.connect(self.delete_all_mods)
        buttons_layout.addWidget(self.delete_all_button)

        self.bulk_install_button = QPushButton("📦 Install from ZIP")
        self.bulk_install_button.setStyleSheet("background-color: #ff9800; color: white;")
        self.bulk_install_button.clicked.connect(self._bulk_install_mods)
        buttons_layout.addWidget(self.bulk_install_button)

        self.buttons = {}
        self.buttons["check_updates"] = QPushButton("🔄 Check mod updates")
        self.buttons["check_updates"].setStyleSheet("background-color: #4facfe; color: white;")
        self.buttons["check_updates"].clicked.connect(self._check_mod_updates)
        buttons_layout.addWidget(self.buttons["check_updates"])

        self.layout.addLayout(buttons_layout)

        self._icon_thread = None
        self.load_featured_mods()
        self.update_texts()

    def tr(self, key: str) -> str:
        lang = self.config.get("language", "ru")
        return translations.get(lang, {}).get(key, key)

    def update_texts(self):
        src = self.source_combo.currentText()
        self.title.setText(f"🧩 {self.tr('Mods from')} {src}")
        self.search_input.setPlaceholderText(f"🔍 {self.tr('Search mod...')}")
        self.open_folder_button.setText(f"📂 {self.tr('Open mods folder')}")
        self.delete_all_button.setText(f"🗑 {self.tr('Delete all mods')}")

    def _connect_item_clicked(self):
        try:
            self.results_list.itemClicked.disconnect(self.show_mod_info)
        except TypeError:
            pass
        try:
            self.results_list.itemDoubleClicked.disconnect(self.show_mod_dialog)
        except TypeError:
            pass
        self.results_list.itemClicked.connect(self.show_mod_info)
        self.results_list.itemDoubleClicked.connect(self.show_mod_dialog)

    def _load_icons_bg(self, items_with_urls):
        if self._icon_thread is None or not self._icon_thread.isRunning():
            self._icon_thread = IconLoadThread(items_with_urls)
            self._icon_thread.icon_data.connect(self._on_icon_data)
            self._icon_thread.start()

    def _on_icon_data(self, item, data):
        try:
            pm = QPixmap()
            pm.loadFromData(data)
            if not pm.isNull():
                item.setIcon(QIcon(pm.scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio,
                                              Qt.TransformationMode.SmoothTransformation)))
        except Exception:
            pass

    def load_featured_mods(self):
        try:
            url = f"{MODRINTH_API}/search?limit=20&index=downloads"
            resp = requests.get(url, headers={"User-Agent": "SuperLauncher/2.0"}, timeout=10)
            data = resp.json()
            self.results_list.clear()
            icon_items = []
            for hit in data["hits"]:
                desc = hit.get("description", "")[:80]
                downloads = hit.get("downloads", 0)
                item = QListWidgetItem(f"{hit['title']} ⬇{downloads} — {desc}")
                item.setData(Qt.ItemDataRole.UserRole, ("modrinth", hit["project_id"], hit))
                self.results_list.addItem(item)
                if hit.get("icon_url"):
                    icon_items.append((item, hit["icon_url"]))
            self._connect_item_clicked()
            if icon_items:
                self._load_icons_bg(icon_items)
        except Exception as e:
            QMessageBox.critical(self, self.tr("Error"), str(e))

    def search_mods(self):
        query = self.search_input.text()
        if not query.strip():
            return
        source = self.source_combo.currentText()
        if source == "Modrinth":
            self._search_modrinth(query)
        else:
            self._search_curseforge(query)

    def _search_modrinth(self, query):
        try:
            url = f"{MODRINTH_API}/search?query={query}&limit=30&index=relevance"
            resp = requests.get(url, headers={"User-Agent": "SuperLauncher/2.0"}, timeout=10)
            data = resp.json()
            self.results_list.clear()
            icon_items = []
            for hit in data["hits"]:
                if hit.get("project_type") != "mod":
                    continue
                desc = hit.get("description", "")[:80]
                downloads = hit.get("downloads", 0)
                item = QListWidgetItem(f"{hit['title']} ⬇{downloads} — {desc}")
                item.setData(Qt.ItemDataRole.UserRole, ("modrinth", hit["project_id"], hit))
                self.results_list.addItem(item)
                if hit.get("icon_url"):
                    icon_items.append((item, hit["icon_url"]))
            self._connect_item_clicked()
            if icon_items:
                self._load_icons_bg(icon_items)
        except Exception as e:
            QMessageBox.critical(self, self.tr("Error"), str(e))

    def _search_curseforge(self, query):
        try:
            params = {
                "gameId": 432,
                "classId": 6,
                "searchFilter": query,
                "pageSize": 30,
                "sortField": 2,
                "sortOrder": "desc"
            }
            resp = requests.get(
                f"{CURSEFORGE_API}/mods/search",
                params=params,
                headers={
                    "x-api-key": get_cf_api_key(),
                    "Accept": "application/json"
                },
                timeout=15
            )
            data = resp.json()
            self.results_list.clear()
            icon_items = []
            for mod in data.get("data", []):
                name = mod.get("name", "Unknown")
                summary = mod.get("summary", "")[:80]
                downloads = mod.get("downloadCount", 0)
                item = QListWidgetItem(f"{name} ⬇{downloads} — {summary}")
                r = {"name": name, "description": summary, "downloads": downloads, "author": (mod.get("authors") or [{}])[0].get("name", "Unknown") if mod.get("authors") else "Unknown"}
                item.setData(Qt.ItemDataRole.UserRole, ("curseforge", mod["id"], r))
                self.results_list.addItem(item)
                logo = mod.get("logo", {})
                if logo and logo.get("url"):
                    icon_items.append((item, logo["url"]))
            self._connect_item_clicked()
            if icon_items:
                self._load_icons_bg(icon_items)
        except Exception as e:
            QMessageBox.critical(self, self.tr("Error"), f"CurseForge: {e}")

    def show_mod_info(self, item):
        data = item.data(Qt.ItemDataRole.UserRole)
        if len(data) >= 3:
            r = data[2]
            name = r.get("name") or r.get("title", "Unknown")
            desc = r.get("description", r.get("desc", "Нет описания"))[:200]
            downloads = r.get("downloads", r.get("downloadCount", 0))
            author = r.get("author", "Unknown")
            msg = f"<b>{name}</b><br><br>{desc}<br><br>⬇ Скачиваний: {downloads:,}<br>👤 Автор: {author}<br><br><i>Дважды кликните для установки</i>"
            QMessageBox.information(self, "Информация о моде", msg)

    def show_mod_dialog(self, item):
        source, mod_id = item.data(Qt.ItemDataRole.UserRole)
        if source == "modrinth":
            self._show_modrinth_dialog(mod_id)
        else:
            self._show_curseforge_dialog(mod_id)

    def _show_modrinth_dialog(self, project_id):
        try:
            versions_url = f"{MODRINTH_API}/project/{project_id}/version"
            resp = requests.get(versions_url, headers={"User-Agent": "SuperLauncher/2.0"})
            versions = resp.json()

            if not versions:
                QMessageBox.warning(self, self.tr("No available versions"),
                                    self.tr("No versions available"))
                return

            dialog = QDialog(self)
            dialog.setWindowTitle(self.tr("Install mod"))
            dialog.setMinimumWidth(400)
            layout = QVBoxLayout(dialog)

            version_box = QComboBox()
            version_loader_map = {}
            for v in versions:
                mc_versions = v.get("game_versions", [])
                loaders = v.get("loaders", [])
                if not mc_versions or not loaders:
                    continue
                ver_num = v.get("version_number", "?")
                display_text = f"{mc_versions[0]} | {loaders[0]} | {ver_num}"
                version_loader_map[display_text] = v

            if not version_loader_map:
                QMessageBox.warning(self, self.tr("No supported builds"),
                                    self.tr("No supported builds"))
                return

            version_box.addItems(version_loader_map.keys())
            layout.addWidget(QLabel(self.tr("Minecraft version and loader:")))
            layout.addWidget(version_box)

            install_button = QPushButton(self.tr("Install mod"))
            install_button.setStyleSheet("""
                background-color: #4facfe; color: white;
                border: none; border-radius: 5px; padding: 8px; font-weight: bold;
            """)
            layout.addWidget(install_button)

            install_button.clicked.connect(
                lambda: self._download_from_modrinth(version_loader_map[version_box.currentText()], dialog)
            )

            dialog.exec()
        except Exception as e:
            QMessageBox.critical(self, self.tr("Error"), str(e))

    def _download_from_modrinth(self, version_data, dialog):
        files = version_data.get("files", [])
        for file in files:
            if file.get("filename", "").endswith(".jar"):
                url = file["url"]
                filename = file["filename"]
                save_path = os.path.join(self.mods_dir, filename)
                dialog.close()
                self.start_download(url, save_path)
                return
        QMessageBox.warning(self, self.tr("File not found"), self.tr("File not found"))

    def _show_curseforge_dialog(self, mod_id):
        try:
            resp = requests.get(
                f"{CURSEFORGE_API}/mods/{mod_id}/files",
                headers={
                    "x-api-key": get_cf_api_key(),
                    "Accept": "application/json"
                },
                timeout=10
            )
            data = resp.json()
            files = data.get("data", [])

            if not files:
                QMessageBox.warning(self, self.tr("No available versions"),
                                    self.tr("No versions available"))
                return

            dialog = QDialog(self)
            dialog.setWindowTitle(self.tr("Install mod"))
            dialog.setMinimumWidth(500)
            layout = QVBoxLayout(dialog)

            file_box = QComboBox()
            file_map = {}
            LOADER_NAMES = {1: "Forge", 2: "Cauldron", 3: "LiteLoader", 4: "Fabric", 5: "Quilt", 6: "NeoForge"}
            for f in files[:30]:
                display_name = f.get("displayName", f.get("fileName", "?"))
                mc_ver = "?"
                file_loader = "?"
                for sgv in f.get("sortableGameVersions", []):
                    gv_type = sgv.get("gameVersionTypeId")
                    gv_name = sgv.get("gameVersionName", "")
                    if gv_type == 1:
                        mc_ver = gv_name
                    elif gv_type == 2:
                        file_loader = LOADER_NAMES.get(int(gv_name), gv_name) if gv_name.isdigit() else gv_name
                if mc_ver == "?":
                    mc_ver = next((v for v in f.get("gameVersions", []) if v and v[0].isdigit()), "?")
                dl_count = f.get("downloadCount", 0)
                release_type = {1: "Release", 2: "Beta", 3: "Alpha"}.get(f.get("releaseType"), "")
                label = f"{mc_ver} | {file_loader} | {display_name} ⬇{dl_count}"
                if release_type:
                    label += f" [{release_type}]"
                file_map[label] = f
                file_box.addItem(label)

            layout.addWidget(QLabel(self.tr("Select file:")))
            layout.addWidget(file_box)

            install_button = QPushButton(self.tr("Install mod"))
            install_button.setStyleSheet("""
                background-color: #f1642e; color: white;
                border: none; border-radius: 5px; padding: 8px; font-weight: bold;
            """)
            layout.addWidget(install_button)

            install_button.clicked.connect(
                lambda: self._download_from_curseforge(file_map[file_box.currentText()], dialog)
            )

            dialog.exec()
        except Exception as e:
            QMessageBox.critical(self, self.tr("Error"), f"CurseForge: {e}")

    def _download_from_curseforge(self, file_data, dialog):
        file_id = file_data.get("id")
        mod_id = file_data.get("modId")
        try:
            resp = requests.get(
                f"{CURSEFORGE_API}/mods/{mod_id}/files/{file_id}/download-url",
                headers={
                    "x-api-key": get_cf_api_key(),
                    "Accept": "application/json"
                },
                timeout=10
            )
            data = resp.json()
            dl_url = data.get("data", "")
            if not dl_url:
                # fallback: build URL manually
                filename = file_data.get("fileName", "mod.jar")
                dl_url = f"https://media.forgecdn.net/files/{file_id // 1000}/{file_id % 1000}/{filename}"

            filename = file_data.get("fileName", "mod.jar")
            save_path = os.path.join(self.mods_dir, filename)
            dialog.close()
            self.start_download(dl_url, save_path)
        except Exception as e:
            QMessageBox.critical(self, self.tr("Error"), f"CurseForge download: {e}")

    def start_download(self, url, save_path):
        self.progress_dialog = QDialog(self)
        self.progress_dialog.setWindowTitle(self.tr("Downloading mod"))
        self.progress_dialog.setModal(True)

        dialog_layout = QVBoxLayout(self.progress_dialog)
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        dialog_layout.addWidget(self.progress_bar)

        self.progress_dialog.show()

        self.download_thread = ModDownloadThread(url, save_path)
        self.download_thread.progress.connect(self.progress_bar.setValue)
        self.download_thread.finished.connect(self.on_download_finished)
        self.download_thread.start()

    def on_download_finished(self, result):
        self.progress_dialog.hide()
        if result.startswith("ERROR:"):
            QMessageBox.critical(self, self.tr("Error"), result)
        else:
            QMessageBox.information(self, self.tr("Done"),
                                    f"{self.tr('Mod installed successfully:')}\n{result}")

    def _check_mod_updates(self):
        if not os.path.isdir(self.mods_dir):
            QMessageBox.information(self, "Updates", "Папка модов не найдена")
            return
        updates = []
        for fn in os.listdir(self.mods_dir):
            if not fn.endswith(".jar"):
                continue
            mod_id = fn.split("-")[0] if "-" in fn else fn.replace(".jar", "")
            try:
                resp = requests.get(f"{MODRINTH_API}/project/{mod_id}/version",
                    headers={"User-Agent": "SuperLauncher/2.0"}, timeout=10)
                if resp.status_code == 200:
                    versions = resp.json()
                    if versions:
                        latest = versions[0].get("version_number", "")
                        if latest and latest not in fn:
                            updates.append(f"{fn} -> {latest}")
            except:
                pass
        if updates:
            QMessageBox.information(self, "Mod Updates",
                "Доступны обновления:\n\n" + "\n".join(updates))
        else:
            QMessageBox.information(self, "Mod Updates", "Обновлений не найдено")

    def open_mods_folder(self):
        path = os.path.realpath(self.mods_dir)
        if sys.platform == "win32":
            os.startfile(path)
        elif sys.platform == "darwin":
            os.system(f"open \"{path}\"")
        else:
            os.system(f"xdg-open \"{path}\"")

    def delete_all_mods(self):
        confirm = QMessageBox.question(
            self, self.tr("Delete all mods"),
            self.tr("Are you sure you want to delete all mods?"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            deleted = 0
            for file in os.listdir(self.mods_dir):
                if file.endswith(".jar"):
                    try:
                        os.remove(os.path.join(self.mods_dir, file))
                        deleted += 1
                    except Exception as e:
                        QMessageBox.warning(self, self.tr("Error"),
                                            f"{self.tr('Could not delete')} {file}: {e}")
            QMessageBox.information(self, self.tr("Done"),
                                    f"{self.tr('All mods deleted')}: {deleted}")

    def _bulk_install_mods(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Выберите .jar/.zip файлы модов", "", "Mods (*.jar *.zip)")
        if not files:
            return
        copied = 0
        for src in files:
            try:
                shutil.copy2(src, os.path.join(self.mods_dir, os.path.basename(src)))
                copied += 1
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Не удалось скопировать {os.path.basename(src)}:\n{e}")
        QMessageBox.information(self, "Готово", f"Установлено модов: {copied}")


class NewsPage(QWidget):
    def __init__(self, parent=None, language=None):
        super().__init__(parent)
        self.parent_window = parent
        config = load_config()
        self.language = language or config.get("language", "ru")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Заголовок
        self.title = QLabel()
        self.title.setStyleSheet("font-size: 26px; font-weight: bold; margin-bottom: 15px; color: white;")
        layout.addWidget(self.title)

        # Scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        layout.addWidget(self.scroll_area)

        self.container = QWidget()
        self.scroll_area.setWidget(self.container)
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(0, 0, 0, 0)
        self.container_layout.setSpacing(12)

        # Новости
        self.news_list = [
            ("2026-06-13 v3.0.0",
             "🎉 Мега-релиз! Полноценные инстансы, управление контентом, Java-детектор,"
             " публикация на Modrinth, FTB+Technic поиск, OAuth PKCE, AI ассистент,"
             " менеджер скинов/ресурспаков/шейдеров/миров/скриншотов, Java-загрузчик"),
            ("2026-06-13 v2.0.0",
             "Система инстансов с изоляцией .minecraft, импорт/экспорт .mrpack,"
             " модпадки с Modrinth/CurseForge/FTB/Technic, авторизация Microsoft+Ely.by+Offline,"
             " лог-вьюер, AI агент (Ollama), новый дизайн"),
            ("2025-08-12 v1.4.0.7", "Добавлен Discord RPC"),
            ("2025-07-24 v1.4.0.5", "Добавлена поддержка скачивания модов из Modrinth и настроек лаунчера"),
            ("2025-07-23 v1.4.0.4",
             "Добавлена возможность создавать и управлять локальными Minecraft-серверами прямо из лаунчера..."),
            ("2025-07-23 v1.4.0.3", "Добавлен новый дизайн и восстановлен код"),
            ("2025-06-26 v1.4.0.2", "Добавлен новый дизайн, но утерян код"),
            ("2025-06-26 v1.4.0.1", "Исправлены баги, но дизайн устаревший"),
            ("2025-06-26 v1.4.0.0", "Исправлены баги, но дизайн устаревший"),
            ("2025-06-26 v1.3", "Лаунчер выйдет из бета в следующем релизе")
        ]

        self.news_labels = []  # Сохраняем лейблы для обновления текста
        self.update_texts()
        self.populate_news()

    def _tr(self, text):
        return translations.get(self.language, {}).get(text, text)

    def update_texts(self):
        self.title.setText(self._tr("News"))

    def populate_news(self):
        # Очищаем контейнер перед заполнением
        for i in reversed(range(self.container_layout.count())):
            widget = self.container_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # Добавление новостей
        for date, text in self.news_list:
            translated_text = self._tr(text)
            news_label = QLabel(f"<b>{date}</b>: {translated_text}")
            news_label.setWordWrap(True)
            news_label.setStyleSheet("font-size: 16px; color: #c0c0c0;")
            self.container_layout.addWidget(news_label)
            self.news_labels.append(news_label)

        self.container_layout.addStretch()

    def set_language(self, language):
        self.language = language
        self.update_texts()
        self.populate_news()


class UpdateDownloadThread(QThread):
    progress = pyqtSignal(int)
    speed = pyqtSignal(str)
    finished = pyqtSignal(str)

    def __init__(self, url, filename):
        super().__init__()
        self.url = url
        self.filename = filename

    def run(self):
        try:
            with requests.get(self.url, stream=True, timeout=30) as r:
                r.raise_for_status()
                total = int(r.headers.get("content-length", 0))
                downloaded = 0
                start = time.time()
                with open(self.filename, "wb") as f:
                    for chunk in r.iter_content(chunk_size=65536):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            if total > 0:
                                pct = int(downloaded * 100 / total)
                                self.progress.emit(pct)
                                elapsed = time.time() - start
                                if elapsed > 0:
                                    speed_bps = downloaded / elapsed
                                    if speed_bps > 1048576:
                                        speed_str = f"{speed_bps/1048576:.1f} MB/s"
                                    else:
                                        speed_str = f"{speed_bps/1024:.0f} KB/s"
                                    eta = (total - downloaded) / speed_bps if speed_bps > 0 else 0
                                    self.speed.emit(f"{speed_str} | ETA: {eta:.0f}s")
            self.finished.emit(str(self.filename))
        except Exception as e:
            self.finished.emit(f"ERROR: {str(e)}")


class UpdatesPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.releases = []
        self.download_url = None
        self.download_version = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        # === HEADER ===
        header = QHBoxLayout()
        self.title = QLabel("🔄 Обновления")
        self.title.setStyleSheet("font-size: 26px; font-weight: bold; color: white;")
        header.addWidget(self.title)
        header.addStretch()

        self.btn_refresh = QPushButton("⟳ Проверить")
        self.btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_refresh.setStyleSheet(
            "QPushButton { background: #4facfe; color: white; border: none; "
            "border-radius: 6px; padding: 8px 18px; font-weight: bold; }"
            "QPushButton:hover { background: #3a8ed9; }")
        self.btn_refresh.clicked.connect(self.check_for_updates)
        header.addWidget(self.btn_refresh)
        layout.addLayout(header)

        # === CURRENT VERSION CARD ===
        self.version_card = QFrame()
        self.version_card.setStyleSheet(
            "QFrame { background: rgba(79, 172, 254, 0.1); border: 1px solid rgba(79,172,254,0.3); "
            "border-radius: 12px; padding: 16px; }")
        vc_layout = QHBoxLayout(self.version_card)
        vc_layout.setContentsMargins(16, 12, 16, 12)

        vc_icon = QLabel("📦")
        vc_icon.setStyleSheet("font-size: 32px;")
        vc_layout.addWidget(vc_icon)

        vc_info = QVBoxLayout()
        vc_info.setSpacing(2)
        vc_title = QLabel("Текущая версия")
        vc_title.setStyleSheet("color: #888; font-size: 12px;")
        vc_info.addWidget(vc_title)
        self.vc_version = QLabel(CURRENT_VERSION)
        self.vc_version.setStyleSheet("color: white; font-size: 22px; font-weight: bold;")
        vc_info.addWidget(self.vc_version)
        vc_layout.addLayout(vc_info)
        vc_layout.addStretch()

        self.vc_status = QLabel()
        self.vc_status.setStyleSheet("color: #4caf50; font-size: 13px; font-weight: bold;")
        vc_layout.addWidget(self.vc_status)

        self.vc_channel = QLabel()
        self.vc_channel.setStyleSheet("color: #888; font-size: 12px;")
        vc_layout.addWidget(self.vc_channel)

        layout.addWidget(self.version_card)

        # === UPDATE AVAILABLE CARD ===
        self.update_card = QFrame()
        self.update_card.setVisible(False)
        self.update_card.setStyleSheet(
            "QFrame { background: rgba(76, 175, 80, 0.1); border: 1px solid rgba(76,175,80,0.4); "
            "border-radius: 12px; padding: 16px; }")
        uc_layout = QVBoxLayout(self.update_card)
        uc_layout.setContentsMargins(16, 12, 16, 12)
        uc_layout.setSpacing(8)

        uc_header = QHBoxLayout()
        self.uc_icon = QLabel("⬆")
        self.uc_icon.setStyleSheet("font-size: 28px;")
        uc_header.addWidget(self.uc_icon)
        self.uc_title = QLabel()
        self.uc_title.setStyleSheet("color: #4caf50; font-size: 18px; font-weight: bold;")
        uc_header.addWidget(self.uc_title)
        uc_header.addStretch()
        self.uc_badge = QLabel()
        self.uc_badge.setStyleSheet(
            "background: #4caf50; color: white; padding: 2px 10px; "
            "border-radius: 4px; font-size: 11px; font-weight: bold;")
        uc_header.addWidget(self.uc_badge)
        uc_layout.addLayout(uc_header)

        self.uc_changelog = QLabel()
        self.uc_changelog.setWordWrap(True)
        self.uc_changelog.setStyleSheet("color: #ccc; font-size: 13px; padding: 4px 0;")
        uc_layout.addWidget(self.uc_changelog)

        uc_actions = QHBoxLayout()
        self.btn_download = QPushButton("⬇ Скачать и установить")
        self.btn_download.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_download.setStyleSheet(
            "QPushButton { background: #4caf50; color: white; border: none; "
            "border-radius: 6px; padding: 10px 24px; font-weight: bold; font-size: 14px; }"
            "QPushButton:hover { background: #43a047; }"
            "QPushButton:disabled { background: #555; }")
        self.btn_download.clicked.connect(self.start_download)
        uc_actions.addWidget(self.btn_download)

        self.btn_skip = QPushButton("Пропустить")
        self.btn_skip.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_skip.setStyleSheet(
            "QPushButton { background: transparent; color: #888; border: 1px solid #555; "
            "border-radius: 6px; padding: 10px 16px; font-size: 13px; }"
            "QPushButton:hover { color: white; border-color: #888; }")
        self.btn_skip.clicked.connect(lambda: self.update_card.setVisible(False))
        uc_actions.addWidget(self.btn_skip)
        uc_actions.addStretch()
        uc_layout.addLayout(uc_actions)

        # progress bar + speed
        self.download_progress = QProgressBar()
        self.download_progress.setVisible(False)
        self.download_progress.setStyleSheet(
            "QProgressBar { border: 1px solid #4caf50; border-radius: 6px; text-align: center; "
            "height: 22px; background: #1a1a2e; color: white; }"
            "QProgressBar::chunk { background: qlineargradient(x1:0,y1:0,x2:1,y2:0, "
            "stop:0 #4caf50, stop:1 #81c784); border-radius: 5px; }")
        uc_layout.addWidget(self.download_progress)

        self.download_speed = QLabel()
        self.download_speed.setVisible(False)
        self.download_speed.setStyleSheet("color: #888; font-size: 11px;")
        uc_layout.addWidget(self.download_speed)

        layout.addWidget(self.update_card)

        # === RELEASE NOTES / VERSION HISTORY ===
        notes_label = QLabel("📋 История версий")
        notes_label.setStyleSheet("font-size: 18px; font-weight: bold; color: white; margin-top: 8px;")
        layout.addWidget(notes_label)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        self.release_list = QListWidget()
        self.release_list.setStyleSheet(
            "QListWidget { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); "
            "border-radius: 8px; padding: 4px; color: white; font-size: 13px; }"
            "QListWidget::item { padding: 8px; border-radius: 4px; }"
            "QListWidget::item:hover { background: rgba(255,255,255,0.08); }"
            "QListWidget::item:selected { background: rgba(79,172,254,0.3); }")
        self.release_list.currentRowChanged.connect(self.on_release_selected)
        splitter.addWidget(self.release_list)

        self.release_notes = QTextEdit()
        self.release_notes.setReadOnly(True)
        self.release_notes.setStyleSheet(
            "QTextEdit { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); "
            "border-radius: 8px; padding: 12px; color: #ccc; font-size: 13px; }")
        splitter.addWidget(self.release_notes)

        splitter.setSizes([250, 450])
        layout.addWidget(splitter, stretch=1)

        self.status_label = QLabel("Нажмите «Проверить» для поиска обновлений")
        self.status_label.setStyleSheet("color: #666; font-size: 12px;")
        layout.addWidget(self.status_label)

        QTimer.singleShot(500, self.check_for_updates)

    def check_for_updates(self):
        self.btn_refresh.setEnabled(False)
        self.btn_refresh.setText("⟳ Поиск...")
        self.status_label.setText("Проверка обновлений...")

        def task():
            try:
                # GitHub Releases API — все релизы
                url = "https://api.github.com/repos/Ludvig2457Ultra/SuperLauncherMC/releases?per_page=20"
                resp = requests.get(url, timeout=15,
                    headers={"Accept": "application/vnd.github.v3+json"})
                if resp.status_code != 200:
                    QTimer.singleShot(0, lambda: self.status_label.setText(
                        f"Ошибка API GitHub: {resp.status_code}"))
                    return

                data = resp.json()
                releases = []
                for r in data:
                    tag = r.get("tag_name", "")
                    name = r.get("name", tag)
                    body = r.get("body", "") or ""
                    published = r.get("published_at", "")[:10]
                    prerelease = r.get("prerelease", False)
                    assets = r.get("assets", [])
                    dl_url = ""
                    for a in assets:
                        if a.get("name", "").endswith(".exe"):
                            dl_url = a.get("browser_download_url", "")
                            break
                    if not dl_url:
                        for a in assets:
                            if a.get("name", "").endswith(".py"):
                                dl_url = a.get("browser_download_url", "")
                                break
                    try:
                        v = packaging_version.parse(tag)
                    except Exception:
                        continue
                    releases.append({
                        "tag": tag, "name": name, "body": body,
                        "date": published, "prerelease": prerelease,
                        "dl_url": dl_url, "version": v
                    })

                releases.sort(key=lambda x: x["version"], reverse=True)
                self.releases = releases

                # Fill list
                QTimer.singleShot(0, self.populate_release_list)

                # Check for new version
                current_v = packaging_version.parse(CURRENT_VERSION)
                for r in releases:
                    if r["version"] > current_v and r["dl_url"]:
                        self.download_url = r["dl_url"]
                        self.download_version = r["tag"]
                        QTimer.singleShot(0, lambda v=r: self.show_update(v))
                        return

                QTimer.singleShot(0, self.show_up_to_date)

            except Exception as e:
                QTimer.singleShot(0, lambda: self.status_label.setText(f"Ошибка: {e}"))
            finally:
                QTimer.singleShot(0, lambda: self.btn_refresh.setEnabled(True))
                QTimer.singleShot(0, lambda: self.btn_refresh.setText("⟳ Проверить"))

        from threading import Thread
        Thread(target=task, daemon=True).start()

    def populate_release_list(self):
        self.release_list.blockSignals(True)
        self.release_list.clear()
        for r in self.releases:
            badge = " 🔧" if r["prerelease"] else ""
            text = f"{r['tag']}{badge}  {r['date']}"
            item = QListWidgetItem(text)
            item.setData(Qt.ItemDataRole.UserRole, r["tag"])
            if r["prerelease"]:
                item.setForeground(QColor("#ff9800"))
            else:
                item.setForeground(QColor("white"))
            self.release_list.addItem(item)
        self.release_list.blockSignals(False)
        if self.releases:
            self.release_list.setCurrentRow(0)

    def on_release_selected(self, row):
        if row < 0 or row >= len(self.releases):
            return
        r = self.releases[row]
        body = r.get("body", "Нет описания.")
        # Strip HTML, keep markdown-ish
        import html
        safe_body = html.escape(body)
        # Simple markdown-like rendering
        lines = safe_body.split("\n")
        html_lines = []
        for line in lines:
            if line.startswith("## "):
                html_lines.append(f"<h3 style='color:#4facfe;'>{line[3:]}</h3>")
            elif line.startswith("### "):
                html_lines.append(f"<h4 style='color:#81c784;'>{line[4:]}</h4>")
            elif line.startswith("- ") or line.startswith("* "):
                html_lines.append(f"• {line[2:]}")
            elif line.startswith("**") and line.endswith("**"):
                html_lines.append(f"<b>{line[2:-2]}</b>")
            else:
                html_lines.append(line)
        html_content = "<br>".join(html_lines)
        header = f"<h2 style='color:white;'>{r['tag']}</h2>"
        meta = f"<p style='color:#888; font-size:12px;'>{r['date']}" + \
               (" | 🔧 Предрелиз</p>" if r["prerelease"] else "</p>")
        self.release_notes.setHtml(header + meta + "<hr>" + html_content)

    def show_update(self, release):
        self.update_card.setVisible(True)
        self.uc_title.setText(f"Доступна версия {release['tag']}")
        self.uc_badge.setText("НОВОЕ")
        # First line of body as summary
        body = release.get("body", "")
        summary = body.split("\n")[0] if body else "Обновление доступно для скачивания."
        if len(summary) > 120:
            summary = summary[:117] + "..."
        self.uc_changelog.setText(summary)
        self.vc_status.setText(f"⬆ Доступно обновление: {release['tag']}")
        self.vc_status.setStyleSheet("color: #4caf50; font-size: 13px; font-weight: bold;")

    def show_up_to_date(self):
        self.vc_status.setText("✓ Установлена последняя версия")
        self.vc_status.setStyleSheet("color: #4caf50; font-size: 13px; font-weight: bold;")
        self.status_label.setText(f"Последняя проверка: {datetime.datetime.now().strftime('%H:%M:%S')}")

    def start_download(self):
        if not self.download_url or not self.download_version:
            return

        filename = Path(__file__).parent / f"SuperLauncher_{self.download_version}.exe"
        self.btn_download.setEnabled(False)
        self.btn_download.setText("⏳ Загрузка...")
        self.download_progress.setVisible(True)
        self.download_progress.setValue(0)
        self.download_speed.setVisible(True)
        self.download_speed.setText("Подготовка...")
        self.status_label.setText(f"Загрузка {self.download_version}...")

        self.dl_thread = UpdateDownloadThread(self.download_url, str(filename))
        self.dl_thread.progress.connect(self.download_progress.setValue)
        self.dl_thread.speed.connect(self.download_speed.setText)
        self.dl_thread.finished.connect(self.on_download_finished)
        self.dl_thread.start()

    def on_download_finished(self, result):
        self.download_progress.setVisible(False)
        self.download_speed.setVisible(False)
        self.btn_download.setEnabled(True)
        self.btn_download.setText("⬇ Скачать и установить")

        if result.startswith("ERROR:"):
            QMessageBox.critical(self, "Ошибка", result)
            self.status_label.setText("Ошибка загрузки")
            return

        reply = QMessageBox.question(self, "Обновление",
            f"Версия {self.download_version} загружена.\n"
            "Запустить установку? Текущий лаунчер закроется.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            subprocess.Popen([result], close_fds=True)
            QApplication.quit()


class CreateServerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = load_config()
        self.setWindowTitle(self.tr("Create your own server"))
        self.setFixedSize(400, 300)

        layout = QFormLayout(self)

        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText(self.tr("Server Name"))

        self.input_port = QLineEdit()
        self.input_port.setPlaceholderText(self.tr("Port (e.g., 25565)"))
        self.input_port.setText("25565")

        self.combo_version = QComboBox()
        self.combo_version.setMinimumContentsLength(12)

        self.combo_core = QComboBox()
        self.combo_core.addItems(["Paper", "Purpur", "Vanilla", "Fabric", "Quilt"])
        self.combo_core.currentTextChanged.connect(self.on_core_changed)

        self.ram_slider = QSlider(Qt.Orientation.Horizontal)
        self.ram_slider.setMinimum(1)
        self.ram_slider.setMaximum(16)
        self.ram_slider.setValue(4)
        self.ram_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.ram_slider.setTickInterval(1)
        self.ram_slider.valueChanged.connect(self.on_ram_changed)
        self.ram_label = QLabel(f"4 {self.tr('RAM (GB):')}")
        self.ram_label.setStyleSheet("font-size: 12px; color: #ccc;")

        ram_widget = QWidget()
        ram_layout = QVBoxLayout(ram_widget)
        ram_layout.setContentsMargins(0, 0, 0, 0)
        ram_layout.addWidget(self.ram_slider)
        ram_layout.addWidget(self.ram_label)

        layout.addRow(self.tr("Server Name") + ":", self.input_name)
        layout.addRow(self.tr("Port") + ":", self.input_port)
        layout.addRow(self.tr("Version") + ":", self.combo_version)
        layout.addRow(self.tr("Core") + ":", self.combo_core)
        layout.addRow(self.tr("RAM (GB):") + ":", ram_widget)

        btn_layout = QHBoxLayout()
        self.btn_create = QPushButton(self.tr("Create"))
        self.btn_cancel = QPushButton(self.tr("Cancel"))
        btn_layout.addWidget(self.btn_create)
        btn_layout.addWidget(self.btn_cancel)
        layout.addRow(btn_layout)

        self.btn_create.clicked.connect(self.create_server)
        self.btn_cancel.clicked.connect(self.reject)

        self.fetch_versions()

    def tr(self, key: str) -> str:
        lang = self.config.get("language", "ru")
        return translations.get(lang, {}).get(key, key)

    def refresh_language(self):
        self.setWindowTitle(self.tr("Create your own server"))
        layout = self.layout()
        self.input_name.setPlaceholderText(self.tr("Server Name"))
        self.input_port.setPlaceholderText(self.tr("Port (e.g., 25565)"))
        if layout.labelForField(self.input_name):
            layout.labelForField(self.input_name).setText(self.tr("Server Name") + ":")
        if layout.labelForField(self.input_port):
            layout.labelForField(self.input_port).setText(self.tr("Port") + ":")
        if layout.labelForField(self.combo_version):
            layout.labelForField(self.combo_version).setText(self.tr("Version") + ":")
        if layout.labelForField(self.combo_core):
            layout.labelForField(self.combo_core).setText(self.tr("Core") + ":")
        if layout.labelForField(self.ram_slider):
            layout.labelForField(self.ram_slider).setText(self.tr("RAM (GB):") + ":")
        self.btn_create.setText(self.tr("Create"))
        self.btn_cancel.setText(self.tr("Cancel"))
        self.on_ram_changed(self.ram_slider.value())

    def on_ram_changed(self, val):
        self.ram_label.setText(f"{val} GB")

    def on_core_changed(self, core):
        self.fetch_versions()

    def fetch_versions(self):
        self.combo_version.clear()
        self.combo_version.addItem(self.tr("Loading..."))
        from threading import Thread
        core = self.combo_core.currentText().lower()

        def task():
            try:
                versions = []
                if core in ("paper", "purpur"):
                    if core == "paper":
                        resp = requests.get("https://api.papermc.io/v2/projects/paper", timeout=10)
                        versions = resp.json().get("versions", [])
                    elif core == "purpur":
                        resp = requests.get("https://api.purpurmc.org/v2/purpur", timeout=10)
                        versions = list(resp.json().get("versions", {}).keys())
                    versions = sorted(versions, key=lambda x: [int(p) if p.isdigit() else p for p in x.split(".")], reverse=True)
                elif core in ("vanilla", "fabric", "quilt"):
                    resp = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json", timeout=10)
                    manifest = resp.json()
                    versions = [v["id"] for v in manifest["versions"] if v["type"] == "release"]
                    versions.sort(key=lambda x: [int(p) if p.isdigit() else p for p in x.split(".")], reverse=True)
                if versions:
                    self.combo_version.clear()
                    self.combo_version.addItems(versions)
                else:
                    self.combo_version.clear()
                    self.combo_version.addItem("1.20.4")
            except Exception:
                self.combo_version.clear()
                self.combo_version.addItems(["1.20.4", "1.20.1", "1.19.4"])

        Thread(target=task, daemon=True).start()

    def create_server(self):
        name = self.input_name.text().strip()
        port = self.input_port.text().strip()
        version = self.combo_version.currentText()
        core = self.combo_core.currentText()

        if not name or not port.isdigit():
            QMessageBox.warning(self, self.tr("Error"), self.tr("Please enter a valid server name and port (number)."))
            return

        self.server_name = name
        self.server_port = int(port)
        self.server_version = version
        self.server_core = core
        self.ram_gb = self.ram_slider.value()
        self.accept()


class DownloadThread(QThread):
    progress_changed = pyqtSignal(int)
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, core, version, save_path):
        super().__init__()
        self.core = core
        self.version = version
        self.save_path = save_path

    def run(self):
        try:
            url = self.get_jar_url(self.core, self.version)
            r = requests.get(url, stream=True)
            r.raise_for_status()

            total_length = r.headers.get('content-length')
            if total_length is None:
                with open(self.save_path, 'wb') as f:
                    f.write(r.content)
                self.progress_changed.emit(100)
            else:
                total_length = int(total_length)
                downloaded = 0
                with open(self.save_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            percent = int(downloaded * 100 / total_length)
                            self.progress_changed.emit(percent)

            self.finished.emit()

        except Exception as e:
            self.error.emit(str(e))

    def get_jar_url(self, core, version):
        core = core.lower()
        if core == "paper":
            builds_url = f"https://api.papermc.io/v2/projects/paper/versions/{version}"
            resp = requests.get(builds_url)
            resp.raise_for_status()
            build = resp.json()["builds"][-1]
            return f"https://api.papermc.io/v2/projects/paper/versions/{version}/builds/{build}/downloads/paper-{version}-{build}.jar"

        elif core == "purpur":
            builds_url = f"https://api.purpurmc.org/v2/purpur/{version}"
            resp = requests.get(builds_url)
            resp.raise_for_status()
            build = resp.json()["builds"][-1]
            return f"https://api.purpurmc.org/v2/purpur/{version}/{build}/download"

        elif core == "vanilla":
            manifest = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json").json()
            version_data = next((v for v in manifest["versions"] if v["id"] == version), None)
            if not version_data:
                raise Exception(f"Версия {version} не найдена")
            version_json = requests.get(version_data["url"]).json()
            return version_json["downloads"]["server"]["url"]

        elif core == "fabric":
            loader_ver = requests.get("https://meta.fabricmc.net/v2/versions/loader", timeout=10).json()
            installer_ver = requests.get("https://meta.fabricmc.net/v2/versions/installer", timeout=10).json()
            loader = loader_ver[0]["version"]
            installer = installer_ver[0]["version"]
            return f"https://meta.fabricmc.net/v2/versions/loader/{version}/{loader}/{installer}/server/jar"

        elif core == "quilt":
            meta = requests.get("https://meta.quiltmc.org/v3/versions/loader", timeout=10).json()
            loader = meta[0]["version"]
            installer = requests.get("https://meta.quiltmc.org/v3/versions/installer", timeout=10).json()[0]["version"]
            return f"https://meta.quiltmc.org/v3/downloads/installer/installer-{installer}.jar"

        else:
            raise Exception(f"Ядро {core} не поддерживается")


class PluginInstallThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, slug, game_version, loader, plugins_folder):
        super().__init__()
        self.slug = slug
        self.game_version = game_version
        self.loader = loader
        self.plugins_folder = plugins_folder

    def run(self):
        try:
            url = f"{MODRINTH_API}/project/{self.slug}/version"
            headers = {"User-Agent": "SuperLauncher/2.0"}
            resp = requests.get(url, headers=headers, timeout=15)
            resp.raise_for_status()
            versions = resp.json()

            loaders_to_try = [self.loader]
            if self.loader == "paper":
                loaders_to_try.append("bukkit")
            elif self.loader == "purpur":
                loaders_to_try.extend(["bukkit", "paper"])
            elif self.loader == "bukkit":
                loaders_to_try.extend(["paper", "purpur"])

            match = None
            for v in versions:
                gv = v.get("game_versions", [])
                loaders = v.get("loaders", [])
                if (not self.game_version or self.game_version in gv) and any(l in loaders for l in loaders_to_try):
                    match = v
                    break
            if not match:
                self.error.emit(f"No version found for {self.game_version or 'any'} / {self.loader}")
                return

            files = match.get("files", [])
            if not files:
                self.error.emit("No files in version")
                return

            file_info = files[0]
            dl_url = file_info.get("url")
            filename = file_info.get("filename", f"{self.slug}.jar")
            save_path = os.path.join(self.plugins_folder, filename)

            r = requests.get(dl_url, stream=True, timeout=30)
            r.raise_for_status()
            total = int(r.headers.get("content-length", 0))
            downloaded = 0
            with open(save_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total > 0:
                            self.progress.emit(int(downloaded * 100 / total))
            self.finished.emit(save_path)
        except Exception as e:
            self.error.emit(str(e))


class ServerProcessThread(QThread):
    output_line = pyqtSignal(str)
    started = pyqtSignal()
    stopped = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, server_path, start_command, ram_gb=4):
        super().__init__()
        self.server_path = server_path
        self.start_command = start_command
        self.ram_gb = ram_gb
        self.process = None
        self._running = False

    def run(self):
        bat_path = os.path.join(self.server_path, "start.bat")
        try:
            with open(bat_path, "w", encoding="utf-8") as f:
                f.write(f"""@echo off
java -Xmx{self.ram_gb}G -Xms{self.ram_gb}G -jar server.jar nogui
""")
            self.process = subprocess.Popen(
                bat_path, cwd=self.server_path, shell=True,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, encoding="utf-8", errors="replace"
            )
            self._running = True
            self.started.emit()
            for line in iter(self.process.stdout.readline, ""):
                if not self._running:
                    break
                if line:
                    self.output_line.emit(line.rstrip("\r\n"))
            self.process.wait()
        except Exception as e:
            self.error.emit(str(e))
        finally:
            self._running = False
            self.stopped.emit()

    def start_server(self):
        if not self.isRunning():
            self.start()

    def stop_server(self):
        self._running = False
        if self.process and self.process.poll() is None:
            try:
                self.process.stdin.write("stop\n")
                self.process.stdin.flush()
            except Exception:
                pass
            try:
                self.process.wait(timeout=10)
            except Exception:
                try:
                    self.process.kill()
                except Exception:
                    pass

    def send_command(self, cmd):
        if self.process and self.process.poll() is None:
            try:
                self.process.stdin.write(cmd + "\n")
                self.process.stdin.flush()
            except Exception:
                pass


class ServerControlDialog(QDialog):
    def __init__(self, server_name, server_path, ram_gb=4, server_version='', server_core='', parent=None):
        super().__init__(parent)
        self.config = load_config()
        self.server_name = server_name
        self.server_path = server_path
        self.ram_gb = ram_gb
        self.server_version = server_version
        self.server_core = server_core
        self.server_thread = ServerProcessThread(server_path, "", ram_gb)
        self.playit_process = None
        self.plugin_install_thread = None

        self.setWindowTitle(self.tr("Manage server") + f" '{server_name}'")
        self.resize(700, 500)
        self.setMinimumSize(600, 400)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        main_layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # -- Console tab --
        self.console_tab = QWidget()
        console_layout = QVBoxLayout(self.console_tab)

        btn_row = QHBoxLayout()
        self.btn_start = QPushButton(self.tr("Start server"))
        self.btn_start.setStyleSheet("background-color: #4caf50; color: white; font-weight: bold; padding: 6px 16px; border-radius: 4px;")
        self.btn_stop = QPushButton(self.tr("Stop server"))
        self.btn_stop.setStyleSheet("background-color: #f44336; color: white; font-weight: bold; padding: 6px 16px; border-radius: 4px;")
        self.btn_stop.setEnabled(False)
        btn_row.addWidget(self.btn_start)
        btn_row.addWidget(self.btn_stop)
        btn_row.addStretch()
        console_layout.addLayout(btn_row)

        self.console_output = QTextEdit()
        self.console_output.setReadOnly(True)
        self.console_output.setStyleSheet("""
            background-color: #1a1a2e; color: #00ff00;
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: 12px; border: 1px solid #333; border-radius: 4px;
        """)
        console_layout.addWidget(self.console_output)

        cmd_row = QHBoxLayout()
        self.cmd_input = QLineEdit()
        self.cmd_input.setPlaceholderText(self.tr("Enter command..."))
        self.cmd_input.returnPressed.connect(self.send_console_command)
        self.btn_send = QPushButton(self.tr("Send"))
        self.btn_send.clicked.connect(self.send_console_command)
        cmd_row.addWidget(self.cmd_input)
        cmd_row.addWidget(self.btn_send)
        console_layout.addLayout(cmd_row)

        self.tabs.addTab(self.console_tab, self.tr("Console"))

        self.btn_start.clicked.connect(self.start_server)
        self.btn_stop.clicked.connect(self.stop_server)

        # -- Settings tab --
        self.settings_tab = QWidget()
        settings_layout = QVBoxLayout(self.settings_tab)

        self.checkbox_eula = QCheckBox(self.tr("I accept the EULA"))
        self.checkbox_offline = QCheckBox(self.tr("Enable offline mode (cracked)"))
        self.checkbox_playit = QCheckBox(self.tr("Use playit.gg (tunnel)"))

        self.spin_max_players = QSpinBox()
        self.spin_max_players.setRange(1, 100)
        self.spin_max_players.setValue(20)

        self.motd_edit = QLineEdit("A SuperLauncher Server")

        self.ram_slider = QSlider(Qt.Orientation.Horizontal)
        self.ram_slider.setMinimum(1)
        self.ram_slider.setMaximum(16)
        self.ram_slider.setValue(self.ram_gb)
        self.ram_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.ram_slider.setTickInterval(1)
        self.ram_slider.valueChanged.connect(lambda v: setattr(self, 'ram_gb', v))

        form = QFormLayout()
        form.addRow(self.tr("EULA") + ":", self.checkbox_eula)
        form.addRow(self.tr("Offline mode") + ":", self.checkbox_offline)
        form.addRow(self.tr("Max players") + ":", self.spin_max_players)
        form.addRow(self.tr("MOTD") + ":", self.motd_edit)
        form.addRow(self.tr("RAM (GB):") + ":", self.ram_slider)
        form.addRow(self.tr("playit.gg") + ":", self.checkbox_playit)
        settings_layout.addLayout(form)

        self.btn_save_settings = QPushButton(self.tr("Save settings"))
        self.btn_save_settings.setStyleSheet("padding: 6px 16px; font-weight: bold; background-color: #4facfe; color: black; border-radius: 4px;")
        self.btn_save_settings.clicked.connect(self.save_settings)
        settings_layout.addWidget(self.btn_save_settings)
        settings_layout.addStretch()

        self.tabs.addTab(self.settings_tab, self.tr("Settings"))

        # -- Plugins tab --
        self.plugins_tab = QWidget()
        plugins_layout = QVBoxLayout(self.plugins_tab)

        search_row = QHBoxLayout()
        self.plugin_search_input = QLineEdit()
        self.plugin_search_input.setPlaceholderText(self.tr("Search plugins..."))
        self.btn_plugin_search = QPushButton(self.tr("Search"))
        self.btn_plugin_search.clicked.connect(self.search_plugins)
        search_row.addWidget(self.plugin_search_input)
        search_row.addWidget(self.btn_plugin_search)
        plugins_layout.addLayout(search_row)

        self.plugin_results = QListWidget()
        plugins_layout.addWidget(QLabel(self.tr("Search results:")))
        plugins_layout.addWidget(self.plugin_results)

        install_row = QHBoxLayout()
        self.btn_plugin_install = QPushButton(self.tr("Install"))
        self.btn_plugin_install.clicked.connect(self.install_selected_plugin)
        install_row.addWidget(self.btn_plugin_install)
        install_row.addStretch()
        plugins_layout.addLayout(install_row)

        plugins_layout.addWidget(QLabel(self.tr("Installed plugins:")))
        self.installed_plugins_list = QListWidget()
        plugins_layout.addWidget(self.installed_plugins_list)

        uninstall_row = QHBoxLayout()
        self.btn_plugin_uninstall = QPushButton(self.tr("Uninstall"))
        self.btn_plugin_uninstall.clicked.connect(self.uninstall_plugin)
        uninstall_row.addWidget(self.btn_plugin_uninstall)
        uninstall_row.addStretch()
        plugins_layout.addLayout(uninstall_row)

        self.tabs.addTab(self.plugins_tab, self.tr("Plugins"))
        self.refresh_installed_plugins()

        # -- Backup tab --
        self.backup_tab = QWidget()
        backup_layout = QVBoxLayout(self.backup_tab)

        self.btn_create_backup = QPushButton(self.tr("Create Backup"))
        self.btn_create_backup.setStyleSheet("padding: 8px; font-weight: bold; background-color: #ff9800; color: black; border-radius: 4px;")
        self.btn_create_backup.clicked.connect(self.create_backup)
        backup_layout.addWidget(self.btn_create_backup)

        backup_layout.addWidget(QLabel(self.tr("Backups:")))
        self.backup_list = QListWidget()
        backup_layout.addWidget(self.backup_list)

        self.btn_restore_backup = QPushButton(self.tr("Restore"))
        self.btn_restore_backup.clicked.connect(self.restore_backup)
        backup_layout.addWidget(self.btn_restore_backup)

        self.tabs.addTab(self.backup_tab, self.tr("Backup"))
        self.refresh_backups()

        self.server_thread.output_line.connect(self.on_server_output)
        self.server_thread.started.connect(self.on_server_started)
        self.server_thread.stopped.connect(self.on_server_stopped)
        self.server_thread.error.connect(self.on_server_error)

        self.load_settings()

    def tr(self, key: str) -> str:
        lang = self.config.get("language", "ru")
        return translations.get(lang, {}).get(key, key)

    def refresh_language(self):
        self.setWindowTitle(self.tr("Manage server") + f" '{self.server_name}'")
        self.tabs.setTabText(0, self.tr("Console"))
        self.tabs.setTabText(1, self.tr("Settings"))
        self.tabs.setTabText(2, self.tr("Plugins"))
        self.tabs.setTabText(3, self.tr("Backup"))
        self.btn_start.setText(self.tr("Start server"))
        self.btn_stop.setText(self.tr("Stop server"))
        self.cmd_input.setPlaceholderText(self.tr("Enter command..."))
        self.btn_send.setText(self.tr("Send"))
        self.checkbox_eula.setText(self.tr("I accept the EULA"))
        self.checkbox_offline.setText(self.tr("Enable offline mode (cracked)"))
        self.checkbox_playit.setText(self.tr("Use playit.gg (tunnel)"))
        self.btn_save_settings.setText(self.tr("Save settings"))
        self.plugin_search_input.setPlaceholderText(self.tr("Search plugins..."))
        self.btn_plugin_search.setText(self.tr("Search"))
        self.btn_plugin_install.setText(self.tr("Install"))
        self.btn_plugin_uninstall.setText(self.tr("Uninstall"))
        self.btn_create_backup.setText(self.tr("Create Backup"))
        self.btn_restore_backup.setText(self.tr("Restore"))

    def load_settings(self):
        eula_path = os.path.join(self.server_path, "eula.txt")
        eula_accepted = False
        if os.path.isfile(eula_path):
            with open(eula_path, "r", encoding="utf-8") as f:
                eula_accepted = "eula=true" in f.read().lower()
        self.checkbox_eula.setChecked(eula_accepted)

        prop_path = os.path.join(self.server_path, "server.properties")
        online_mode = True
        max_players = 20
        motd = "A SuperLauncher Server"
        if os.path.isfile(prop_path):
            with open(prop_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("online-mode="):
                        online_mode = line.strip().split("=")[1].lower() == "true"
                    elif line.startswith("max-players="):
                        try:
                            max_players = int(line.strip().split("=")[1])
                        except Exception:
                            pass
                    elif line.startswith("motd="):
                        motd = line.strip().split("=", 1)[1] if "=" in line else motd
        self.checkbox_offline.setChecked(not online_mode)
        self.spin_max_players.setValue(max_players)
        self.motd_edit.setText(motd)
        self.checkbox_playit.setChecked(False)

    def save_settings(self):
        eula_path = os.path.join(self.server_path, "eula.txt")
        try:
            with open(eula_path, "w", encoding="utf-8") as f:
                f.write(f"eula={'true' if self.checkbox_eula.isChecked() else 'false'}\n")
        except Exception as e:
            QMessageBox.critical(self, self.tr("Error"), self.tr("Failed to save eula.txt") + f":\n{e}")
            return

        prop_path = os.path.join(self.server_path, "server.properties")
        props = {}
        if os.path.isfile(prop_path):
            try:
                with open(prop_path, "r", encoding="utf-8") as f:
                    for line in f:
                        if "=" in line:
                            k, v = line.strip().split("=", 1)
                            props[k] = v
            except Exception:
                pass
        props["online-mode"] = "false" if self.checkbox_offline.isChecked() else "true"
        props["max-players"] = str(self.spin_max_players.value())
        props["motd"] = self.motd_edit.text()

        try:
            with open(prop_path, "w", encoding="utf-8") as f:
                for k, v in props.items():
                    f.write(f"{k}={v}\n")
        except Exception as e:
            QMessageBox.critical(self, self.tr("Error"), self.tr("Failed to save server.properties") + f":\n{e}")
            return

        self.ram_gb = self.ram_slider.value()
        QMessageBox.information(self, self.tr("Success"), self.tr("Settings saved!"))

    def start_server(self):
        if self.server_thread.isRunning():
            return
        if not self.checkbox_eula.isChecked():
            QMessageBox.warning(self, "EULA", self.tr("You must accept the EULA!"))
            return
        self.save_settings()
        self.console_output.clear()
        self.console_output.append(self.tr("Starting server..."))
        if self.checkbox_playit.isChecked():
            self.start_playit()
        self.server_thread.ram_gb = self.ram_gb
        self.server_thread.start_server()

    def stop_server(self):
        if not self.server_thread.isRunning():
            return
        self.console_output.append(self.tr("Stopping server..."))
        self.server_thread.stop_server()
        self.stop_playit()

    def send_console_command(self):
        cmd = self.cmd_input.text().strip()
        if cmd:
            self.server_thread.send_command(cmd)
            self.console_output.append(f"> {cmd}")
            self.cmd_input.clear()

    def on_server_output(self, line):
        self.console_output.append(line)
        scrollbar = self.console_output.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def on_server_started(self):
        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.console_output.append(self.tr("Server started."))

    def on_server_stopped(self):
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.console_output.append(self.tr("Server stopped."))

    def on_server_error(self, msg):
        self.console_output.append(f"[ERROR] {msg}")
        QMessageBox.critical(self, self.tr("Error"), msg)

    # --- playit.gg ---
    def download_and_install_playit(self):
        msi_url = "https://github.com/playit-cloud/playit-agent/releases/download/v0.15.26/playit-windows-x86_64-signed.msi"
        temp_dir = tempfile.gettempdir()
        msi_path = os.path.join(temp_dir, "playit-agent.msi")
        if not os.path.isfile(msi_path):
            try:
                response = requests.get(msi_url, stream=True)
                response.raise_for_status()
                with open(msi_path, "wb") as f:
                    for chunk in response.iter_content(8192):
                        if chunk:
                            f.write(chunk)
                os.system(f'powershell -Command "Unblock-File -Path \'{msi_path}\'"')
            except Exception as e:
                QMessageBox.critical(self, self.tr("Error"), self.tr("Failed to download playit MSI") + f":\n{e}")
                return False
        try:
            result = subprocess.run(["msiexec", "/i", msi_path, "/quiet", "/qn"], capture_output=True, text=True, shell=False)
            if result.returncode != 0:
                QMessageBox.critical(self, self.tr("Error"), self.tr("Installation failed"))
                return False
            return True
        except Exception as e:
            QMessageBox.critical(self, self.tr("Error"), self.tr("Failed to install playit") + f":\n{e}")
            return False

    def start_playit(self):
        possible_paths = [
            os.path.expandvars(r"%ProgramFiles%\playit\playit.exe"),
            os.path.expandvars(r"%ProgramFiles(x86)%\playit\playit.exe"),
            os.path.join(self.server_path, "playit.exe"),
        ]
        playit_exe = next((p for p in possible_paths if os.path.isfile(p)), None)
        if not playit_exe:
            if not self.download_and_install_playit():
                return False
            playit_exe = next((p for p in possible_paths if os.path.isfile(p)), None)
            if not playit_exe:
                return False
        try:
            self.playit_process = subprocess.Popen([playit_exe], cwd=os.path.dirname(playit_exe))
            return True
        except Exception:
            return False

    def stop_playit(self):
        if self.playit_process and self.playit_process.poll() is None:
            try:
                self.playit_process.terminate()
                self.playit_process.wait(5)
            except Exception:
                self.playit_process.kill()
            finally:
                self.playit_process = None

    # --- Plugins ---
    def search_plugins(self):
        query = self.plugin_search_input.text().strip()
        if not query:
            return
        self.plugin_results.clear()
        from threading import Thread

        category_map = {"paper": "paper", "purpur": "purpur", "vanilla": "bukkit", "fabric": "fabric", "quilt": "quilt"}
        cat = category_map.get(self.server_core.lower(), "bukkit")

        def task():
            try:
                # Modrinth AND facets with project_type:mod + categories:bukkit returns 0 results,
                # so only use project_type filter for fabric/quilt where it works.
                if cat in ("fabric", "quilt"):
                    facets = f'[["project_type:mod"],["categories:{cat}"]]'
                else:
                    facets = f'[["categories:{cat}"]]'
                url = f"{MODRINTH_API}/search?query={urllib.parse.quote(query)}&facets={urllib.parse.quote(facets)}&limit=30"
                resp = requests.get(url, headers={"User-Agent": "SuperLauncher/2.0"}, timeout=10)
                resp.raise_for_status()
                data = resp.json()
                hits = data.get("hits", [])
                if not hits:
                    self.plugin_results.addItem(self.tr("No plugins found"))
                    return
                for hit in hits:
                    title = hit.get("title", "?")
                    slug = hit.get("slug", "")
                    downloads = hit.get("downloads", 0)
                    summary = hit.get("description", "")
                    if len(summary) > 80:
                        summary = summary[:77] + "..."
                    item_text = f"{title} ({slug}) - {downloads} downloads"
                    item = QListWidgetItem(item_text)
                    item.setData(Qt.ItemDataRole.UserRole, slug)
                    self.plugin_results.addItem(item)
            except Exception as e:
                self.plugin_results.addItem(self.tr("Error") + f": {e}")

        Thread(target=task, daemon=True).start()

    def install_selected_plugin(self):
        item = self.plugin_results.currentItem()
        if not item:
            return
        slug = item.data(Qt.ItemDataRole.UserRole)
        if not slug:
            return

        plugins_folder = os.path.join(self.server_path, "plugins")
        os.makedirs(plugins_folder, exist_ok=True)

        loader_map = {"paper": "bukkit", "purpur": "bukkit", "vanilla": "bukkit", "fabric": "fabric", "quilt": "quilt"}
        loader = loader_map.get(self.server_core.lower(), "bukkit")
        version = self.server_version if self.server_version else ""

        self.plugin_install_thread = PluginInstallThread(slug, version, loader, plugins_folder)
        self.plugin_install_thread.finished.connect(lambda p: QMessageBox.information(
            self, self.tr("Install plugin"), self.tr("Plugin installed") + f": {os.path.basename(p)}"))
        self.plugin_install_thread.finished.connect(lambda p: self.refresh_installed_plugins())
        self.plugin_install_thread.error.connect(lambda e: QMessageBox.critical(
            self, self.tr("Error"), self.tr("Downloading plugin...") + f"\n{e}"))
        self.plugin_install_thread.start()

    def refresh_installed_plugins(self):
        self.installed_plugins_list.clear()
        plugins_folder = os.path.join(self.server_path, "plugins")
        if os.path.isdir(plugins_folder):
            for f in sorted(os.listdir(plugins_folder)):
                if f.endswith(".jar"):
                    self.installed_plugins_list.addItem(f)

    def uninstall_plugin(self):
        item = self.installed_plugins_list.currentItem()
        if not item:
            return
        filename = item.text()
        reply = QMessageBox.question(self, self.tr("Uninstall"),
                                     f"{self.tr('Are you sure?')}\n{filename}",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply != QMessageBox.StandardButton.Yes:
            return
        filepath = os.path.join(self.server_path, "plugins", filename)
        try:
            os.remove(filepath)
            self.refresh_installed_plugins()
        except Exception as e:
            QMessageBox.critical(self, self.tr("Error"), str(e))

    # --- Backups ---
    def create_backup(self):
        backup_dir = os.path.join(self.server_path, "backups")
        os.makedirs(backup_dir, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(backup_dir, f"backup_{timestamp}.zip")

        try:
            with zipfile.ZipFile(backup_path, "w", zipfile.ZIP_DEFLATED) as zf:
                for folder_name in ["world", "world_nether", "world_the_end", "plugins", ""]:
                    folder_path = os.path.join(self.server_path, folder_name)
                    if not os.path.isdir(folder_path):
                        continue
                    for root, dirs, files in os.walk(folder_path):
                        if "backups" in root.split(os.sep):
                            continue
                        for fname in files:
                            fpath = os.path.join(root, fname)
                            arcname = os.path.relpath(fpath, self.server_path)
                            zf.write(fpath, arcname)
            QMessageBox.information(self, self.tr("Backup"), self.tr("Backup created") + f":\n{backup_path}")
            self.refresh_backups()
        except Exception as e:
            QMessageBox.critical(self, self.tr("Error"), str(e))

    def refresh_backups(self):
        self.backup_list.clear()
        backup_dir = os.path.join(self.server_path, "backups")
        if os.path.isdir(backup_dir):
            for f in sorted(os.listdir(backup_dir), reverse=True):
                if f.endswith(".zip"):
                    self.backup_list.addItem(f)

    def restore_backup(self):
        item = self.backup_list.currentItem()
        if not item:
            return
        filename = item.text()
        reply = QMessageBox.question(self, self.tr("Restore backup"),
                                     f"{self.tr('Are you sure?')}\n{filename}",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply != QMessageBox.StandardButton.Yes:
            return
        backup_path = os.path.join(self.server_path, "backups", filename)
        try:
            with zipfile.ZipFile(backup_path, "r") as zf:
                zf.extractall(self.server_path)
            QMessageBox.information(self, self.tr("Restore backup"), self.tr("Backup restored"))
            self.refresh_installed_plugins()
        except Exception as e:
            QMessageBox.critical(self, self.tr("Error"), str(e))


class ServersPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.config = load_config()

        self.servers_file = "servers_list.json"
        self.servers_list = []

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.layout.setSpacing(10)

        self.title_label = QLabel(self.tr("🖧 Minecraft Servers"))
        self.title_label.setStyleSheet(
            "font-size: 26px; font-weight: bold; margin-bottom: 15px; color: white;"
        )
        self.layout.addWidget(self.title_label)

        self.btn_create_server = QPushButton(self.tr("Create your own server"))
        self.btn_create_server.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_create_server.setStyleSheet(
            "padding: 8px; font-weight: bold; background-color: #4facfe; color: black; border-radius: 8px;"
        )
        self.btn_create_server.clicked.connect(self.open_create_server_dialog)
        self.layout.addWidget(self.btn_create_server)

        form_layout = QHBoxLayout()
        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText(self.tr("Server Name"))
        self.input_ip = QLineEdit()
        self.input_ip.setPlaceholderText(self.tr("IP or domain"))

        self.btn_add_server = QPushButton(self.tr("Add server"))
        self.btn_add_server.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_add_server.setStyleSheet(
            "padding: 6px 12px; font-weight: bold; background-color: #4CAF50; color: white; border-radius: 5px;"
        )
        self.btn_add_server.clicked.connect(self.add_server)

        form_layout.addWidget(self.input_name)
        form_layout.addWidget(self.input_ip)
        form_layout.addWidget(self.btn_add_server)
        self.layout.addLayout(form_layout)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.hide()
        self.layout.addWidget(self.progress_bar)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        self.layout.addWidget(self.scroll_area)

        self.container = QWidget()
        self.container.setStyleSheet("background: transparent;")
        self.scroll_area.setWidget(self.container)
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(0, 0, 0, 0)
        self.container_layout.setSpacing(8)

        self.load_servers()
        self.update_servers_ui()

    def tr(self, key: str) -> str:
        if self.parent_window and hasattr(self.parent_window, "tr"):
            return self.parent_window.tr(key)
        lang = self.config.get("language", "ru")
        return translations.get(lang, {}).get(key, key)

    def refresh_language(self):
        self.title_label.setText(self.tr("🖧 Minecraft Servers"))
        self.btn_create_server.setText(self.tr("Create your own server"))
        self.input_name.setPlaceholderText(self.tr("Server Name"))
        self.input_ip.setPlaceholderText(self.tr("IP or domain"))
        self.btn_add_server.setText(self.tr("Add server"))
        self.update_servers_ui()

    def open_create_server_dialog(self):
        dialog = CreateServerDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            name = dialog.server_name
            port = dialog.server_port
            version = dialog.server_version
            core = dialog.server_core
            ram_gb = dialog.ram_gb
            ip = f"localhost:{port}"

            server_path = os.path.join("servers", name)
            os.makedirs(server_path, exist_ok=True)

            self.progress_bar.setValue(0)
            self.progress_bar.show()

            self.download_thread = DownloadThread(core, version, os.path.join(server_path, "server.jar"))
            self.download_thread.progress_changed.connect(self.progress_bar.setValue)
            self.download_thread.finished.connect(lambda: self.on_download_finished(name, ip, server_path, ram_gb, version, core))
            self.download_thread.error.connect(self.on_download_error)
            self.download_thread.start()

    def on_download_finished(self, name, ip, server_path, ram_gb=4, version='', core=''):
        self.progress_bar.hide()
        self.generate_start_bat(server_path, ram_gb)

        self.servers_list.append({"name": name, "ip": ip, "managed": True, "ram_gb": ram_gb, "version": version, "core": core})
        self.save_servers()
        self.update_servers_ui()

        QMessageBox.information(
            self,
            self.tr("Done"),
            f"{self.tr('Server')} '{name}' {self.tr('successfully created!')}"
        )

    def on_download_error(self, error_message):
        self.progress_bar.hide()
        QMessageBox.critical(self, self.tr("Error"), error_message)

    def generate_start_bat(self, path, ram_gb=4):
        with open(os.path.join(path, "start.bat"), "w", encoding="utf-8") as f:
            f.write(f"""@echo off
java -Xmx{ram_gb}G -Xms{ram_gb}G -jar server.jar nogui
""")

    def load_servers(self):
        try:
            with open(self.servers_file, "r", encoding="utf-8") as f:
                self.servers_list = json.load(f)
        except Exception:
            self.servers_list = []

    def save_servers(self):
        try:
            with open(self.servers_file, "w", encoding="utf-8") as f:
                json.dump(self.servers_list, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print("Error saving servers:", e)

    def add_server(self):
        name = self.input_name.text().strip()
        ip = self.input_ip.text().strip()

        if not name or not ip:
            QMessageBox.warning(
                self,
                self.tr("Error"),
                self.tr("Please fill in the server name and IP.")
            )
            return

        self.servers_list.append({"name": name, "ip": ip, "managed": False})
        self.save_servers()
        self.update_servers_ui()

        self.input_name.clear()
        self.input_ip.clear()

    def update_servers_ui(self):
        while self.container_layout.count():
            item = self.container_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        for server in self.servers_list:
            self.add_server_widget(server['name'], server['ip'], server.get('managed', False), server.get('ram_gb', 4), server.get('version', ''), server.get('core', ''))

        self.container_layout.addStretch()

    def add_server_widget(self, name, ip, managed, ram_gb=4, version='', core=''):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: rgba(40, 40, 55, 0.9);
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 10px;
                padding: 8px;
            }
        """)
        card_layout = QHBoxLayout(card)
        card_layout.setContentsMargins(12, 8, 12, 8)
        card_layout.setSpacing(10)

        icon_label = QLabel("🖧")
        icon_label.setStyleSheet("font-size: 24px;")
        card_layout.addWidget(icon_label)

        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(2)

        name_label = QLabel(f"<b>{name}</b>")
        name_label.setStyleSheet("font-size: 16px; color: white;")
        info_layout.addWidget(name_label)

        ip_label = QLabel(f"<span style='color:#4facfe;'>{ip}</span>")
        ip_label.setStyleSheet("font-size: 13px;")
        info_layout.addWidget(ip_label)

        badge_text = self.tr("Managed") if managed else self.tr("Manual")
        badge_color = "#4caf50" if managed else "#ff9800"
        badge = QLabel(f"<span style='background:{badge_color}; color:white; padding:2px 8px; border-radius:3px; font-size:11px;'>{badge_text}</span>")
        badge.setStyleSheet("font-size: 11px;")
        info_layout.addWidget(badge)

        card_layout.addWidget(info_widget)
        card_layout.addStretch()

        btn_style = "padding: 5px 12px; font-weight: bold; border-radius: 5px; font-size: 12px;"

        if managed:
            btn_console = QPushButton(self.tr("Console"))
            btn_console.setStyleSheet(f"{btn_style} background-color: #4facfe; color: black;")
            btn_console.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            server_path = os.path.join("servers", name)
            btn_console.clicked.connect(lambda checked, n=name, p=server_path, r=ram_gb, v=version, c=core: self.open_console(n, p, r, v, c))
            card_layout.addWidget(btn_console)

            btn_open = QPushButton(self.tr("Open folder"))
            btn_open.setStyleSheet(f"{btn_style} background-color: #607d8b; color: white;")
            btn_open.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            btn_open.clicked.connect(lambda checked, p=server_path: os.startfile(p) if hasattr(os, 'startfile') else None)
            card_layout.addWidget(btn_open)

        btn_delete = QPushButton(self.tr("Delete"))
        btn_delete.setStyleSheet(f"{btn_style} background-color: #f44336; color: white;")
        btn_delete.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_delete.clicked.connect(lambda checked, n=name, m=managed: self.delete_server(n, m))
        card_layout.addWidget(btn_delete)

        btn_ping = QPushButton("📡 Ping")
        btn_ping.setStyleSheet(f"{btn_style} background-color: #5bc0de; color: black;")
        btn_ping.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_ping.clicked.connect(lambda checked, h=ip: self._ping_server(h))
        card_layout.addWidget(btn_ping)

        self.container_layout.addWidget(card)

    def open_console(self, server_name, server_path, ram_gb=4, version='', core=''):
        dialog = ServerControlDialog(server_name, server_path, ram_gb, version, core, self)
        dialog.exec()

    def delete_server(self, server_name, managed):
        reply = QMessageBox.question(
            self,
            self.tr("Confirm deletion"),
            f"{self.tr('Are you sure you want to delete the server')} '{server_name}'? {self.tr('This action cannot be undone.')}",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.servers_list = [s for s in self.servers_list if s['name'] != server_name]
            self.save_servers()
            self.update_servers_ui()

            if managed:
                server_path = os.path.join("servers", server_name)
                if os.path.exists(server_path) and os.path.isdir(server_path):
                    try:
                        shutil.rmtree(server_path)
                    except Exception as e:
                        QMessageBox.critical(self, self.tr("Error"), f"{self.tr('Failed to delete folder')}:\n{e}")

    def _ping_server(self, hostname):
        if ":" in hostname:
            hostname = hostname.split(":")[0]
        try:
            if sys.platform == "win32":
                result = subprocess.run(["ping", "-n", "1", hostname], capture_output=True, text=True, timeout=10)
            else:
                result = subprocess.run(["ping", "-c", "1", hostname], capture_output=True, text=True, timeout=10)
            output = result.stdout + result.stderr
            output = output[-2000:]
            QMessageBox.information(self, f"📡 Ping {hostname}", output)
        except subprocess.TimeoutExpired:
            QMessageBox.warning(self, "Ping", "Таймаут ожидания ответа")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка ping: {e}")

# =========== ЗАМЕНИТЬ ВЕСЬ КЛАСС MainWindow НА ЭТОТ ===========
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SuperLauncher 2026 Edition v2.0.0")
        self.setWindowIcon(QIcon("assets/icon.png"))

        self.resize(1080, 720)
        self.setMinimumSize(800, 600)
        self.setMaximumSize(1920, 1080)

        self.account_system = AccountSystem()
        self.skins_manager = SkinsManager(self.account_system)
        self.builds_manager = BuildsManager()
        self.custom_ui = CustomizableUI()
        self.platform_info = CrossPlatformSupport.get_platform_info()

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")

        # Main container
        main_container = QFrame()
        main_container.setObjectName("MainContainer")
        main_container.setStyleSheet("""
            QFrame#MainContainer {
                background: #121218;
                border: 1px solid rgba(255,255,255,0.04);
                border-radius: 0;
            }
        """)
        
        # VERTICAL: top_bar + content_row
        main_vbox = QVBoxLayout(main_container)
        main_vbox.setContentsMargins(0, 0, 0, 0)
        main_vbox.setSpacing(0)
        
        # ===== TOP BAR =====
        top_bar = QFrame()
        top_bar.setObjectName("TopBar")
        top_bar.setFixedHeight(52)
        top_bar.setStyleSheet("""
            QFrame#TopBar {
                background: #0e0e16;
                border-bottom: 1px solid rgba(255,255,255,0.04);
            }
        """)
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(16, 0, 16, 0)
        top_layout.setSpacing(12)
        
        # Logo area
        logo = QLabel("⚡")
        logo.setStyleSheet("font-size: 18px; background: transparent;")
        top_layout.addWidget(logo)
        
        app_name = QLabel("SuperLauncher")
        app_name.setStyleSheet("font-size: 14px; font-weight: 700; color: rgba(255,255,255,0.8); background: transparent;")
        top_layout.addWidget(app_name)
        
        top_layout.addSpacing(16)
        
        # Page title (changes with page)
        self.page_title = QLabel("Главная")
        self.page_title.setStyleSheet("font-size: 13px; font-weight: 500; color: rgba(255,255,255,0.35); background: transparent;")
        top_layout.addWidget(self.page_title)
        
        top_layout.addStretch()
        
        # Search bar
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍  Search...")
        self.search_input.setFixedWidth(200)
        self.search_input.setFixedHeight(32)
        self.search_input.setStyleSheet("""
            QLineEdit {
                background: rgba(255,255,255,0.04);
                border: 1px solid rgba(255,255,255,0.04);
                border-radius: 6px;
                padding: 4px 10px;
                color: rgba(255,255,255,0.6);
                font-size: 12px;
            }
            QLineEdit:focus {
                border-color: rgba(168,85,247,0.2);
                background: rgba(168,85,247,0.04);
            }
        """)
        top_layout.addWidget(self.search_input)
        
        # Account button in top bar
        self.top_account_btn = QPushButton("👤")
        self.top_account_btn.setFixedSize(32, 32)
        self.top_account_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.top_account_btn.setStyleSheet("""
            QPushButton {
                background: rgba(168,85,247,0.06);
                border: 1px solid rgba(168,85,247,0.08);
                border-radius: 16px;
                font-size: 14px;
                padding: 0;
            }
            QPushButton:hover {
                background: rgba(168,85,247,0.12);
                border-color: rgba(168,85,247,0.15);
            }
        """)
        self.top_account_btn.clicked.connect(self.show_login_dialog)
        top_layout.addWidget(self.top_account_btn)
        
        main_vbox.addWidget(top_bar)
        
        # ===== CONTENT ROW: sidebar + pages =====
        content_row = QHBoxLayout()
        content_row.setContentsMargins(0, 0, 0, 0)
        content_row.setSpacing(0)
        
        self.sidebar = ModernSidebar(self)
        
        self.pages = QStackedWidget()
        self.pages.setStyleSheet("""
            QStackedWidget {
                background: #121218;
                border: none;
            }
        """)
        
        self.create_all_pages()
        self.check_pages_consistency()
        
        content_row.addWidget(self.sidebar)
        content_row.addWidget(self.pages, 1)
        
        main_vbox.addLayout(content_row, 1)
        
        outer = QHBoxLayout()
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(main_container)
        
        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(outer)

        self.launch_thread = LaunchThread()
        self.launch_thread.state_update_signal.connect(self.state_update)
        self.launch_thread.progress_update_signal.connect(self.update_progress)
        self.launch_thread.error_signal.connect(self.show_launch_error)

        self.pages.currentChanged.connect(self._on_page_changed)

        self.discord_rpc_thread = DiscordRPCThread(self)
        self.discord_rpc_thread.start()

        self.setup_status_bar()

        self.launch_start_time = None
        self.session_timer = QTimer()
        self.session_timer.timeout.connect(self._update_session_label)
        self.session_timer.setInterval(5000)

        self.check_auto_login()

        self.custom_ui.apply_to_widget(self)
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
    
    def create_all_pages(self):
        pages_list = []

        # 0 - Главная
        pages_list.append(self.create_home_page())

        # 1 - Аккаунт
        pages_list.append(self.create_account_page())

        # 2 - Моды
        pages_list.append(ModsPage(self))

        # 3 - Инстансы
        pages_list.append(InstancesPage(self))

        # 4 - Скины
        pages_list.append(self.create_skins_page())

        # 5 - Новости
        pages_list.append(NewsPage(self))

        # 6 - Обновления
        pages_list.append(UpdatesPage())

        # 7 - Серверы
        pages_list.append(ServersPage(self))

        # 8 - Настройки
        self.settings_page = SettingsPage(self)
        pages_list.append(self.settings_page)

        # 9 - Minecraft
        minecraft_page = MinecraftLauncherPage(self)
        if hasattr(minecraft_page, 'start_button'):
            old_button = minecraft_page.start_button
            new_button = AnimatedButton("🎮 Играть")
            new_button.setFixedHeight(50)
            new_button.setStyleSheet("font-size: 18px; font-weight: bold;")
            new_button.clicked.connect(self.launch_game)

            layout = minecraft_page.layout()
            for i in range(layout.count()):
                item = layout.itemAt(i)
                if item.widget() == old_button:
                    layout.removeWidget(old_button)
                    old_button.deleteLater()
                    layout.insertWidget(i, new_button)
                    minecraft_page.start_button = new_button
                    break
        pages_list.append(minecraft_page)

        # 10 - Управление контентом
        pages_list.append(ContentManagerPage(self))

        # 11 - AI Агент
        self.ai_page = AIAgentPage(self)
        pages_list.append(self.ai_page)

        for page in pages_list:
            self.pages.addWidget(page)

        print(f"✅ Создано {len(pages_list)} страниц")
    
    def _on_page_changed(self, index):
        if hasattr(self, 'discord_rpc_thread'):
            self.discord_rpc_thread.update_page(index)

    def check_pages_consistency(self):
        """Проверка соответствия кнопок и страниц"""
        button_count = len(self.sidebar.nav_buttons)
        page_count = self.pages.count()
        
        if button_count != page_count:
            print(f"⚠️ Несоответствие: {button_count} кнопок, {page_count} страниц")
            # Автоматическая корректировка
            if button_count < page_count:
                print(f"Добавляем {page_count - button_count} кнопок...")
            elif button_count > page_count:
                print(f"Удаляем {button_count - page_count} лишних кнопок...")
            return False
        
        print(f"✅ Все в порядке: {button_count} кнопок, {page_count} страниц")
        return True
    

    def _create_recent_instances_widget(self):
        instances = load_instances()
        if not instances:
            return None
        widget = QWidget()
        widget.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        title = QLabel("Recent Instances")
        title.setStyleSheet("""
            font-size: 12px; font-weight: 600; color: rgba(255,255,255,0.4);
            background: transparent; padding-bottom: 2px;
        """)
        layout.addWidget(title)
        
        cards = QHBoxLayout()
        cards.setSpacing(6)
        for inst in instances[:4]:
            card = QPushButton()
            card.setFixedSize(130, 68)
            card.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            card.setStyleSheet("""
                QPushButton {
                    font-size: 10px; padding: 6px; border-radius: 7px;
                    background: #1a1a24;
                    color: white;
                    border: 1px solid rgba(255,255,255,0.04);
                    text-align: left;
                }
                QPushButton:hover {
                    background: #1e1e2a;
                    border-color: rgba(168,85,247,0.08);
                }
            """)
            card.setText(f"<b>{inst.get('icon', '📦')} {inst['name']}</b><br><span style='color:rgba(255,255,255,0.25);font-size:9px;'>{inst['mc_version']} · {inst['loader']}</span>")
            card.clicked.connect(lambda checked, i=inst: self._launch_instance(i))
            cards.addWidget(card)
        layout.addLayout(cards)
        return widget

    def create_home_page(self):
        page = QWidget()
        page.setStyleSheet("background: transparent;")
        outer = QVBoxLayout(page)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        
        # Scrollable content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { background: transparent; border: none; }")
        
        content = QWidget()
        content.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(content)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)

        # ===== HERO SECTION =====
        hero = QFrame()
        hero.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(168,85,247,0.06), stop:1 rgba(168,85,247,0.02));
                border: 1px solid rgba(168,85,247,0.06);
                border-radius: 12px;
            }
        """)
        hero.setFixedHeight(160)
        hero_layout = QHBoxLayout(hero)
        hero_layout.setContentsMargins(28, 0, 28, 0)
        
        hero_text = QVBoxLayout()
        hero_text.setSpacing(6)
        hero_title = QLabel("SuperLauncher")
        hero_title.setStyleSheet("font-size: 28px; font-weight: 700; color: white; background: transparent;")
        hero_text.addWidget(hero_title)
        hero_sub = QLabel("Next Generation Minecraft Launcher")
        hero_sub.setStyleSheet("font-size: 13px; color: rgba(255,255,255,0.3); background: transparent;")
        hero_text.addWidget(hero_sub)
        
        # Quick launch button
        launch_btn = QPushButton("▶  Launch Minecraft")
        launch_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        launch_btn.setStyleSheet("""
            QPushButton {
                background: rgba(168,85,247,0.15);
                color: white; border: 1px solid rgba(168,85,247,0.15);
                border-radius: 8px; padding: 10px 24px;
                font-weight: 600; font-size: 13px;
            }
            QPushButton:hover {
                background: rgba(168,85,247,0.25);
                border-color: rgba(168,85,247,0.25);
            }
        """)
        launch_btn.clicked.connect(self.launch_game)
        hero_text.addWidget(launch_btn)
        
        hero_layout.addLayout(hero_text)
        hero_layout.addStretch()
        
        # Stats on hero
        stats_w = QWidget()
        stats_w.setStyleSheet("background: transparent;")
        stats_l = QVBoxLayout(stats_w)
        stats_l.setSpacing(8)
        stats_l.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        instances = load_instances()
        stat_inst = QLabel(f"<span style='font-size:24px;font-weight:700;color:white;'>{len(instances)}</span><br><span style='font-size:11px;color:rgba(255,255,255,0.3);'>Instances</span>")
        stat_inst.setStyleSheet("background: transparent;")
        stat_inst.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stats_l.addWidget(stat_inst)
        
        hero_layout.addWidget(stats_w)
        layout.addWidget(hero)

        # ===== USER SECTION =====
        user_card = QFrame()
        user_card.setStyleSheet("""
            QFrame {
                background: #1a1a24;
                border: 1px solid rgba(255,255,255,0.04);
                border-radius: 8px;
            }
        """)
        u_layout = QHBoxLayout(user_card)
        u_layout.setContentsMargins(14, 10, 14, 10)
        u_layout.setSpacing(10)
        
        avatar = QLabel("👤")
        avatar.setStyleSheet("""
            font-size: 20px; padding: 6px;
            background: #22222e;
            border: 1px solid rgba(168,85,247,0.06);
            border-radius: 50%;
            min-width: 34px; min-height: 34px;
        """)
        u_layout.addWidget(avatar)
        
        u_info = QVBoxLayout()
        u_info.setSpacing(1)
        self.username_label = QLabel("Гость")
        self.username_label.setStyleSheet("font-size: 14px; font-weight: 600; color: white;")
        u_info.addWidget(self.username_label)
        self.user_status_label = QLabel("Не авторизован")
        self.user_status_label.setStyleSheet("font-size: 11px; color: rgba(255,255,255,0.2);")
        u_info.addWidget(self.user_status_label)
        u_layout.addLayout(u_info)
        u_layout.addStretch()
        
        self.login_button = QPushButton("Войти")
        self.login_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.login_button.setStyleSheet("""
            QPushButton {
                background: rgba(168,85,247,0.08);
                color: rgba(255,255,255,0.7);
                border: 1px solid rgba(168,85,247,0.08);
                border-radius: 6px; padding: 6px 14px;
                font-weight: 500; font-size: 12px;
            }
            QPushButton:hover {
                background: rgba(168,85,247,0.15);
                border-color: rgba(168,85,247,0.15);
                color: white;
            }
        """)
        self.login_button.clicked.connect(self.show_login_dialog)
        u_layout.addWidget(self.login_button)
        
        layout.addWidget(user_card)

        # ===== INSTANCES GRID =====
        instances = load_instances()
        if instances:
            grid_card = QFrame()
            grid_card.setStyleSheet("""
                QFrame {
                    background: #1a1a24;
                    border: 1px solid rgba(255,255,255,0.04);
                    border-radius: 8px;
                }
            """)
            grid_layout = QVBoxLayout(grid_card)
            grid_layout.setContentsMargins(14, 12, 14, 12)
            grid_layout.setSpacing(10)
            
            grid_title = QLabel("Instances")
            grid_title.setStyleSheet("font-size: 13px; font-weight: 600; color: rgba(255,255,255,0.5); background: transparent;")
            grid_layout.addWidget(grid_title)
            
            # Horizontal scrollable card row
            scroll_row = QScrollArea()
            scroll_row.setWidgetResizable(False)
            scroll_row.setFixedHeight(200)
            scroll_row.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            scroll_row.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            scroll_row.setStyleSheet("QScrollArea { background: transparent; border: none; }")
            
            cards_w = QWidget()
            cards_w.setStyleSheet("background: transparent;")
            cards_row = QHBoxLayout(cards_w)
            cards_row.setContentsMargins(0, 0, 0, 0)
            cards_row.setSpacing(8)
            
            for inst in instances[:8]:
                card = self._create_mini_instance_card(inst)
                cards_row.addWidget(card)
            
            cards_row.addStretch()
            scroll_row.setWidget(cards_w)
            grid_layout.addWidget(scroll_row)
            
            layout.addWidget(grid_card)

        # ===== QUICK ACTIONS =====
        actions_card = QFrame()
        actions_card.setStyleSheet("""
            QFrame {
                background: #1a1a24;
                border: 1px solid rgba(255,255,255,0.04);
                border-radius: 8px;
            }
        """)
        a_layout = QVBoxLayout(actions_card)
        a_layout.setContentsMargins(14, 10, 14, 10)
        a_layout.setSpacing(8)
        
        a_title = QLabel("Quick Access")
        a_title.setStyleSheet("font-size: 13px; font-weight: 600; color: rgba(255,255,255,0.5); background: transparent;")
        a_layout.addWidget(a_title)
        
        a_grid = QHBoxLayout()
        a_grid.setSpacing(6)
        
        quick_items = [
            ("🧩", "Mods", lambda: self.pages.setCurrentIndex(2)),
            ("🖼️", "Skins", lambda: self.pages.setCurrentIndex(4)),
            ("⚙️", "Settings", lambda: self.pages.setCurrentIndex(8)),
            ("📁", "Content", lambda: self.pages.setCurrentIndex(10)),
        ]
        for icon, text, cb in quick_items:
            btn = QPushButton(f"{icon}  {text}")
            btn.setFixedHeight(44)
            btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 12px; font-weight: 500;
                    border-radius: 6px;
                    background: rgba(255,255,255,0.02);
                    color: rgba(255,255,255,0.55);
                    border: 1px solid rgba(255,255,255,0.04);
                }
                QPushButton:hover {
                    background: rgba(168,85,247,0.05);
                    border-color: rgba(168,85,247,0.1);
                    color: white;
                }
            """)
            btn.clicked.connect(cb)
            a_grid.addWidget(btn)
        a_layout.addLayout(a_grid)
        layout.addWidget(actions_card)

        layout.addStretch()
        
        scroll.setWidget(content)
        outer.addWidget(scroll)
        return page

    def _create_mini_instance_card(self, inst):
        card = QPushButton()
        card.setFixedSize(150, 150)
        card.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        card.setStyleSheet("""
            QPushButton {
                background: #1e1e2a;
                border: 1px solid rgba(255,255,255,0.04);
                border-radius: 8px;
                text-align: center;
                padding: 10px;
            }
            QPushButton:hover {
                background: #22222e;
                border-color: rgba(168,85,247,0.08);
            }
        """)
        icon = inst.get("icon", "📦")
        name = inst["name"]
        version = inst.get('mc_version', '?')
        loader = inst.get('loader', 'vanilla')
        card.setText(f"<div style='font-size:28px;margin-bottom:6px;'>{icon}</div><b style='font-size:12px;color:white;'>{name}</b><br><span style='font-size:10px;color:rgba(255,255,255,0.3);'>{version} · {loader}</span>")
        card.clicked.connect(lambda checked, i=inst: self._launch_instance(i))
        return card

    # В классе MainWindow (примерно строка 4012) ЗАМЕНИТЕ:

    def create_user_info_widget_720p(self):
        widget = QFrame()
        widget.setStyleSheet("""
            QFrame {
                background: rgba(255,255,255,0.03);
                border: 1px solid rgba(102,126,234,0.1);
                border-radius: 16px;
            }
        """)

        layout = QHBoxLayout(widget)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(14)

        self.avatar_label = QLabel("👤")
        self.avatar_label.setStyleSheet("""
            font-size: 32px; padding: 8px;
            background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                stop:0 rgba(102,126,234,0.2), stop:1 rgba(118,75,162,0.1));
            border: 1px solid rgba(102,126,234,0.2);
            border-radius: 50%;
            min-width: 52px; min-height: 52px; 
            text-align: center;
        """)
        layout.addWidget(self.avatar_label)

        user_info_widget = QWidget()
        user_info_layout = QVBoxLayout(user_info_widget)
        user_info_layout.setContentsMargins(0, 0, 0, 0)
        user_info_layout.setSpacing(4)

        self.username_label = QLabel("Гость")
        self.username_label.setStyleSheet("font-size: 18px; font-weight: 700; color: white;")
        user_info_layout.addWidget(self.username_label)

        self.user_status_label = QLabel("Не авторизован")
        self.user_status_label.setStyleSheet("font-size: 12px; color: rgba(255,255,255,0.4);")
        user_info_layout.addWidget(self.user_status_label)

        layout.addWidget(user_info_widget)
        layout.addStretch()

        self.login_button = QPushButton("Войти")
        self.login_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.login_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white; border: none;
                border-radius: 10px; padding: 8px 20px;
                font-weight: 600; font-size: 13px;
                letter-spacing: 0.5px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #7b92f0, stop:1 #8b5cbf);
            }
        """)
        self.login_button.clicked.connect(self.show_login_dialog)
        layout.addWidget(self.login_button)

        return widget

    def create_quick_actions_720p(self):
        """Быстрые действия для 720p"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        title = QLabel("🚀 Быстрые действия")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: white; margin-bottom: 8px;")
        layout.addWidget(title)
        
        grid_widget = QWidget()
        grid_layout = QGridLayout(grid_widget)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.setSpacing(8)
        
        actions = [
            ("🎮", "Запуск", self.launch_game),
            ("🛒", "Скины", lambda: self.pages.setCurrentIndex(4)),
            ("📦", "Сборки", lambda: self.pages.setCurrentIndex(3)),
            ("⚙️", "Настройки", lambda: self.pages.setCurrentIndex(8)),
            ("🆘", "Помощь", self.show_help),
        ]
        
        row, col = 0, 0
        for icon, text, callback in actions:
            btn = QPushButton(f"{icon}  {text}")
            btn.setFixedSize(130, 70)
            btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 13px; font-weight: 600;
                    padding: 6px;
                    border-radius: 10px;
                    background: rgba(102,126,234,0.08);
                    color: white;
                    border: 1px solid rgba(102,126,234,0.12);
                    text-align: center;
                }
                QPushButton:hover {
                    background: rgba(102,126,234,0.18);
                    border: 1px solid rgba(102,126,234,0.3);
                }
            """)
            btn.clicked.connect(callback)
            grid_layout.addWidget(btn, row, col)
            
            col += 1
            if col > 2:
                col = 0
                row += 1
        
        layout.addWidget(grid_widget)
        return widget
    
    def create_stats_widget(self):
        """Создание виджета статистики"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Заголовок
        title = QLabel("📊 Статистика")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: white; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Контейнер для статистики
        stats_container = QWidget()
        stats_layout = QHBoxLayout(stats_container)
        stats_layout.setContentsMargins(0, 0, 0, 0)
        stats_layout.setSpacing(10)
        
        stats = [
            ("📈", "Прогресс", [
                ("Уровень:", "1"),
                ("Опыт:", "0/1000"),
                ("Подарки:", "0")
            ]),
            ("🏆", "Достижения", [
                ("Новичок:", "✅"),
                ("Исследователь:", "❌"),
                ("Коллекционер:", "❌")
            ]),
            ("🎯", "Активность", [
                ("Игровое время:", "0ч"),
                ("Запусков:", "0"),
                ("Серверов:", "0")
            ])
        ]
        
        for icon, title_text, items in stats:
            frame = QFrame()
            frame.setStyleSheet("""
                QFrame {
                    background-color: rgba(255, 255, 255, 0.05);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    border-radius: 10px;
                    padding: 15px;
                }
            """)
            frame_layout = QVBoxLayout(frame)
            frame_layout.setSpacing(5)
            
            # Заголовок блока
            block_title = QLabel(f"{icon} {title_text}")
            block_title.setStyleSheet("font-weight: bold; font-size: 16px; color: #4facfe;")
            frame_layout.addWidget(block_title)
            
            # Элементы статистики
            for label, value in items:
                item_widget = QWidget()
                item_layout = QHBoxLayout(item_widget)
                item_layout.setContentsMargins(0, 0, 0, 0)
                
                label_widget = QLabel(label)
                label_widget.setStyleSheet("color: #aaaaaa;")
                
                value_widget = QLabel(value)
                value_widget.setStyleSheet("color: white; font-weight: bold;")
                
                item_layout.addWidget(label_widget)
                item_layout.addStretch()
                item_layout.addWidget(value_widget)
                
                frame_layout.addWidget(item_widget)
            
            frame_layout.addStretch()
            stats_layout.addWidget(frame)
        
        layout.addWidget(stats_container)
        return widget
    
    def create_account_page(self):
        """Создание страницы аккаунта"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        title = QLabel("👤 Мой Аккаунт")
        title.setStyleSheet("font-size: 28px; font-weight: bold; margin-bottom: 20px; color: white;")
        layout.addWidget(title)
        
        # Информация об аккаунте
        info_group = QGroupBox("Информация об аккаунте")
        info_group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #4facfe;
                border: 2px solid #4facfe;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
            }
        """)
        
        info_layout = QVBoxLayout()
        
        # Данные пользователя
        user_data = [
            ("Имя пользователя:", "Гость"),
            ("Email:", "Не указан"),
            ("Уровень:", "1"),
            ("Опыт:", "0"),
            ("Дата регистрации:", "Не зарегистрирован")
        ]
        
        for label, value in user_data:
            row_widget = QWidget()
            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(10, 5, 10, 5)
            
            label_widget = QLabel(label)
            label_widget.setStyleSheet("color: #aaaaaa; font-size: 14px;")
            label_widget.setMinimumWidth(150)
            
            value_widget = QLabel(value)
            value_widget.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
            
            row_layout.addWidget(label_widget)
            row_layout.addWidget(value_widget)
            row_layout.addStretch()
            
            info_layout.addWidget(row_widget)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # Лицензии
        license_group = QGroupBox("Лицензии")
        license_group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #4facfe;
                border: 2px solid #4facfe;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
            }
        """)
        
        license_layout = QVBoxLayout()
        
        self.license_label = QLabel("Статус: Бесплатная версия")
        self.license_label.setStyleSheet("color: white; font-size: 14px; padding: 10px;")
        license_layout.addWidget(self.license_label)
        
        # Поле для ввода ключа
        key_widget = QWidget()
        key_layout = QHBoxLayout(key_widget)
        key_layout.setContentsMargins(10, 5, 10, 5)
        
        self.license_input = QLineEdit()
        self.license_input.setPlaceholderText("Введите ключ лицензии...")
        self.license_input.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 5px;
                padding: 8px;
                color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #4facfe;
            }
        """)
        
        self.activate_license_btn = QPushButton("Активировать")
        self.activate_license_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.activate_license_btn.setStyleSheet("""
            QPushButton {
                background-color: #4facfe;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3a9bed;
            }
            QPushButton:disabled {
                background-color: #666666;
                color: #aaaaaa;
            }
        """)
        self.activate_license_btn.clicked.connect(self.activate_license)
        
        key_layout.addWidget(self.license_input)
        key_layout.addWidget(self.activate_license_btn)
        license_layout.addWidget(key_widget)
        
        # Информация о лицензиях
        license_info = QLabel("• Standard: Все основные функции\n• Premium: Дополнительные темы и скины\n• Ultimate: Полный доступ ко всему")
        license_info.setStyleSheet("color: #aaaaaa; font-size: 12px; padding: 10px; background-color: rgba(255, 255, 255, 0.05); border-radius: 5px;")
        license_layout.addWidget(license_info)
        
        license_group.setLayout(license_layout)
        layout.addWidget(license_group)
        
        # Кнопки управления
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        button_layout.setContentsMargins(0, 10, 0, 0)
        
        btn_logout = QPushButton("Выйти из аккаунта")
        btn_logout.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_logout.setStyleSheet("""
            QPushButton {
                background-color: #ff5555;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ff4444;
            }
        """)
        btn_logout.clicked.connect(self.logout_user)
        
        btn_delete = QPushButton("Удалить аккаунт")
        btn_delete.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_delete.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 85, 85, 0.3);
                color: #ff5555;
                border: 1px solid #ff5555;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 85, 85, 0.5);
            }
        """)
        btn_delete.clicked.connect(self.delete_account)
        
        button_layout.addWidget(btn_logout)
        button_layout.addStretch()
        button_layout.addWidget(btn_delete)
        
        layout.addWidget(button_widget)
        layout.addStretch()
        
        return page
    

    
    def create_skins_page(self):
        """Создание страницы скинов"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        title = QLabel("🖼️ Скины и Оформление")
        title.setStyleSheet("font-size: 28px; font-weight: bold; margin-bottom: 20px; color: white;")
        layout.addWidget(title)
        
        # Текущий скин
        current_group = QGroupBox("🎯 Текущий скин")
        current_group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #4facfe;
                border: 2px solid #4facfe;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
            }
        """)
        
        current_layout = QHBoxLayout()
        current_layout.setContentsMargins(15, 15, 15, 15)
        
        self.current_skin_preview = QLabel("👤")
        self.current_skin_preview.setFixedSize(120, 120)
        self.current_skin_preview.setStyleSheet("""
            border: 3px solid #4facfe;
            border-radius: 10px;
            font-size: 72px;
            text-align: center;
            background-color: rgba(255, 255, 255, 0.1);
        """)
        current_layout.addWidget(self.current_skin_preview)
        
        skin_info = QWidget()
        skin_info_layout = QVBoxLayout(skin_info)
        skin_info_layout.setSpacing(10)
        
        self.current_skin_name = QLabel("Стандартный")
        self.current_skin_name.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
        skin_info_layout.addWidget(self.current_skin_name)
        
        skin_desc = QLabel("Базовый скин по умолчанию")
        skin_desc.setStyleSheet("color: #aaaaaa; font-size: 14px;")
        skin_desc.setWordWrap(True)
        skin_info_layout.addWidget(skin_desc)
        
        # Кнопка применения
        btn_apply = QPushButton("Применить скин")
        btn_apply.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_apply.setStyleSheet("""
            QPushButton {
                background-color: #4facfe;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-weight: bold;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #3a9bed;
            }
        """)
        btn_apply.clicked.connect(lambda: self.apply_skin("default"))
        skin_info_layout.addWidget(btn_apply)
        
        skin_info_layout.addStretch()
        current_layout.addWidget(skin_info)
        current_layout.addStretch()
        
        current_group.setLayout(current_layout)
        layout.addWidget(current_group)
        
        # Библиотека скинов
        skins_group = QGroupBox("📚 Библиотека скинов")
        skins_group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #4facfe;
                border: 2px solid #4facfe;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
            }
        """)
        
        # Создаем сетку для скинов
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        
        skins_container = QWidget()
        self.skins_grid = QGridLayout(skins_container)
        self.skins_grid.setContentsMargins(10, 10, 10, 10)
        self.skins_grid.setSpacing(15)
        
        # Добавляем тестовые скины
        test_skins = [
            ("👤", "Стандартный", "Бесплатно", True),
            ("🎅", "Санта", "500 XP", False),
            ("⛄", "Снеговик", "300 XP", False),
            ("🦌", "Олень", "400 XP", False),
            ("🎄", "Ёлка", "250 XP", False),
            ("🌟", "Звезда", "600 XP", False),
            ("❄️", "Снежинка", "350 XP", False),
            ("🎁", "Подарок", "450 XP", False)
        ]
        
        row, col = 0, 0
        for icon, name, price, unlocked in test_skins:
            skin_widget = self.create_skin_widget(icon, name, price, unlocked)
            self.skins_grid.addWidget(skin_widget, row, col)
            
            col += 1
            if col > 3:  # 4 колонки
                col = 0
                row += 1
        
        scroll.setWidget(skins_container)
        
        skins_layout = QVBoxLayout()
        skins_layout.addWidget(scroll)
        skins_group.setLayout(skins_layout)
        layout.addWidget(skins_group)
        
        # Кнопка загрузки своего скина
        btn_upload = QPushButton("📤 Загрузить свой скин")
        btn_upload.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_upload.setStyleSheet("""
            QPushButton {
                background-color: rgba(79, 172, 254, 0.2);
                color: #4facfe;
                border: 2px dashed #4facfe;
                border-radius: 8px;
                padding: 15px;
                font-size: 16px;
                font-weight: bold;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: rgba(79, 172, 254, 0.3);
            }
        """)
        btn_upload.clicked.connect(self.upload_custom_skin)
        layout.addWidget(btn_upload)
        
        layout.addStretch()
        return page
    
    def create_skin_widget(self, icon, name, price, unlocked):
        """Создание виджета скина"""
        widget = QFrame()
        widget.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                padding: 10px;
            }
            QFrame:hover {
                border: 1px solid #4facfe;
                background-color: rgba(79, 172, 254, 0.1);
            }
        """)
        widget.setFixedSize(180, 180)
        
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        
        # Иконка скина
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 48px; text-align: center;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)
        
        # Название
        name_label = QLabel(name)
        name_label.setStyleSheet("font-weight: bold; font-size: 14px; color: white; text-align: center;")
        name_label.setWordWrap(True)
        layout.addWidget(name_label)
        
        # Цена/статус
        status_label = QLabel("Разблокирован" if unlocked else price)
        status_label.setStyleSheet(f"""
            color: {'#4facfe' if unlocked else '#FFD700'};
            font-size: 12px;
            text-align: center;
        """)
        layout.addWidget(status_label)
        
        # Кнопка
        btn_text = "Применить" if unlocked else "Разблокировать"
        btn = QPushButton(btn_text)
        btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {'#4facfe' if unlocked else 'rgba(255, 215, 0, 0.2)'};
                color: {'white' if unlocked else '#FFD700'};
                border: none;
                border-radius: 5px;
                padding: 5px;
                font-size: 12px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {'#3a9bed' if unlocked else 'rgba(255, 215, 0, 0.3)'};
            }}
        """)
        
        if unlocked:
            btn.clicked.connect(lambda: self.apply_skin(name))
        else:
            btn.clicked.connect(lambda: self.unlock_skin(name, price))
        
        layout.addWidget(btn)
        
        return widget
    
    def setup_status_bar(self):
        status_bar = self.statusBar()
        status_bar.setStyleSheet("""
            QStatusBar {
                background: #0e0e16;
                color: rgba(255,255,255,0.25);
                border-top: 1px solid rgba(255,255,255,0.03);
                font-size: 11px;
                padding: 1px 16px;
            }
        """)
        
        self.status_user_label = QLabel("👤  Гость")
        self.status_user_label.setStyleSheet("padding: 2px 6px; font-size: 11px; color: rgba(255,255,255,0.4);")
        status_bar.addWidget(self.status_user_label)
        
        sep1 = QLabel("·")
        sep1.setStyleSheet("color: rgba(255,255,255,0.1);")
        status_bar.addWidget(sep1)
        
        version_label = QLabel(f"✦  {CURRENT_VERSION}")
        version_label.setStyleSheet("padding: 2px 6px; font-size: 11px; color: rgba(255,255,255,0.2);")
        status_bar.addWidget(version_label)
        
        sep2 = QLabel("·")
        sep2.setStyleSheet("color: rgba(255,255,255,0.1);")
        status_bar.addWidget(sep2)
        
        self.session_label = QLabel("")
        self.session_label.setStyleSheet("padding: 2px 6px; font-size: 11px; color: rgba(168,85,247,0.6); font-weight: 500;")
        status_bar.addWidget(self.session_label)
        
        # Разделитель
        status_bar.addWidget(QLabel("|"))
        
        # Время
        self.status_time_label = QLabel()
        self.status_time_label.setStyleSheet("padding: 5px; font-size: 12px;")
        status_bar.addPermanentWidget(self.status_time_label)
        
        # Таймер обновления времени
        self.time_timer = QTimer()
        self.time_timer.timeout.connect(self.update_time)
        self.time_timer.start(1000)
        self.update_time()
    
    def update_time(self):
        """Обновление времени в статусбаре"""
        current_time = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.status_time_label.setText(f"🕒 {current_time}")
    
    def check_auto_login(self):
        """Проверка автоматического входа"""
        # Можно добавить сохранение сессии
        pass
    
    def show_login_dialog(self):
        """Показать диалог входа"""
        dialog = LoginDialog(self.account_system, self)
        if dialog.exec():
            user = dialog.get_user()
            if user:
                self.update_user_info(user)
                self.check_for_gifts()
    
    def update_user_info(self, user):
        """Обновление информации о пользователе"""
        self.username_label.setText(user["username"])
        self.user_status_label.setText(f"Уровень {user.get('level', 1)} • {user.get('xp', 0)} XP")
        self.login_button.setText("Выйти")
        self.login_button.clicked.disconnect()
        self.login_button.clicked.connect(self.logout_user)
        
        self.status_user_label.setText(f"👤 {user['username']} | Ур. {user.get('level', 1)}")
    
    def logout_user(self):
        """Выход пользователя"""
        self.account_system.logout()
        self.username_label.setText("Гость")
        self.user_status_label.setText("Не авторизован")
        self.login_button.setText("Войти / Зарегистрироваться")
        self.login_button.clicked.disconnect()
        self.login_button.clicked.connect(self.show_login_dialog)
        
        self.status_user_label.setText("👤 Гость")
    
    def delete_account(self):
        """Удаление аккаунта"""
        reply = QMessageBox.question(
            self,
            "Удаление аккаунта",
            "Вы уверены, что хотите удалить аккаунт? Это действие нельзя отменить.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            QMessageBox.information(
                self,
                "Удаление аккаунта",
                "Функция удаления аккаунта находится в разработке."
            )
    
    def apply_skin(self, skin_name):
        """Применение скина"""
        if not self.account_system.current_user:
            QMessageBox.warning(self, "Ошибка", "Требуется вход в аккаунт")
            return
        
        success, message = self.skins_manager.apply_skin_to_minecraft(skin_name.lower().replace(" ", "_"))
        if success:
            self.current_skin_name.setText(skin_name)
            QMessageBox.information(self, "Успех", message)
        else:
            QMessageBox.warning(self, "Ошибка", message)
    
    def unlock_skin(self, skin_name, price):
        """Разблокировка скина"""
        if not self.account_system.current_user:
            QMessageBox.warning(self, "Ошибка", "Требуется вход в аккаунт")
            return
        
        skin_id = skin_name.lower().replace(" ", "_")
        user = self.account_system.current_user
        
        success, message = self.skins_manager.unlock_skin(skin_id, user)
        if success:
            QMessageBox.information(self, "Успех", message)
            # Обновляем страницу скинов
            self.pages.setCurrentIndex(4)  # Переходим на страницу скинов
        else:
            QMessageBox.warning(self, "Ошибка", message)
    
    def upload_custom_skin(self):
        """Загрузка кастомного скина"""
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Выберите изображение скина")
        file_dialog.setNameFilter("Изображения (*.png *.jpg *.jpeg)")
        
        if file_dialog.exec():
            files = file_dialog.selectedFiles()
            if files:
                image_path = files[0]
                success, result = self.skins_manager.upload_custom_skin(image_path)
                if success:
                    QMessageBox.information(self, "Успех", f"Скин загружен! ID: {result}")
                else:
                    QMessageBox.warning(self, "Ошибка", result)
    
    def activate_license(self):
        """Активация лицензии"""
        license_key = self.license_input.text().strip()
        if not license_key:
            QMessageBox.warning(self, "Ошибка", "Введите ключ лицензии")
            return
        
        if not self.account_system.current_user:
            QMessageBox.warning(self, "Ошибка", "Требуется вход в аккаунт")
            return
        
        success, message = self.account_system.activate_license(
            license_key,
            self.account_system.current_user["user_id"]
        )
        
        if success:
            QMessageBox.information(self, "Успех", message)
            self.license_label.setText(f"Статус: {self.account_system.current_user.get('license_tier', 'free').upper()}")
        else:
            QMessageBox.critical(self, "Ошибка", message)
    
    
    def show_toast(self, title, message, duration=3000):
        toast = QLabel(f"<b>{title}</b><br>{message}", self)
        toast.setStyleSheet("""
            background-color: #4facfe; color: white; border-radius: 10px;
            padding: 15px 25px; font-size: 14px;
        """)
        toast.setAlignment(Qt.AlignmentFlag.AlignCenter)
        toast.adjustSize()
        toast.move((self.width() - toast.width()) // 2, 20)
        toast.setWordWrap(True)
        toast.setFixedWidth(min(toast.width() + 40, self.width() - 40))
        toast.show()
        QTimer.singleShot(duration, toast.deleteLater)

    def show_help(self):
        """Показать справку"""
        QMessageBox.information(
            self,
            "Помощь",
            "SuperLauncher 2026 - Новогоднее издание\n\n"
            "🎮 Быстрый запуск: Нажмите кнопку 'Играть' на странице Minecraft\n"
            "🎁 Подарки: Заходите ежедневно за бесплатными наградами\n"
            "👤 Аккаунт: Создайте аккаунт для синхронизации и доступа к премиум функциям\n"
            "🖼️ Скины: Разблокируйте и применяйте уникальные скины\n"
            "📦 Сборки: Устанавливайте готовые сборки модов\n"
            "🧩 Моды: Ищите и устанавливайте моды из Modrinth\n"
            "📢 Новости: Следите за обновлениями лаунчера\n"
            "🔄 Обновления: Обновляйте лаунчер до последней версии\n"
            "🖧 Серверы: Создавайте и управляйте Minecraft-серверами\n"
            "⚙️ Настройки: Настройте лаунчер под себя\n\n"
            "Поддержка: https://github.com/Ludvig2457Ultra/SuperLauncherMC"
        )
    
    def show_stats(self):
        """Показать статистику"""
        QMessageBox.information(
            self,
            "Статистика",
            "Ваша статистика:\n\n"
            "• Уровень: 1\n"
            "• Опыт: 0/1000\n"
            "• Игровое время: 0 часов\n"
            "• Запусков: 0\n"
            "• Получено подарков: 0\n"
            "• Разблокировано скинов: 1\n"
            "• Установлено сборок: 0"
        )
    
    def show_social(self):
        """Показать социальные функции"""
        QMessageBox.information(
            self,
            "Социальное",
            "Социальные функции:\n\n"
            "• Друзья (в разработке)\n"
            "• Группы (в разработке)\n"
            "• Общие сборки (в разработке)\n"
            "• Рейтинги (в разработке)\n\n"
            "Эти функции появятся в следующих обновлениях!"
        )
    
    # Существующие методы
    def tr(self, key: str) -> str:
        lang = "ru"
        if hasattr(self, "settings_page") and self.settings_page:
            lang = self.settings_page.config.get("language", "ru")
        return translations.get(lang, {}).get(key, key)
    
    def on_button_clicked(self, button):
        idx = self.sidebar.nav_buttons.index(button)
        if idx < self.pages.count():
            self.pages.setCurrentIndex(idx)
            for i, btn in enumerate(self.sidebar.nav_buttons):
                btn.setChecked(i == idx)
        else:
            print(f"⚠️ Ошибка: страница с индексом {idx} не существует")
    
    def update_progress(self, value, max_value, label):
        minecraft_page = self.pages.widget(9)  # Minecraft страница — индекс 9
        if hasattr(minecraft_page, 'start_progress'):
            minecraft_page.start_progress.setMaximum(max_value)
            minecraft_page.start_progress.setValue(value)
            minecraft_page.start_progress_label.setText(label)
    
    def _update_session_label(self):
        if self.launch_start_time:
            elapsed = datetime.datetime.now() - self.launch_start_time
            total_sec = int(elapsed.total_seconds())
            m = total_sec // 60
            s = total_sec % 60
            self.session_label.setText(f"⏱ Session: {m}m {s}s")

    def state_update(self, running):
        if not running:
            self.session_timer.stop()
            self.launch_start_time = None
            self.session_label.setText("")
        minecraft_page = self.pages.widget(9)  # Minecraft страница — индекс 9
        if hasattr(minecraft_page, 'start_button'):
            minecraft_page.start_button.setDisabled(running)
        if hasattr(minecraft_page, 'start_progress'):
            minecraft_page.start_progress.setVisible(running)
            minecraft_page.start_progress_label.setVisible(running)
    
    def show_launch_error(self, error_msg):
        QMessageBox.critical(self, "Ошибка запуска", f"Minecraft не запустился:\n{error_msg}")

    def apply_settings(self):
        if hasattr(self, "settings_page"):
            theme = self.settings_page.config.get("theme", "dark")
            # Обновляем тему
            self.custom_ui.apply_to_widget(self)
    
    def _launch_instance(self, inst):
        if hasattr(self, "settings_page"):
            config = self.settings_page.config
        else:
            config = {}

        user = self.account_system.current_user
        username = user["username"] if user else "player"
        uuid_str = user.get("user_id", str(uuid1())) if user else str(uuid1())
        token_str = user.get("mc_token", "") if user else ""

        inst_dir = os.path.join(INSTANCES_DIR, inst["id"], "game")

        self.launch_thread.mc_directory = inst_dir
        self.launch_thread.max_ram = inst.get("max_ram", config.get("max_ram", 4096))
        self.launch_thread.min_ram = max(1024, inst.get("max_ram", 4096) // 4)
        self.launch_thread.java_path = inst.get("java_path", config.get("java_path", ""))
        self.launch_thread.jvm_args = inst.get("jvm_args", config.get("jvm_args", ""))
        self.launch_thread.uuid = uuid_str
        self.launch_thread.token = token_str

        if config.get("launch_mode") == "java" and config.get("java_path"):
            self.launch_thread.java_path = config["java_path"]

        loader = inst.get("loader", "Vanilla").lower()
        version = inst.get("mc_version", "latest_release")

        instances = load_instances()
        for x in instances:
            if x["id"] == inst["id"]:
                x["last_played"] = datetime.datetime.now().isoformat()
                break
        save_instances(instances)

        self.launch_thread.launch_setup_signal.emit(version, username, loader)
        self.launch_thread.start()

    def launch_game(self):
        minecraft_page = self.pages.widget(9)
        if hasattr(self, "settings_page"):
            config = self.settings_page.config
            version = minecraft_page.version_select.currentText()
            username = minecraft_page.username.text() or "player"
            loader_type = minecraft_page.loader_select.currentText().lower()

            if self.account_system.current_user:
                username = self.account_system.current_user["username"]

            user = self.account_system.current_user
            uuid_str = user.get("user_id", str(uuid1())) if user else str(uuid1())
            token_str = user.get("mc_token", "") if user else ""

            self.launch_thread.max_ram = config.get("max_ram", 4096)
            self.launch_thread.min_ram = max(1024, config.get("max_ram", 4096) // 4)
            self.launch_thread.java_path = config.get("java_path", "")
            self.launch_thread.jvm_args = config.get("jvm_args", "")
            self.launch_thread.uuid = uuid_str
            self.launch_thread.token = token_str

            if config.get("launch_mode") == "java" and config.get("java_path"):
                self.launch_thread.java_path = config["java_path"]

            # Сохраняем последние ник/версию/загрузчик
            config["last_username"] = username
            config["last_version_id"] = version
            config["last_loader_type"] = loader_type
            save_config(config)

            self.launch_start_time = datetime.datetime.now()
            self.session_timer.start()
            self.session_label.setText("⏱ Session: 0m 0s")
            self.show_toast("Minecraft", "Запуск...")

            self.launch_thread.launch_setup_signal.emit(version, username, loader_type)
            self.launch_thread.start()
    
    def closeEvent(self, event):
        if hasattr(self, "discord_rpc_thread") and self.discord_rpc_thread:
            self.discord_rpc_thread.stop()
        super().closeEvent(event)

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())