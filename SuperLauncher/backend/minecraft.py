import os
import subprocess
import threading
from ..core.platform import PlatformSupport

class MinecraftLauncher:
    def __init__(self):
        self.process = None
        self._running = False

    def is_running(self):
        return self._running

    def launch(self, version, username, java_path="", min_ram=1024, max_ram=4096,
               jvm_args="", callback=None, error_callback=None):
        mc_dir = PlatformSupport.get_minecraft_path()
        versions_dir = os.path.join(mc_dir, "versions", version)
        jar_path = os.path.join(versions_dir, f"{version}.jar")

        if not os.path.exists(jar_path):
            if error_callback:
                error_callback(f"Версия {version} не установлена")
            return

        java = java_path or "java"
        args = [java, f"-Xmx{max_ram}M", f"-Xms{min_ram}M"]
        if jvm_args:
            args.extend(jvm_args.split())
        args.extend(["-jar", jar_path, "--username", username, "--version", version])

        def run():
            self._running = True
            try:
                self.process = subprocess.Popen(
                    args, cwd=mc_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    text=True, encoding="utf-8", errors="replace")
                for line in iter(self.process.stdout.readline, ""):
                    if callback:
                        callback(line.rstrip())
                self.process.wait()
            except Exception as e:
                if error_callback:
                    error_callback(str(e))
            finally:
                self._running = False
                self.process = None

        threading.Thread(target=run, daemon=True).start()

    def kill(self):
        if self.process and self.process.poll() is None:
            try:
                self.process.kill()
            except Exception:
                pass
