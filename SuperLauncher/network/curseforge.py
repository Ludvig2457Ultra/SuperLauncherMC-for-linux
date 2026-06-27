import requests
from ..core.constants import CURSEFORGE_API
from ..core.config import AppConfig

class CurseForgeAPI:
    @classmethod
    def _headers(cls):
        return {"x-api-key": AppConfig.get_cf_api_key(), "Accept": "application/json"}

    @classmethod
    def search_mods(cls, query="", limit=30, class_id=6):
        try:
            params = {"gameId": 432, "classId": class_id, "searchFilter": query,
                      "pageSize": limit, "sortField": 2, "sortOrder": "desc"}
            resp = requests.get(f"{CURSEFORGE_API}/mods/search", params=params,
                                headers=cls._headers(), timeout=15)
            return resp.json().get("data", [])
        except Exception:
            return []

    @classmethod
    def search_modpacks(cls, query="", limit=30):
        return cls.search_mods(query, limit, class_id=4471)

    @classmethod
    def get_files(cls, mod_id):
        try:
            resp = requests.get(f"{CURSEFORGE_API}/mods/{mod_id}/files",
                                headers=cls._headers(), timeout=15)
            return resp.json().get("data", [])
        except Exception:
            return []

    @classmethod
    def get_download_url(cls, mod_id, file_id):
        try:
            resp = requests.get(f"{CURSEFORGE_API}/mods/{mod_id}/files/{file_id}/download-url",
                                headers=cls._headers(), timeout=15)
            return resp.json().get("data", "")
        except Exception:
            return ""
