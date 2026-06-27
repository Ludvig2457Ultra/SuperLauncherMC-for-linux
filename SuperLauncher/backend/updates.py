import threading
import requests
from packaging import version as packaging_version

class UpdateChecker:
    def __init__(self):
        self.releases = []
        self.latest = None

    def check(self, current_version, callback=None):
        def task():
            try:
                url = "https://api.github.com/repos/Ludvig2457Ultra/SuperLauncherMC/releases?per_page=10"
                resp = requests.get(url, headers={"Accept": "application/vnd.github.v3+json"}, timeout=15)
                if resp.status_code != 200:
                    return
                data = resp.json()
                current = packaging_version.parse(current_version)
                for r in data:
                    try:
                        v = packaging_version.parse(r.get("tag_name", ""))
                    except Exception:
                        continue
                    if v > current:
                        assets = r.get("assets", [])
                        dl_url = ""
                        for a in assets:
                            if a.get("name", "").endswith((".exe", ".py")):
                                dl_url = a.get("browser_download_url", "")
                                break
                        self.latest = {
                            "tag": r["tag_name"], "name": r.get("name", ""),
                            "body": r.get("body", ""), "date": r.get("published_at", "")[:10],
                            "dl_url": dl_url, "prerelease": r.get("prerelease", False)
                        }
                        if callback:
                            callback(self.latest)
                        return
                if callback:
                    callback(None)
            except Exception:
                pass

        threading.Thread(target=task, daemon=True).start()
