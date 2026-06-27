from PyQt6.QtWidgets import (
    QMainWindow, QStackedWidget, QHBoxLayout, QLabel, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon

from ..core.config import AppConfig
from ..core.translations import Translations
from ..backend.account import AccountSystem
from ..backend.builds import BuildsManager
from ..backend.skins import SkinsManager
from ..backend.minecraft import MinecraftLauncher
from ..backend.servers import ServerManager
from ..backend.discord_rpc import DiscordRPC
from ..backend.updates import UpdateChecker
from .theme import ThemeManager
from .sidebar import ModernSidebar
from .glass_frame import GlassFrame
from .pages import (
    HomePage, AccountPage, ModsPage, BuildsPage, SkinsPage,
    NewsPage, UpdatesPage, ServersPage, SettingsPage, MinecraftPage, AIAgentPage
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SuperLauncher 2.0")
        self.setMinimumSize(1100, 700)
        self.resize(1280, 800)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.config = AppConfig()
        self.translations = Translations()
        self.theme = ThemeManager()
        self.account = AccountSystem()
        self.builds = BuildsManager()
        self.skins = SkinsManager()
        self.launcher = MinecraftLauncher()
        self.servers = ServerManager()
        self.discord = DiscordRPC()
        self.updater = UpdateChecker()

        self._setup_ui()
        self._setup_connections()

    def _setup_ui(self):
        glass = GlassFrame(self)
        glass.set_tint(25, 25, 35, 220)

        layout = QHBoxLayout(glass)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(0)

        self.sidebar = ModernSidebar(self)
        layout.addWidget(self.sidebar)

        self.stack = QStackedWidget(glass)
        self.stack.setStyleSheet(
            "QStackedWidget { background: rgba(30,30,40,0.85); "
            "border: 1px solid rgba(255,255,255,0.08); border-radius: 14px; }")
        layout.addWidget(self.stack, 1)

        self._init_pages()
        self.stack.setCurrentIndex(0)
        self.setCentralWidget(glass)
        self.setStyleSheet(self.theme.stylesheet())

    def _init_pages(self):
        self.pages = [
            HomePage(self),
            AccountPage(self),
            ModsPage(self),
            BuildsPage(self),
            SkinsPage(self),
            NewsPage(self),
            UpdatesPage(self),
            ServersPage(self),
            SettingsPage(self),
            MinecraftPage(self),
            AIAgentPage(self),
        ]
        for p in self.pages:
            self.stack.addWidget(p)

    def _setup_connections(self):
        if self.config.get("discord_rpc", True):
            self.discord.connect()
        self.updater.check("v2.0.0_2026")

    def navigate_to(self, index):
        if 0 <= index < self.stack.count():
            self.stack.setCurrentIndex(index)
