import os
import secrets
import datetime
from PIL import Image
from ..core.constants import DATA_DIR

class SkinsManager:
    def __init__(self):
        self.skins_dir = os.path.join(DATA_DIR, "assets", "skins")
        os.makedirs(self.skins_dir, exist_ok=True)
        self.library = {
            "default": {"name": "Стандартный", "rarity": "common", "price": 0},
            "santa_hat": {"name": "Шапка Санты", "rarity": "holiday", "price": 0},
            "santa_suit": {"name": "Костюм Санты", "rarity": "epic", "price": 500},
            "new_year_2026": {"name": "2026 Новый Год", "rarity": "legendary", "price": 1000},
            "reindeer": {"name": "Олень Рудольф", "rarity": "rare", "price": 300},
            "snowman": {"name": "Снеговик", "rarity": "rare", "price": 250},
        }

    def is_unlocked(self, skin_id, user):
        if skin_id == "default":
            return True
        return skin_id in user.get("skins", ["default"])

    def unlock(self, skin_id, user):
        if self.is_unlocked(skin_id, user):
            return False, "Уже разблокирован"
        skin = self.library.get(skin_id)
        if not skin:
            return False, "Не найден"
        price = skin.get("price", 0)
        if price > 0 and user.get("xp", 0) < price:
            return False, f"Нужно {price} XP"
        if price > 0:
            user["xp"] = user.get("xp", 0) - price
        user.setdefault("skins", []).append(skin_id)
        return True, f"Скин '{skin['name']}' разблокирован!"

    def upload_custom(self, image_path, user):
        if not os.path.exists(image_path):
            return False, "Файл не найден"
        try:
            img = Image.open(image_path)
            if img.size not in [(64, 64), (64, 32)]:
                return False, "Размер должен быть 64x64 или 64x32"
            skin_id = f"custom_{secrets.token_hex(8)}"
            dst = os.path.join(DATA_DIR, "user_data", user["user_id"], "skins", f"{skin_id}.png")
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            img.save(dst)
            user.setdefault("custom_skins", []).append({
                "id": skin_id, "uploaded_at": datetime.datetime.now().isoformat()})
            return True, skin_id
        except Exception as e:
            return False, str(e)
