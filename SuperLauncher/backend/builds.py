import os
import json
import shutil
import tempfile
import zipfile
import requests
import datetime
from ..network.api_client import ApiClient
from ..core.config import AppConfig

class BuildsManager:
    def search_modrinth(self, query="", limit=20):
        try:
            params = {"limit": limit, "index": "downloads",
                      "facets": '[["project_type:modpack"]]'}
            if query:
                params["query"] = query
            resp = requests.get("https://api.modrinth.com/v2/search",
                                params=params, headers={"User-Agent": "SuperLauncher/2.0"}, timeout=15)
            hits = resp.json().get("hits", [])
            return [{
                "id": h["project_id"], "name": h["title"],
                "description": h.get("description", "")[:100],
                "downloads": h.get("downloads", 0), "author": h.get("author", "?"),
                "icon_url": h.get("icon_url"), "source": "modrinth"
            } for h in hits]
        except Exception:
            return []

    def search_curseforge(self, query="", limit=30):
        try:
            params = {"gameId": 432, "classId": 4471, "searchFilter": query,
                      "pageSize": limit, "sortField": 2, "sortOrder": "desc"}
            resp = requests.get("https://api.curseforge.com/v1/mods/search", params=params,
                                headers={"x-api-key": AppConfig.get_cf_api_key(),
                                         "Accept": "application/json"}, timeout=15)
            data = resp.json().get("data", [])
            return [{
                "id": m["id"], "name": m.get("name", "?"),
                "description": m.get("summary", "")[:100],
                "downloads": m.get("downloadCount", 0),
                "author": (m.get("authors") or [{}])[0].get("name", "?") if m.get("authors") else "?",
                "icon_url": (m.get("logo") or {}).get("url"),
                "source": "curseforge"
            } for m in data]
        except Exception:
            return []

    def get_versions(self, project_id, source="modrinth"):
        if source == "modrinth":
            try:
                r = requests.get(f"https://api.modrinth.com/v2/project/{project_id}/version",
                                 headers={"User-Agent": "SuperLauncher/2.0"}, timeout=15)
                return r.json()
            except Exception:
                return []
        try:
            r = requests.get(f"https://api.curseforge.com/v1/mods/{project_id}/files",
                             headers={"x-api-key": AppConfig.get_cf_api_key(),
                                      "Accept": "application/json"}, timeout=15)
            return r.json().get("data", [])
        except Exception:
            return []

    def download_and_install(self, version_data, source, mc_dir, callback=None):
        if source == "modrinth":
            return self._install_modrinth(version_data, mc_dir, callback)
        return self._install_curseforge(version_data, mc_dir, callback)

    def _install_modrinth(self, version_data, mc_dir, callback=None):
        files = version_data.get("files", [])
        if not files:
            return None, "Нет файлов"
        primary = next((f for f in files if f.get("primary")), files[0])
        tmp = tempfile.mkdtemp(prefix="mrpack-")
        try:
            ApiClient.download_file(primary["url"], os.path.join(tmp, primary["filename"]), callback)
            with zipfile.ZipFile(os.path.join(tmp, primary["filename"]), 'r') as z:
                z.extractall(tmp)
            idx_path = os.path.join(tmp, "modrinth.index.json")
            if not os.path.exists(idx_path):
                return None, "Нет index.json"
            with open(idx_path, encoding="utf-8") as f:
                idx = json.load(f)
            deps = idx.get("dependencies", {})
            mc_ver = deps.get("minecraft", "unknown")
            loader = "vanilla"
            for k in deps:
                if k in ("fabric-loader", "quilt-loader"):
                    loader = k.replace("-loader", "")
                elif k == "forge":
                    loader = "forge"
            name = idx.get("name", "modpack").strip()
            for entry in idx.get("files", []):
                path = entry.get("path", "")
                downloads = entry.get("downloads", [])
                if path and downloads:
                    target = os.path.normpath(os.path.join(mc_dir, path))
                    if target.startswith(os.path.normpath(mc_dir) + os.sep):
                        os.makedirs(os.path.dirname(target), exist_ok=True)
                        if not os.path.exists(target):
                            try:
                                ApiClient.download_file(downloads[0], target)
                            except Exception:
                                pass
            for odir in ("overrides", "client-overrides"):
                sdir = os.path.join(tmp, odir)
                if os.path.exists(sdir):
                    for root, dirs, files in os.walk(sdir):
                        for fn in files:
                            src = os.path.join(root, fn)
                            dst = os.path.join(mc_dir, os.path.relpath(root, sdir), fn)
                            os.makedirs(os.path.dirname(dst), exist_ok=True)
                            shutil.copy2(src, dst)
            if callback:
                callback(100)
            return name, {"mc_version": mc_ver, "loader": loader, "_source": "modrinth"}
        except Exception as e:
            return None, str(e)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def _install_curseforge(self, version_data, mc_dir, callback=None):
        dl_url = version_data.get("downloadUrl", "")
        if not dl_url:
            try:
                r = requests.get(
                    f"https://api.curseforge.com/v1/mods/{version_data['modId']}/files/{version_data['id']}/download-url",
                    headers={"x-api-key": AppConfig.get_cf_api_key(), "Accept": "application/json"}, timeout=15)
                dl_url = r.json().get("data", "")
            except Exception:
                pass
        if not dl_url:
            return None, "Нет ссылки"
        tmp = tempfile.mkdtemp(prefix="cfpack-")
        try:
            zip_path = os.path.join(tmp, "pack.zip")
            ApiClient.download_file(dl_url, zip_path, callback)
            with zipfile.ZipFile(zip_path, 'r') as z:
                z.extractall(tmp)
            manifest_path = os.path.join(tmp, "manifest.json")
            installed = []
            if os.path.exists(manifest_path):
                with open(manifest_path, encoding="utf-8") as f:
                    manifest = json.load(f)
                mc_ver = manifest.get("minecraft", {}).get("version", "unknown")
                loader = "forge"
                for entry in manifest.get("files", []):
                    project_id = entry.get("projectID", 0)
                    file_id = entry.get("fileID", 0)
                    fpath = entry.get("filePathOverride", "")
                    if not fpath:
                        continue
                    try:
                        r = requests.get(
                            f"https://api.curseforge.com/v1/mods/{project_id}/files/{file_id}/download-url",
                            headers={"x-api-key": AppConfig.get_cf_api_key(),
                                     "Accept": "application/json"}, timeout=15)
                        furl = r.json().get("data", "")
                        if furl:
                            target = os.path.normpath(os.path.join(mc_dir, fpath))
                            if target.startswith(os.path.normpath(mc_dir) + os.sep):
                                os.makedirs(os.path.dirname(target), exist_ok=True)
                                ApiClient.download_file(furl, target)
                                installed.append(target)
                    except Exception:
                        pass
            else:
                mc_ver = "unknown"
                loader = "vanilla"
                for root, dirs, files in os.walk(tmp):
                    for fn in files:
                        if fn.endswith(".jar"):
                            dst = os.path.join(mc_dir, os.path.relpath(root, tmp), fn)
                            os.makedirs(os.path.dirname(dst), exist_ok=True)
                            shutil.copy2(os.path.join(root, fn), dst)
            if callback:
                callback(100)
            return version_data.get("name", "cf-pack"), {"mc_version": mc_ver, "loader": loader, "_source": "curseforge"}
        except Exception as e:
            return None, str(e)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def create_config(self, pack_folder, source, version_id, mc_versions, loaders):
        os.makedirs(pack_folder, exist_ok=True)
        config = {"type": f"{source}_modpack", "source": source, "version_id": version_id,
                  "mc_versions": [mc_versions] if isinstance(mc_versions, str) else mc_versions,
                  "loaders": [loaders] if isinstance(loaders, str) else loaders,
                  "install_path": pack_folder,
                  "installed_at": datetime.datetime.now().isoformat()}
        with open(os.path.join(pack_folder, "superlauncher_config.json"), "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
