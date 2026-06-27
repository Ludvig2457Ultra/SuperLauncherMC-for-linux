import threading
import time

class DiscordRPC:
    def __init__(self):
        self.rpc = None
        self.connected = False
        self._running = False
        self._thread = None

    def connect(self):
        try:
            from pypresence import Presence
            self.rpc = Presence("1405145554027155456")
            self.rpc.connect()
            self.connected = True
            self._running = True
            self._thread = threading.Thread(target=self._loop, daemon=True)
            self._thread.start()
        except Exception:
            self.connected = False

    def _loop(self):
        while self._running and self.connected:
            try:
                self.rpc.update(details="SuperLauncher 2.0", state="В лаунчере",
                                large_image="superlauncher", start=time.time())
            except Exception:
                pass
            time.sleep(15)

    def disconnect(self):
        self._running = False
        if self.rpc and self.connected:
            try:
                self.rpc.close()
            except Exception:
                pass
        self.connected = False

    def set_in_game(self, version):
        if self.connected and self.rpc:
            try:
                self.rpc.update(details=f"Играет в Minecraft {version}",
                                state="SuperLauncher", large_image="minecraft", start=time.time())
            except Exception:
                pass

    def set_idle(self):
        if self.connected and self.rpc:
            try:
                self.rpc.update(details="SuperLauncher 2.0", state="В простое",
                                large_image="superlauncher", start=time.time())
            except Exception:
                pass
