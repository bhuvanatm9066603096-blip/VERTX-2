import logging
import os
from typing import Any

# Configure a module‑level logger
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
LOGGER.addHandler(handler)

def sanitize_path(path: str) -> str:
    """Return a safe absolute path, preventing directory traversal.
    Raises ValueError if the resulting path is outside the project root.
    """
    project_root = os.path.abspath(os.path.join(__file__, '..', '..'))
    abs_path = os.path.abspath(path)
    if not abs_path.startswith(project_root):
        raise ValueError('Attempted path escape outside project root')
    return abs_path

def safe_open(file_path: str, mode: str = 'r', encoding: str = 'utf-8'):
    """Open a file safely after sanitising the path.
    Logs errors and re‑raises.
    """
    safe_path = sanitize_path(file_path)
    try:
        return open(safe_path, mode, encoding=encoding)
    except Exception as exc:
        LOGGER.error('Failed to open file %s: %s', safe_path, exc)
        raise

def safe_json_load(file_path: str) -> Any:
    """Load JSON from a file using safe_open.
    Returns the parsed object or raises.
    """
    import json
    with safe_open(file_path, 'r') as fp:
        return json.load(fp)
