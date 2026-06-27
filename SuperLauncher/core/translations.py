import json
import os
from .config import AppConfig

class Translations:
    _instance = None
    _data = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        pass

    def tr(self, key):
        lang = AppConfig().get("language", "ru")
        table = self._data.get(lang, {})
        return table.get(key, key)

    def load(self, lang=None):
        if lang is None:
            lang = AppConfig().get("language", "ru")
        path = os.path.join("assets", "lang", f"{lang}.json")
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    self._data[lang] = json.load(f)
            except Exception:
                self._data[lang] = {}
        else:
            self._data[lang] = {}
