import json
import os
from .constants import CONFIG_FILE

_cf_api_key_cache = None

class AppConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._loaded = False
        return cls._instance

    def __init__(self):
        if self._loaded:
            return
        self._loaded = True
        self.data = self._load()

    def _load(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "java_path": "", "ram": 4096, "max_ram": 4096,
            "jvm_args": "", "language": "ru", "theme": "dark",
            "launch_mode": "launcher_lib", "curseforge_api_key": "",
            "page_bg": "dark", "discord_rpc": True, "dark_mode": True,
            "holiday_theme": False, "auto_login": False,
        }

    def save(self):
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)
        except Exception:
            pass

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value

    @staticmethod
    def get_cf_api_key():
        global _cf_api_key_cache
        if _cf_api_key_cache is None:
            _cf_api_key_cache = AppConfig().get("curseforge_api_key", "")
        return _cf_api_key_cache

    @staticmethod
    def invalidate_cf_key():
        global _cf_api_key_cache
        _cf_api_key_cache = None
