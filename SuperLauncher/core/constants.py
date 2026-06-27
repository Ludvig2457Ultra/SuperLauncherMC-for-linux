import os

CURRENT_VERSION = "v2.0.0_2026"
MODRINTH_API = "https://api.modrinth.com/v2"
CURSEFORGE_API = "https://api.curseforge.com/v1"

DATA_DIR = os.path.join(os.path.expanduser("~"), ".local", "share", "SuperLauncher")

CONFIG_FILE = os.path.join(DATA_DIR, "settings.json")
ACCOUNTS_FILE = os.path.join(DATA_DIR, "accounts.json")
LICENSES_FILE = os.path.join(DATA_DIR, "licenses.json")
SERVERS_FILE = os.path.join(DATA_DIR, "servers_list.json")

APP_NAME = "SuperLauncher"
ORG_NAME = "SuperLauncher"
