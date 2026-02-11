from pathlib import Path
from typing import List, Dict
import os
from src.paths import is_path_allowed


def scan_project(project_path: Path, allowed_roots: List[Path]) -> List[Dict]:
    """
    Scannt rekursiv ein Projektverzeichnis und erstellt eine Liste aller Dateien mit Metadaten.

    Diese Funktion sammelt alle Dateien im Projekt, prüft Pfadsicherheit und
    liefert Metadaten wie Größe und Änderungsdatum.

    :param project_path: Zu scannender Projektpfad
    :param allowed_roots: Erlaubte Root-Pfade für Sicherheit
    :return: Liste von Datei-Dicts mit Metadaten
    """
    files = []
    
    for root, dirs, filenames in os.walk(project_path):
        root_path = Path(root)
        
        # Prüfe Pfadsicherheit für das Verzeichnis
        if not is_path_allowed(root_path, allowed_roots):
            continue
            
        for filename in filenames:
            file_path = root_path / filename
            
            # Zusätzliche Sicherheit: Prüfe jeden Dateipfad
            if not is_path_allowed(file_path, allowed_roots):
                continue
                
            try:
                stat = file_path.stat()
                files.append({
                    'path': str(file_path),
                    'size': stat.st_size,
                    'mtime': stat.st_mtime,
                    'relative_path': str(file_path.relative_to(project_path))
                })
            except (OSError, ValueError):
                # Überspringe Dateien, die nicht gelesen werden können
                continue
                
    return files