"""
Strukturprüfung für Bauwerksdokumentation.

Dieses Modul implementiert den Soll/Ist-Vergleich zwischen der erwarteten
Projektstruktur (aus Excel) und der tatsächlichen Verzeichnisstruktur.
"""

from pathlib import Path
from typing import Dict, List, Any, Set
import os
from src.logging_config import log_analysis_event


def compare_structures(soll_structure: List[Dict[str, Any]], ist_files: List[Dict[str, Any]], project_root: Path) -> Dict[str, List[Dict[str, Any]]]:
    """
    Vergleicht die SOLL-Struktur mit der IST-Struktur und kategorisiert Abweichungen.

    Basierend auf DOMAIN_RULES.md werden drei Kategorien von Abweichungen identifiziert:
    - fehlend: In SOLL definiert, aber nicht in IST vorhanden
    - zusätzlich_korrekt: In IST vorhanden und unter SOLL-Pfaden platziert
    - zusätzlich_falsch: In IST vorhanden, aber außerhalb SOLL-Struktur platziert

    Args:
        soll_structure: Liste der erwarteten Strukturelemente aus Excel
        ist_files: Liste der tatsächlich gefundenen Dateien aus Scanner
        project_root: Wurzelverzeichnis des Projekts

    Returns:
        Dict mit den drei Kategorien von Abweichungen
    """
    # Erstelle Sets für effiziente Suche
    soll_paths = _extract_soll_paths(soll_structure)
    ist_paths = _extract_ist_paths(ist_files, project_root)
    ist_file_paths = {str(Path(f["path"]).relative_to(project_root)) for f in ist_files}

    # Kategorisiere Abweichungen
    fehlend = _find_missing(soll_structure, ist_paths)
    zusätzlich_korrekt, zusätzlich_falsch = _find_extra(ist_paths, soll_paths, ist_file_paths, soll_structure)
    # Tiefe-Verstöße entfernt - nicht in DOMAIN_RULES definiert

    return {
        "fehlend": fehlend,
        "zusätzlich_korrekt": zusätzlich_korrekt,
        "zusätzlich_falsch": zusätzlich_falsch,
        # "tiefe_verstoss": tiefe_verstoss,  # Entfernt - nicht in DOMAIN_RULES
        "ist_paths": ist_paths,
        "ist_file_paths": ist_file_paths
    }


def _extract_soll_paths(soll_structure: List[Dict[str, Any]]) -> Set[str]:
    """
    Extrahiert alle erwarteten Pfade aus der SOLL-Struktur.

    Args:
        soll_structure: Liste der erwarteten Strukturelemente

    Returns:
        Set aller erwarteten relativen Pfade
    """
    paths = set()

    for item in soll_structure:
        # Erstelle Pfad aus Nummer (z.B. "1.01" -> "1/1.01")
        number = item["number"]
        path_parts = []

        # Baue hierarchischen Pfad auf
        parts = number.split(".")
        current_path = ""

        for i, part in enumerate(parts):
            if i == 0:
                current_path = part
            else:
                current_path = f"{current_path}/{'.'.join(parts[:i+1])}"
            path_parts.append(current_path)

        # Füge alle Pfadebenen hinzu
        for path in path_parts:
            paths.add(path)

    return paths


def _extract_ist_paths(ist_files: List[Dict[str, Any]], project_root: Path) -> Set[str]:
    """
    Extrahiert alle tatsächlichen Pfade aus den gescannten Dateien.

    Args:
        ist_files: Liste der gescannten Dateien
        project_root: Wurzelverzeichnis des Projekts

    Returns:
        Set aller relativen Pfade (Ordner und Dateien)
    """
    paths = set()

    for file_info in ist_files:
        # Extrahiere relativen Pfad
        full_path = Path(file_info["path"])
        try:
            relative_path = full_path.relative_to(project_root)
            # Füge sowohl Datei- als auch alle übergeordneten Ordner-Pfade hinzu
            for parent in relative_path.parents:
                if parent != Path("."):
                    paths.add(str(parent))
            paths.add(str(relative_path))
        except ValueError:
            # Pfad ist nicht unter project_root
            continue

    return paths


