import json
import os
import hashlib
import secrets
import datetime
from ..core.constants import ACCOUNTS_FILE, LICENSES_FILE, DATA_DIR

class AccountSystem:
    def __init__(self):
        self.current_user = None
        self._ensure_files()

    def _ensure_files(self):
        if not os.path.exists(ACCOUNTS_FILE):
            self._save([], ACCOUNTS_FILE)
        if not os.path.exists(LICENSES_FILE):
            self._save({}, LICENSES_FILE)

    def _load(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {} if "license" in path else []

    def _save(self, data, path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def register(self, username, email, password):
        accounts = self._load(ACCOUNTS_FILE)
        for a in accounts:
            if a["username"] == username:
                return False, "Имя занято"
            if a["email"] == email:
                return False, "Email занят"
        user_id = secrets.token_hex(16)
        salt = secrets.token_hex(8)
        pw_hash = hashlib.sha256(f"{password}{salt}".encode()).hexdigest()
        user = {"user_id": user_id, "username": username, "email": email,
                "password_hash": pw_hash, "salt": salt,
                "created_at": datetime.datetime.now().isoformat(),
                "license_tier": "free", "level": 1, "xp": 0, "skins": ["default"]}
        accounts.append(user)
        self._save(accounts, ACCOUNTS_FILE)
        os.makedirs(os.path.join(DATA_DIR, "user_data", user_id), exist_ok=True)
        return True, user

    def login(self, username_or_email, password):
        accounts = self._load(ACCOUNTS_FILE)
        for a in accounts:
            if a["username"] == username_or_email or a["email"] == username_or_email:
                pw_hash = hashlib.sha256(f"{password}{a['salt']}".encode()).hexdigest()
                if pw_hash == a["password_hash"]:
                    a["last_login"] = datetime.datetime.now().isoformat()
                    self._save(accounts, ACCOUNTS_FILE)
                    self.current_user = a
                    return True, a
        return False, "Неверный логин или пароль"

    def logout(self):
        self.current_user = None

    def activate_license(self, key, user_id):
        licenses = self._load(LICENSES_FILE)
        if key not in licenses:
            return False, "Неверный ключ"
        lic = licenses[key]
        if lic.get("activated"):
            return False, "Уже активирована"
        if datetime.datetime.now().timestamp() > lic.get("expires_at", 0):
            return False, "Срок истек"
        lic["activated"] = True
        lic["activated_by"] = user_id
        self._save(licenses, LICENSES_FILE)
        accounts = self._load(ACCOUNTS_FILE)
        for a in accounts:
            if a["user_id"] == user_id:
                a["license_tier"] = lic.get("tier", "standard")
                self._save(accounts, ACCOUNTS_FILE)
                if self.current_user and self.current_user.get("user_id") == user_id:
                    self.current_user["license_tier"] = a["license_tier"]
                break
        return True, "Лицензия активирована!"
