import yaml
import os
import shutil
from pathlib import Path
from typing import Dict, List
from ..l8n import Strings

class Settings:
    def __init__(self):
        # Paths
        self.config_dir = Path.home() / ".config" / "sortomatic"
        self.settings_file = self.config_dir / "settings.yaml"
        self.filetypes_file = self.config_dir / "filetypes.yaml"
        self.cache_dir = Path.home() / ".cache" / "sortomatic"
        
        # Internal defaults (used if files are missing or corrupted)
        self.categories: Dict[str, List[str]] = {
            Strings.CAT_IMAGE: ["jpg", "jpeg", "png", "gif", "bmp", "tiff", "heic", "svg"],
            Strings.CAT_VIDEO: ["mp4", "mkv", "avi", "mov", "wmv", "flv", "webm"],
            Strings.CAT_DOCUMENT: ["pdf", "doc", "docx", "txt", "md", "xls", "xlsx", "ppt", "pptx"],
            Strings.CAT_MUSIC: ["mp3", "wav", "flac", "aac", "ogg", "m4a"],
            Strings.CAT_ARCHIVE: ["zip", "rar", "7z", "tar", "gz"],
            Strings.CAT_CODE: ["py", "js", "html", "css", "json", "xml", "c", "cpp", "h", "java", "go", "rs", "sh", "bat", "ps1"],
            Strings.CAT_3D: ["obj", "stl", "fbx", "blend", "dae", "3ds", "step", "stp"],
            Strings.CAT_SOFTWARE: ["exe", "msi", "app", "deb", "rpm", "dmg", "iso", "bin"]
        }
        self.ignore_patterns: List[str] = [".git", "__pycache__", ".DS_Store", "node_modules", ".venv", ".sortomatic"]
        self.atomic_markers: List[str] = [".git", ".hg", "Makefile", "package.json", "requirements.txt", "venv"]
        self.batch_size: int = 1000
        self.reset_db: bool = False
        
        # New: Externalized magic numbers
        self.hashing_chunk_size: int = 1024 * 1024  # 1MB
        self.fast_hash_size: int = 4 * 1024        # 4KB
        self.categorization_timeout: float = 1.0    # 1 second
        self.hashing_timeout: float = 60.0          # 60 seconds (generous for large files)
        
        cpu_count = os.cpu_count() or 4
        self.max_workers = max(1, cpu_count // 2)

        # GUI Settings
        self.gui_port: int = 8080
        self.gui_theme: str = "solarized"
        self.gui_dark_mode: bool = True
        
        # UI Order and Colors (Source of Truth)
        self.category_order: List[str] = [
            Strings.CAT_OTHER,
            Strings.CAT_DOCUMENT,
            Strings.CAT_IMAGE,
            Strings.CAT_ARCHIVE,
            Strings.CAT_MUSIC,
            Strings.CAT_VIDEO,
            Strings.CAT_3D,
            Strings.CAT_SOFTWARE,
            Strings.CAT_CODE
        ]
        
        self.category_colors: Dict[str, str] = {
            Strings.CAT_OTHER: "grey",
            Strings.CAT_DOCUMENT: "cyan",
            Strings.CAT_IMAGE: "green",
            Strings.CAT_ARCHIVE: "yellow",
            Strings.CAT_MUSIC: "orange",
            Strings.CAT_VIDEO: "red",
            Strings.CAT_3D: "magenta",
            Strings.CAT_SOFTWARE: "purple",
            Strings.CAT_CODE: "blue"
        }

        # Initialize and Load
        self._ensure_config_exists()
        self.load()

    def _ensure_config_exists(self):
        """Copies default config files to user directory if they don't exist."""
        if not self.config_dir.exists():
            self.config_dir.mkdir(parents=True, exist_ok=True)

        if not self.cache_dir.exists():
            self.cache_dir.mkdir(parents=True, exist_ok=True)

        package_config_dir = Path(__file__).parent.parent / "config"
        
        defaults = {
            "settings.yaml": self.settings_file,
            "filetypes.yaml": self.filetypes_file
        }

        for filename, dest_path in defaults.items():
            if not dest_path.exists():
                src_path = package_config_dir / filename
                if src_path.exists():
                    shutil.copy(src_path, dest_path)

    def load(self, config_dir: Path | None = None):
        """Loads configuration from the user's YAML files."""
        if config_dir:
            self.config_dir = Path(config_dir)
            self.settings_file = self.config_dir / "settings.yaml"
            self.filetypes_file = self.config_dir / "filetypes.yaml"
            self._ensure_config_exists()

        # 1. Load Settings
        if self.settings_file.exists():
            with open(self.settings_file, "r") as f:
                data = yaml.safe_load(f) or {}
                if data.get("max_workers") is not None:
                    self.max_workers = data["max_workers"]
                if (val := data.get("batch_size")) is not None:
                    self.batch_size = val
                if (val := data.get("reset_db")) is not None:
                    self.reset_db = val
                if (val := data.get("hashing_chunk_size")) is not None:
                    self.hashing_chunk_size = val
                if (val := data.get("fast_hash_size")) is not None:
                    self.fast_hash_size = val
                if (val := data.get("categorization_timeout")) is not None:
                    self.categorization_timeout = val
                if (val := data.get("hashing_timeout")) is not None:
                    self.hashing_timeout = val
                if (val := data.get("gui_port")) is not None:
                    self.gui_port = val
                if (val := data.get("gui_theme")) is not None:
                    self.gui_theme = val
                if (val := data.get("gui_dark_mode")) is not None:
                    self.gui_dark_mode = val
                if (val := data.get("category_order")) is not None:
                    self.category_order = val
                if (val := data.get("category_colors")) is not None:
                    self.category_colors = val
                if data.get("cache_dir"):
                    self.cache_dir = Path(data["cache_dir"]).expanduser()

        # 2. Load Filetypes
        if self.filetypes_file.exists():
            with open(self.filetypes_file, "r") as f:
                data = yaml.safe_load(f) or {}
                self.categories = data.get("categories", self.categories)
                self.ignore_patterns = data.get("ignore", self.ignore_patterns)
                self.atomic_markers = data.get("atomic_markers", self.atomic_markers)

    def get_category(self, extension: str) -> str:
        """Determine category based on file extension."""
        ext = extension.lower().lstrip(".")
        for category, extensions in self.categories.items():
            if ext in extensions:
                return category
        return Strings.CAT_OTHER

# Global singleton
settings = Settings()