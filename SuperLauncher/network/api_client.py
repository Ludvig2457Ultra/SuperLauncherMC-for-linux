import requests
import threading
from typing import Callable, Optional

class ApiClient:
    """Async HTTP client with callbacks"""

    def get(self, url: str, callback: Callable = None, error_callback: Callable = None,
            headers: dict = None, timeout: int = 15, **params):
        def task():
            try:
                h = headers or {"User-Agent": "SuperLauncher/2.0"}
                if params:
                    resp = requests.get(url, params=params, headers=h, timeout=timeout)
                else:
                    resp = requests.get(url, headers=h, timeout=timeout)
                resp.raise_for_status()
                if callback:
                    callback(resp.json())
            except Exception as e:
                if error_callback:
                    error_callback(str(e))
        threading.Thread(target=task, daemon=True).start()

    def get_raw(self, url: str, callback: Callable = None, error_callback: Callable = None,
                headers: dict = None, timeout: int = 15):
        def task():
            try:
                h = headers or {"User-Agent": "SuperLauncher/2.0"}
                resp = requests.get(url, headers=h, timeout=timeout)
                resp.raise_for_status()
                if callback:
                    callback(resp.content)
            except Exception as e:
                if error_callback:
                    error_callback(str(e))
        threading.Thread(target=task, daemon=True).start()

    def post(self, url: str, data: dict, callback: Callable = None, error_callback: Callable = None,
             headers: dict = None, timeout: int = 15):
        def task():
            try:
                h = headers or {"User-Agent": "SuperLauncher/2.0", "Content-Type": "application/json"}
                resp = requests.post(url, json=data, headers=h, timeout=timeout)
                resp.raise_for_status()
                if callback:
                    callback(resp.json())
            except Exception as e:
                if error_callback:
                    error_callback(str(e))
        threading.Thread(target=task, daemon=True).start()

    @staticmethod
    def download_file(url: str, save_path: str, progress_callback: Callable = None):
        resp = requests.get(url, stream=True, timeout=120)
        resp.raise_for_status()
        total = int(resp.headers.get("content-length", 0))
        written = 0
        with open(save_path, "wb") as f:
            for chunk in resp.iter_content(8192):
                if chunk:
                    f.write(chunk)
                    written += len(chunk)
                    if progress_callback and total > 0:
                        progress_callback(int(written * 100 / total))
        if progress_callback:
            progress_callback(100)
