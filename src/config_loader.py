"""Konfigurationsladefunktion."""

import yaml
from pathlib import Path


def load_config(config_file: Path) -> dict:
    """
    Lädt die Konfiguration aus einer YAML-Datei.

    Args:
        config_file: Pfad zur Konfigurationsdatei.

    Returns:
        Dictionary mit Konfigurationsdaten.
    """
    with open(config_file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def load_gui_config(config_file: Path) -> dict:
    """
    Lädt GUI-spezifische Konfigurationen für JSON-Integration und Interaktivität.

    Args:
        config_file: Pfad zur Konfigurationsdatei.

    Returns:
        Dictionary mit GUI-Konfiguration.
    """
    full_config = load_config(config_file)
    return full_config.get("gui", {})