import sys
import os
import io

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from PyQt6.QtWidgets import QApplication
from .ui.main_window import MainWindow
from .core.constants import DATA_DIR

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("SuperLauncher")
    app.setApplicationVersion("2.0.0")

    for d in ["assets/skins", "assets/icons", "user_data", "servers", "builds", "mods_cache", "logs", "temp"]:
        os.makedirs(os.path.join(DATA_DIR, d), exist_ok=True)

    print("SuperLauncher 2.0 - Modular Edition")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
