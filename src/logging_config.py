"""Logging-Konfiguration für das Projekt."""

import logging
from pathlib import Path


def setup_logging(log_file: Path) -> None:
    """
    Richtet das Logging ein, um in die angegebene Logdatei zu schreiben.

    Args:
        log_file: Pfad zur Logdatei.
    """
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        force=True
    )


def log_analysis_event(event_type: str, details: dict, project_root: Path) -> None:
    """
    Protokolliert Analyseereignisse für Nachvollziehbarkeit.

    Wird verwendet, um wichtige Schritte in der Analyse zu loggen,
    z.B. Export von JSON-Ergebnissen oder Generierung von Berichten.

    Args:
        event_type: Typ des Ereignisses (z.B. "json_export", "report_generation")
        details: Zusätzliche Details als Dict
        project_root: Projektverzeichnis für Kontext
    """
    logger = logging.getLogger("bauwerksdoku_analyzer")
    
    message = f"[{event_type}] Projekt: {project_root} | Details: {details}"
    logger.info(message)