def _find_missing(soll_structure: List[Dict[str, Any]], ist_paths: Set[str]) -> List[Dict[str, Any]]:
    """
    Findet fehlende Elemente (in SOLL definiert, aber nicht in IST vorhanden).

    Args:
        soll_structure: Liste der erwarteten Strukturelemente
        ist_paths: Set der tatsächlich vorhandenen Pfade

    Returns:
        Liste der fehlenden Elemente
    """
    missing = []

    for item in soll_structure:
        if item.get("required", False):
            # Für Ordner: Prüfe ob Ordner-Pfad existiert
            if item["type"] == "folder":
                expected_path = _number_to_path(item["number"])
                if expected_path not in ist_paths:
                    missing.append({
                        "path": expected_path,
                        "type": "folder",
                        "name": item["name"],
                        "number": item["number"]
                    })
            # Für Dokumente: Prüfe ob Dokument existiert (vereinfacht - könnte erweitert werden)
            elif item["type"] == "document":
                # Hier könnte eine genauere Prüfung erfolgen
                # Vereinfacht: nehme an, dass Dokumente unter ihrem Ordner liegen
                pass

    return missing


def _find_extra(ist_paths: Set[str], soll_paths: Set[str], ist_file_paths: Set[str], soll_structure: List[Dict[str, Any]]) -> tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Findet zusätzliche Elemente und kategorisiert sie.

    Da wir uns nur um die Ordnerstruktur kümmern, werden Dateien ignoriert.
    Zusätzliche Ordner werden nur als korrekt eingestuft, wenn sie unter SOLL-Pfaden
    liegen UND korrekt nummeriert sind.

    Args:
        ist_paths: Set der tatsächlich vorhandenen Pfade
        soll_paths: Set der erwarteten Pfade
        ist_file_paths: Set der Datei-Pfade (um Ordner von Dateien zu unterscheiden)
        soll_structure: Liste der SOLL-Strukturelemente zur Validierung

    Returns:
        Tuple aus (zusätzlich_korrekt, zusätzlich_falsch)
    """
    zusätzlich_korrekt = []
    zusätzlich_falsch = []

    # Bestimme Strukturtyp basierend auf SOLL-Nummern
    is_12er = any('.' in item['number'] for item in soll_structure)

    for ist_path in ist_paths:
        # Ignoriere Dateien - wir kümmern uns nur um Ordnerstruktur
        if ist_path in ist_file_paths:
            continue

        if ist_path not in soll_paths:
            # Pfad ist zusätzlich - prüfe ob er unter einem SOLL-Pfad liegt
            # Normalisiere Pfad-Trenner für Cross-Plattform
            normalized_ist = ist_path.replace(os.sep, '/')
            is_under_soll = False
            is_numbering_valid = False

            for soll_path in soll_paths:
                normalized_soll = soll_path.replace(os.sep, '/')
                # Prüfe ob IST-Pfad unter SOLL-Pfad liegt oder SOLL-Pfad ist
                if normalized_ist.startswith(normalized_soll + '/') or normalized_ist == normalized_soll:
                    is_under_soll = True
                    # Zusätzlich: Prüfe Nummerierung
                    if is_12er:
                        is_numbering_valid = _is_path_valid_additional_folder(ist_path, soll_structure)
                    else:  # KBOB
                        is_numbering_valid = _is_path_valid_additional_folder_kbob(ist_path, soll_structure)
                    break

            if is_under_soll and is_numbering_valid:
                zusätzlich_korrekt.append({
                    "path": ist_path,
                    "type": "folder"
                })
            else:
                zusätzlich_falsch.append({
                    "path": ist_path,
                    "type": "folder"
                })

    return zusätzlich_korrekt, zusätzlich_falsch


def _number_to_path(number: str) -> str:
    """
    Konvertiert eine Nummer in einen Pfad.

    Beispiele:
    - 12er: "1.01" -> "1/1.01"
    - KBOB: "A01" -> "A/A01", "A01001" -> "A/A01/A01001"

    Args:
        number: Nummer aus der Struktur

    Returns:
        Relativer Pfad
    """
    # Prüfe ob es eine 12er-Nummer ist (enthält Punkte)
    if '.' in number:
        parts = number.split(".")
        # Baue hierarchischen Pfad
        path_parts = []
        for i in range(1, len(parts) + 1):
            path_parts.append(".".join(parts[:i]))
        return "/".join(path_parts)
    else:
        # KBOB-Format: Pfad aus kumulierten Ebenen (skalierbar)
        path_parts = []
        # Ebene 1
        if len(number) >= 1:
            path_parts.append(number[0])
        # Ebene 2
        if len(number) >= 3:
            path_parts.append(number[:3])
        # Ebene 3
        if len(number) >= 6:
            path_parts.append(number[:6])
        # Ebene 4
        if len(number) >= 8:
            path_parts.append(number[:8])
        # Ebene 5
        if len(number) >= 10:
            path_parts.append(number[:10])
        # Ebene 6
        if len(number) >= 12:
            path_parts.append(number[:12])
        # Ebene 7
        if len(number) >= 14:
            path_parts.append(number[:14])
        # Ebene 8
        if len(number) >= 16:
            path_parts.append(number[:16])
        # Ebene 9
        if len(number) >= 18:
            path_parts.append(number[:18])
        # Ebene 10
        if len(number) >= 20:
            path_parts.append(number[:20])
        return "/".join(path_parts)


def _is_valid_additional_folder(folder_name: str, parent_soll_number: str) -> bool:
    """
    Prüft, ob ein zusätzlicher Ordner die korrekte Nummerierungslogik einhält.

    Die Regel: Zusätzliche Ordner müssen die hierarchische Bezeichnung fortführen,
    ab Ebene 4 mit einem zweistelligen Zusatz "01" bis "99".

    Beispiele:
    - parent_soll_number="11.061" -> folder_name="11.06101" ist gültig
    - parent_soll_number="11.06101" -> folder_name="11.0610101" ist gültig
    - parent_soll_number="11.061" -> folder_name="11.0611" ist ungültig (nur eine Ziffer)
    - parent_soll_number="11.061" -> folder_name="11.061100" ist ungültig (mehr als zwei Ziffern)

    Args:
        folder_name: Name des zusätzlichen Ordners (z.B. "11.06101")
        parent_soll_number: Nummer des übergeordneten SOLL-Ordners (z.B. "11.061")

    Returns:
        True wenn die Nummerierung korrekt ist, False sonst
    """
    # Der Ordner muss mit der Parent-Nummer beginnen
    if not folder_name.startswith(parent_soll_number):
        return False

    # Extrahiere die Fortsetzung nach der Parent-Nummer
    continuation = folder_name[len(parent_soll_number):]

    # Die Fortsetzung muss aus genau zwei Ziffern bestehen und zwischen 01 und 99 liegen
    if len(continuation) != 2 or not continuation.isdigit():
        return False

    number = int(continuation)
    return 1 <= number <= 99


def _is_valid_additional_folder_kbob(folder_name: str, parent_soll_number: str) -> bool:
    """
    Prüft, ob ein zusätzlicher Ordner die korrekte KBOB-Nummerierungslogik einhält.

    Die Regel: Zusätzliche Ordner müssen die hierarchische Bezeichnung fortführen,
    mit einem zweistelligen Zusatz "01" bis "99" (gleich wie 12er-Struktur).

    Beispiele:
    - parent_soll_number="O01001" -> folder_name="O0100101" ist gültig
    - parent_soll_number="O0100101" -> folder_name="O010010101" ist gültig
    - parent_soll_number="O01001" -> folder_name="O010011" ist ungültig (nur eine Ziffer)
    - parent_soll_number="O01001" -> folder_name="O01001100" ist ungültig (mehr als zwei Ziffern)

    Args:
        folder_name: Name des zusätzlichen Ordners (z.B. "O0100101")
        parent_soll_number: Nummer des übergeordneten SOLL-Ordners (z.B. "O01001")

    Returns:
        True wenn die Nummerierung korrekt ist, False sonst
    """
    # Der Ordner muss mit der Parent-Nummer beginnen
    if not folder_name.startswith(parent_soll_number):
        return False

    # Extrahiere die Fortsetzung nach der Parent-Nummer
    continuation = folder_name[len(parent_soll_number):]

    # Die Fortsetzung muss aus genau zwei Ziffern bestehen und zwischen 01 und 99 liegen
    if len(continuation) != 2 or not continuation.isdigit():
        return False

    number = int(continuation)
    return 1 <= number <= 99


def _is_path_valid_additional_folder(ist_path: str, soll_structure: List[Dict[str, Any]]) -> bool:
    """
    Prüft, ob ein IST-Pfad ein gültiger zusätzlicher 12er-Ordner ist.

    Args:
        ist_path: Der zu prüfende IST-Pfad
        soll_structure: Liste der SOLL-Strukturelemente

    Returns:
        True wenn es ein gültiger zusätzlicher Ordner ist
    """
    # Normalisiere Pfad
    ist_path_norm = ist_path.replace('\\', '/')
    path = Path(ist_path_norm)
    folder_name = path.name

    # Finde den direkten Eltern-Pfad
    parent_path = str(path.parent).replace('\\', '/')
    if parent_path == ".":
        return False  # Root-Level Ordner können nicht zusätzlich sein

    # Finde den SOLL-Eintrag für den Eltern-Pfad
    parent_soll_number = None
    for item in soll_structure:
        soll_path = _number_to_path(item["number"])
        if soll_path == parent_path:
            parent_soll_number = item["number"]
            break

    if parent_soll_number is None:
        # Parent ist selbst zusätzlich - verwende den Ordner-Namen als parent_soll_number
        parent_path_obj = Path(parent_path)
        parent_soll_number = parent_path_obj.name

    # Prüfe ob der Parent ein Blatt ist (nur von Blättern aus dürfen Unterordner erstellt werden)
    parent_item = None
    for item in soll_structure:
        if item["number"] == parent_soll_number:
            parent_item = item
            break
    
    if parent_item is not None and not _is_leaf(parent_item, soll_structure):
        return False  # Parent ist in SOLL definiert aber kein Blatt

    # Prüfe ob der Ordner-Name eine gültige Fortsetzung ist
    return _is_valid_additional_folder(folder_name, parent_soll_number)


def _is_path_valid_additional_folder_kbob(ist_path: str, soll_structure: List[Dict[str, Any]]) -> bool:
    """
    Prüft, ob ein IST-Pfad ein gültiger zusätzlicher KBOB-Ordner ist.

    Args:
        ist_path: Der zu prüfende IST-Pfad
        soll_structure: Liste der SOLL-Strukturelemente

    Returns:
        True wenn es ein gültiger zusätzlicher Ordner ist
    """
    # Normalisiere Pfad
    ist_path_norm = ist_path.replace('\\', '/')
    path = Path(ist_path_norm)
    folder_name = path.name

    # Finde den direkten Eltern-Pfad
    parent_path = str(path.parent).replace('\\', '/')
    if parent_path == ".":
        return False  # Root-Level Ordner können nicht zusätzlich sein

    # Finde den SOLL-Eintrag für den Eltern-Pfad
    parent_soll_number = None
    for item in soll_structure:
        soll_path = _number_to_path(item["number"])
        if soll_path == parent_path:
            parent_soll_number = item["number"]
            break

    if parent_soll_number is None:
        # Parent ist selbst zusätzlich - verwende den Ordner-Namen als parent_soll_number
        parent_path_obj = Path(parent_path)
        parent_soll_number = parent_path_obj.name

    # Prüfe ob der Parent ein Blatt ist (nur von Blättern aus dürfen Unterordner erstellt werden)
    parent_item = None
    for item in soll_structure:
        if item["number"] == parent_soll_number:
            parent_item = item
            break
    
    if parent_item is not None and not _is_leaf(parent_item, soll_structure):
        return False  # Parent ist in SOLL definiert aber kein Blatt

    # Prüfe ob der Ordner-Name eine gültige Fortsetzung ist
    return _is_valid_additional_folder_kbob(folder_name, parent_soll_number)


def export_analysis_results(analysis_results: Dict[str, List[Dict[str, Any]]], project_root: Path) -> str:
    """
    Erstellt ein standardisiertes JSON-Output für Analyseergebnisse zur Verwendung in GUI und Bericht.

    Das JSON folgt der in COPILOT_SPEC.md definierten Struktur und ermöglicht
    die Datenfluss-Architektur für spätere Phasen (Bericht, GUI).

    Args:
        analysis_results: Ergebnisse aus compare_structures()
        project_root: Wurzelverzeichnis des Projekts

    Returns:
        JSON-String mit standardisierter Struktur
    """
    import json
    from datetime import datetime
    
    # Metadata erstellen
    metadata = {
        "timestamp": datetime.now().isoformat(),
        "project_root": str(project_root),
        "sources": ["structure_check.py"]
    }
    
    # Summary berechnen
    summary = {
        "fehlend": len(analysis_results.get("fehlend", [])),
        "zusätzlich_korrekt": len(analysis_results.get("zusätzlich_korrekt", [])),
        "zusätzlich_falsch": len(analysis_results.get("zusätzlich_falsch", []))
    }
    
    # Details extrahieren (vereinfacht für jetzt; kann später erweitert werden)
    details = {
        "fehlend": [item.get("path", item) if isinstance(item, dict) else item for item in analysis_results.get("fehlend", [])],
        "zusätzlich_korrekt": [item.get("path", item) if isinstance(item, dict) else item for item in analysis_results.get("zusätzlich_korrekt", [])],
        "zusätzlich_falsch": [item.get("path", item) if isinstance(item, dict) else item for item in analysis_results.get("zusätzlich_falsch", [])]
    }
    
    # Baumstruktur (platzhalter; kann in späteren Phasen erweitert werden)
    tree_structure = {
        "root": str(project_root),
        "structure_type": "unknown",  # Kann später aus Excel bestimmt werden
        "nodes": []  # Platzhalter für hierarchische Darstellung
    }
    
    # JSON-Objekt zusammenstellen
    output_data = {
        "metadata": metadata,
        "summary": summary,
        "details": details,
        "tree_structure": tree_structure
    }
    
    # JSON serialisieren
    json_output = json.dumps(output_data, indent=2, ensure_ascii=False)
    
    # Ereignis loggen
    log_analysis_event("json_export", {"summary": summary}, project_root)
    
    return json_output


def get_all_folders_recursive(project_path: Path, allowed_roots: List[Path]) -> List[str]:
    """
    Sammelt alle Ordner-Pfade rekursiv aus dem Projektverzeichnis.

    Diese Funktion dient als Hilfsfunktion für Skripte, die eine einfache
    Liste aller Ordner benötigen, ohne Dateien.

    Args:
        project_path: Das zu scannende Projektverzeichnis
        allowed_roots: Liste der erlaubten Root-Verzeichnisse für Sicherheit

    Returns:
        Liste der relativen Ordner-Pfade als Strings
    """
    folders = []
    
    def _is_allowed_path(path: Path) -> bool:
        """Prüft, ob der Pfad innerhalb der erlaubten Roots liegt."""
        try:
            path.resolve()
            for root in allowed_roots:
                root.resolve()
                path.relative_to(root)
                return True
        except ValueError:
            return False
        return False
    
    def scan_recursive(current_path: Path):
        if not _is_allowed_path(current_path):
            return
            
        try:
            for item in current_path.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    # Relativer Pfad vom Projektroot
                    rel_path = item.relative_to(project_path)
                    folders.append(str(rel_path))
                    
                    # Rekursiv weiter
                    scan_recursive(item)
        except PermissionError:
            pass  # Überspringe Ordner ohne Zugriff
    
    scan_recursive(project_path)
    return folders


def detect_structure_type(actual_folders: List[str]) -> str:
    """
    Erkennt den Strukturtyp basierend auf den vorhandenen Ordnernamen.

    Basierend auf DOMAIN_RULES.md:
    - Numerische Ordnernamen (1, 2, 3, ...) → 12ER-Struktur
    - Alphanumerische Ordnernamen (A, B01, C02, ...) → KBOB-Struktur

    Args:
        actual_folders: Liste der Ordner-Pfade

    Returns:
        "12er" oder "kbob"
    """
    # Sammle Root-Ordnernamen
    root_folders = set()
    for folder in actual_folders:
        parts = Path(folder).parts
        if len(parts) >= 1:
            root_folders.add(parts[0])
    
    # Prüfe Muster
    has_numeric = any(folder.isdigit() for folder in root_folders)
    has_alpha = any(folder.replace('0', '').replace('1', '').replace('2', '').replace('3', '').replace('4', '').replace('5', '').replace('6', '').replace('7', '').replace('8', '').replace('9', '').isalpha() for folder in root_folders)
    
    if has_numeric and not has_alpha:
        return "12er"
    elif has_alpha:
        return "kbob"
    else:
        # Fallback
        return "12er"


def compare_json_with_folders(soll_json_path_or_structure, actual_folders: List[str]) -> Dict[str, Any]:
    """
    Vergleicht eine SOLL-Struktur aus JSON oder Liste mit den IST-Ordnern.

    Args:
        soll_json_path_or_structure: Pfad zur JSON-Datei oder Liste der SOLL-Struktur
        actual_folders: Liste der IST-Ordner-Pfade

    Returns:
        Dict mit Vergleichsergebnissen
    """
    import json
    
    if isinstance(soll_json_path_or_structure, Path):
        # Lade aus Datei
        try:
            with open(soll_json_path_or_structure, 'r', encoding='utf-8') as f:
                soll_data = json.load(f)
        except Exception as e:
            return {"success": False, "error": f"Fehler beim Laden der SOLL-Struktur: {e}"}
    elif isinstance(soll_json_path_or_structure, list):
        # Direkt Liste
        soll_data = soll_json_path_or_structure
    else:
        return {"success": False, "error": "Ungültiger Typ für soll_json_path_or_structure"}
    
    # Extrahiere SOLL-Ordner (vereinfacht - nimmt an, dass es eine Liste von Dicts mit 'path' ist)
    soll_folders = set()
    for item in soll_data:
        if isinstance(item, dict) and 'path' in item:
            soll_folders.add(item['path'])
    
    ist_folders = set(actual_folders)
    
    missing_folders = soll_folders - ist_folders
    additional_folders = ist_folders - soll_folders
    
    # Kategorisiere zusätzliche Ordner (vereinfacht)
    additional_correct = set()
    additional_wrong = set()
    
    for folder in additional_folders:
        # Vereinfacht: Wenn unter einem SOLL-Pfad, dann korrekt
        is_correct = any(folder.startswith(soll + '/') or folder == soll for soll in soll_folders)
        if is_correct:
            additional_correct.add(folder)
        else:
            additional_wrong.add(folder)
    
    return {
        "success": True,
        "total_soll_folders": len(soll_folders),
        "total_ist_folders": len(ist_folders),
        "missing_folders": list(missing_folders),
        "additional_correct": list(additional_correct),
        "additional_wrong": list(additional_wrong)
    }


def compare_excel_with_scan(excel_path: Path, ist_folders: Set[str]) -> Dict[str, Any]:
    """
    Vergleicht eine Excel-Datei direkt mit den IST-Ordnern.

    Diese Funktion lädt die SOLL-Struktur aus Excel und vergleicht sie
    mit den tatsächlich vorhandenen Ordnern (nur erste Ebene).

    Args:
        excel_path: Pfad zur Excel-Datei
        ist_folders: Set der IST-Ordnernamen (erste Ebene)

    Returns:
        Dict mit Vergleichsergebnissen
    """
    from src.excel_parser import parse_excel
    
    try:
        soll_structure = parse_excel(excel_path)
    except Exception as e:
        return {"success": False, "error": f"Fehler beim Laden der Excel-Datei: {e}"}
    
    # Extrahiere SOLL-Ordnernamen (erste Ebene)
    soll_folders = set()
    for item in soll_structure:
        if isinstance(item, dict) and item.get('type') == 'folder':
            path = item.get('number', '')
            # Nimm nur erste Ebene
            parts = path.split('/')
            if parts:
                soll_folders.add(parts[0])
    
    missing_folders = soll_folders - ist_folders
    additional_folders = ist_folders - soll_folders
    
    return {
        "success": True,
        "total_soll_folders": len(soll_folders),
        "missing_folders": list(missing_folders),
        "additional_wrong": list(additional_folders)  # Vereinfacht als falsch
    }


def _is_leaf(soll_item: Dict[str, Any], soll_structure: List[Dict[str, Any]]) -> bool:
    """
    Prüft, ob ein SOLL-Element ein Blatt ist (keine Kinder hat).

    Args:
        soll_item: Das SOLL-Element
        soll_structure: Liste aller SOLL-Elemente

    Returns:
        True wenn es ein Blatt ist (keine Kinder)
    """
    item_path = _number_to_path(soll_item["number"])
    item_depth = soll_item.get("depth")
    if item_depth is None:
        # Berechne depth falls nicht vorhanden
        from src.excel_parser import calculate_depth
        item_depth = calculate_depth(soll_item["number"])
        if item_depth is None:
            return False  # Ungültige Nummer
    
    # Prüfe ob es Kinder gibt (Elemente mit höherer Tiefe unter diesem Pfad)
    for other_item in soll_structure:
        other_depth = other_item.get("depth")
        if other_depth is None:
            from src.excel_parser import calculate_depth
            other_depth = calculate_depth(other_item["number"])
            if other_depth is None:
                continue
        
        if other_depth > item_depth:
            other_path = _number_to_path(other_item["number"])
            if other_path.startswith(item_path + "/"):
                return False
    
    return True