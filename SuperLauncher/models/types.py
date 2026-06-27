from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Mod:
    id: str
    name: str
    description: str = ""
    downloads: int = 0
    icon_url: str = ""
    author: str = "Unknown"
    source: str = "modrinth"
    versions: list = field(default_factory=list)
    loaders: list = field(default_factory=list)

@dataclass
class Modpack:
    id: str
    name: str
    description: str = ""
    downloads: int = 0
    icon_url: str = ""
    author: str = "Unknown"
    source: str = "modrinth"
    mc_version: str = ""
    loader: str = ""

@dataclass
class Server:
    name: str
    ip: str = ""
    managed: bool = False
    ram_gb: int = 4
    version: str = ""
    core: str = ""
    dir_path: str = ""

@dataclass
class User:
    user_id: str = ""
    username: str = "Guest"
    email: str = ""
    license_tier: str = "free"
    level: int = 1
    xp: int = 0
    skins: list = field(default_factory=lambda: ["default"])
