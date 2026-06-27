import os
import subprocess
import threading
import json
from ..core.constants import SERVERS_FILE

class ServerManager:
    def __init__(self):
        self.process = None
        self._running = False

    def load_servers(self):
        try:
            with open(SERVERS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def save_servers(self, servers):
        with open(SERVERS_FILE, "w", encoding="utf-8") as f:
            json.dump(servers, f, indent=2)

    def start(self, server_path, ram_gb=4, java_args=""):
        if self._running:
            return
        bat_path = os.path.join(server_path, "start.bat")
        os.makedirs(server_path, exist_ok=True)
        if not os.path.exists(bat_path):
            with open(bat_path, "w", encoding="utf-8") as f:
                f.write(f"@echo off\njava -Xmx{ram_gb}G -Xms{ram_gb}G {java_args} -jar server.jar nogui\n")

        def run():
            self._running = True
            try:
                self.process = subprocess.Popen(
                    bat_path, cwd=server_path, shell=True,
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    text=True, encoding="utf-8", errors="replace")
                self.process.wait()
            finally:
                self._running = False

        threading.Thread(target=run, daemon=True).start()

    def stop(self):
        if self.process and self.process.poll() is None:
            try:
                self.process.stdin.write("stop\n")
                self.process.stdin.flush()
                self.process.wait(timeout=10)
            except Exception:
                try:
                    self.process.kill()
                except Exception:
                    pass

    def send_command(self, cmd):
        if self.process and self.process.poll() is None:
            try:
                self.process.stdin.write(cmd + "\n")
                self.process.stdin.flush()
            except Exception:
                pass

    def create(self, name, port=25565, version="1.20.4", core="paper"):
        server_path = os.path.join("servers", name)
        os.makedirs(server_path, exist_ok=True)
        return server_path
