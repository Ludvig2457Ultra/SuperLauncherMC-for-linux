import requests
from ..core.constants import MODRINTH_API

class ModrinthAPI:
    HEADERS = {"User-Agent": "SuperLauncher/2.0"}

    @classmethod
    def search_mods(cls, query="", limit=30):
        try:
            params = {"limit": limit, "index": "downloads"}
            if query:
                params["query"] = query
            resp = requests.get(f"{MODRINTH_API}/search", params=params, headers=cls.HEADERS, timeout=15)
            return resp.json().get("hits", [])
        except Exception:
            return []

    @classmethod
    def search_modpacks(cls, query="", limit=20):
        try:
            params = {"limit": limit, "index": "downloads",
                      "facets": '[["project_type:modpack"]]'}
            if query:
                params["query"] = query
            resp = requests.get(f"{MODRINTH_API}/search", params=params, headers=cls.HEADERS, timeout=15)
            return resp.json().get("hits", [])
        except Exception:
            return []

    @classmethod
    def get_versions(cls, project_id):
        try:
            resp = requests.get(f"{MODRINTH_API}/project/{project_id}/version", headers=cls.HEADERS, timeout=15)
            return resp.json()
        except Exception:
            return []

    @classmethod
    def get_project(cls, project_id):
        try:
            resp = requests.get(f"{MODRINTH_API}/project/{project_id}", headers=cls.HEADERS, timeout=15)
            return resp.json()
        except Exception:
            return {}
