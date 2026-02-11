# Placeholder für HTML Report

from pathlib import Path
from string import Template
import json


def generate_html_report(json_data: dict, template_path: Path) -> str:
    """
    Generiert einen HTML-Bericht aus einem Template und Analyseergebnissen.

    Lädt ein HTML-Template und füllt es mit Daten aus dem JSON-Objekt.
    Ermöglicht die Grundlage für Phase 7 (vollständiger HTML-Bericht).

    Args:
        json_data: Datenobjekt aus export_analysis_results()
        template_path: Pfad zum HTML-Template

    Returns:
        HTML-String mit gefülltem Template

    Raises:
        FileNotFoundError: Wenn Template nicht gefunden wird
    """
    if not template_path.exists():
        raise FileNotFoundError(f"Template nicht gefunden: {template_path}")
    
    # Template laden
    template_content = template_path.read_text(encoding="utf-8")
    template = Template(template_content)
    
    # Daten für Substitution vorbereiten
    substitution_data = {}
    
    # Metadata
    substitution_data["timestamp"] = json_data.get("metadata", {}).get("timestamp", "")
    substitution_data["project_root"] = json_data.get("metadata", {}).get("project_root", "")
    
    # Summary
    summary = json_data.get("summary", {})
    substitution_data["fehlend_count"] = summary.get("fehlend", 0)
    substitution_data["zusatz_korrekt_count"] = summary.get("zusätzlich_korrekt", 0)
    substitution_data["zusatz_falsch_count"] = summary.get("zusätzlich_falsch", 0)
    
    # Details als Listen formatieren
    details = json_data.get("details", {})
    substitution_data["fehlend_list"] = "\n".join(f"<li>{item}</li>" for item in details.get("fehlend", []))
    substitution_data["zusatz_korrekt_list"] = "\n".join(f"<li>{item}</li>" for item in details.get("zusätzlich_korrekt", []))
    substitution_data["zusatz_falsch_list"] = "\n".join(f"<li>{item}</li>" for item in details.get("zusätzlich_falsch", []))
    
    # Template füllen
    return template.safe_substitute(substitution_data)