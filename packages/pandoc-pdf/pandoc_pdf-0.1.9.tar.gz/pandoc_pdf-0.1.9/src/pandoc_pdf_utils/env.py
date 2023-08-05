from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "pandoc_pdf"
DEFAULT_CONFIG_DIR = Path(__file__).parent / "default_config"
CACHE_DIR = Path(__file__).parent / "cache"
