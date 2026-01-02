from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    api_key: str
    units: str = "metric"   # metric | imperial | standard
    lang: str = "en"
    timeout: float = 8.0


def _read_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists() or not path.is_file():
        return {}
    raw = path.read_text(encoding="utf-8")
    data = yaml.safe_load(raw)
    return data if isinstance(data, dict) else {}


def load_settings(config_path: Optional[Path] = None) -> Settings:
    """
    Priority:
      0) .env (loaded into environment if present)
      1) env OPENWEATHER_API_KEY (and optional OPENWEATHER_* defaults)
      2) config file: provided path
      3) ./config.yaml
      4) ~/.config/openweather-cli/config.yaml
    """

    # 0) Load .env if present (project root by default)
    # This will not overwrite already-set environment variables.
    load_dotenv()

    # Helper: read optional defaults from env (if set)
    env_key = os.getenv("OPENWEATHER_API_KEY")
    env_units = os.getenv("OPENWEATHER_UNITS")
    env_lang = os.getenv("OPENWEATHER_LANG")
    env_timeout = os.getenv("OPENWEATHER_TIMEOUT")

    # Collect config candidates
    candidates: list[Path] = []
    if config_path:
        candidates.append(config_path)
    candidates.append(Path("config.yaml"))
    candidates.append(Path.home() / ".config" / "openweather-cli" / "config.yaml")

    merged: Dict[str, Any] = {}
    for p in candidates:
        merged.update(_read_yaml(p))

    # API key: env wins, else yaml
    api_key = (env_key or str(merged.get("api_key", ""))).strip()
    if not api_key:
        raise ValueError(
            "Missing API key. Set OPENWEATHER_API_KEY (or .env) or provide config.yaml with 'api_key: ...'."
        )

    # units/lang/timeout:
    # - env overrides yaml if set
    units = (env_units or str(merged.get("units", "metric"))).strip()
    lang = (env_lang or str(merged.get("language", merged.get("lang", "en")))).strip()

    timeout_raw = env_timeout if env_timeout is not None else merged.get("timeout", 8.0)
    try:
        timeout = float(timeout_raw)
    except (TypeError, ValueError):
        raise ValueError("Invalid timeout. Use a number (e.g. 8 or 8.0).")

    if units not in {"metric", "imperial", "standard"}:
        raise ValueError("Invalid units. Use: metric, imperial, or standard.")

    return Settings(api_key=api_key, units=units, lang=lang, timeout=timeout)