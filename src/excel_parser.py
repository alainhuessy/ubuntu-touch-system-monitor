"""Excel-Parser für Strukturdefinitionen."""

import json
from pathlib import Path
from typing import List, Dict, Any

import openpyxl


def calculate_depth(number_str: str) -> int | None:
    """
    Berechnet die Tiefe aus der Nummernstring.
    Für 12er: Basierend auf hierarchischer Struktur (z.B. "8" -> 1, "8.01" -> 2, "8.011" -> 3).
    Für KBOB: Basierend auf Länge (z.B. "O" -> 1, "O01" -> 2, "O01001" -> 3).
    Gibt None zurück, wenn keine gültige Nummer.
    
    Args:
        number_str: Die Nummer als String.
        
    Returns:
        Die berechnete Tiefe oder None.
    """
    if not number_str:
        return None
    # Prüfe, ob es eine gültige Nummer ist (Buchstaben/Zahlen und Punkte)
    import re
    if not re.match(r'^[A-Z0-9]+(\.\d+)*$', number_str):
        return None
    
    if '.' in number_str:
        # 12er-Format mit Punkten
        parts = number_str.split('.')
        depth = len(parts)  # Basis-Tiefe
        
        # Wenn die letzte Zahl mehr als 2 Ziffern hat, ist es eine tiefere Ebene
        last_part = parts[-1]
        if len(last_part) > 2:
            additional_depth = ((len(last_part) - 2) // 2) + 1
            depth += additional_depth
        
        return depth
    else:
        # KBOB-Format ohne Punkte: depth = len // 3 + 1
        return len(number_str) // 3 + 1


def parse_excel(excel_file: Path) -> List[Dict[str, Any]]:
    """
    Parst eine Excel-Datei und extrahiert die Strukturdefinition.

    Args:
        excel_file: Pfad zur Excel-Datei.

    Returns:
        Liste von Dictionaries mit Strukturinformationen.
        Jedes Dict enthält: 'number' (str), 'depth' (int), 'name' (str), 'type' (str: 'folder' oder 'document'), 'required' (bool).
    """
    wb = openpyxl.load_workbook(excel_file, data_only=True)
    ws = wb.active
    
    structure = []
    
    for row in ws.iter_rows(min_row=2, values_only=True):  # Überspringe Header
        if not row[0]:  # Leere Zeile
            continue
        
        try:
            number_str = str(row[0]).strip() if row[0] else None
            name = str(row[1]).strip() if len(row) > 1 and row[1] else None
            typ_code = str(row[2]).strip().upper() if len(row) > 2 and row[2] else None
            
            if not number_str or not name:
                continue  # Ungültige Zeile überspringen
            
            depth = calculate_depth(number_str)
            
            if depth is None or not name:
                continue  # Ungültige Zeile überspringen
            
            # Typ bestimmen (flexibel für 12er und KBOB)
            if typ_code == 'V':
                typ = 'folder'
                required = True
            elif len(number_str) <= 3:  # Kurze Nummern sind folder (für KBOB)
                typ = 'folder'
                required = True
            else:  # Längere Nummern sind documents
                typ = 'document'
                required = typ_code == 'X' or typ_code == 'x'  # 'X' oder 'x' für required
            
            structure.append({
                'number': number_str,
                'depth': depth,
                'name': name,
                'type': typ,
                'required': required
            })
        except (ValueError, TypeError, IndexError):
            continue  # Ungültige Zeile überspringen
    
    return structure


def save_structure_as_json(structure: List[Dict[str, Any]], output_file: Path) -> None:
    """
    Speichert die geparste Struktur als JSON-Datei für Debugging und Nachvollziehbarkeit.

    Args:
        structure: Geparste Strukturdefinition.
        output_file: Pfad zur JSON-Ausgabedatei.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(structure, f, ensure_ascii=False, indent=2)


def parse_and_save_excel(excel_file: Path, json_output_file: Path | None = None) -> List[Dict[str, Any]]:
    """
    Parst eine Excel-Datei und speichert die Struktur optional als JSON.

    Args:
        excel_file: Pfad zur Excel-Datei.
        json_output_file: Optional: Pfad zur JSON-Ausgabedatei. 
                         Falls None, wird neben der Excel-Datei gespeichert.

    Returns:
        Geparste Strukturdefinition.
    """
    structure = parse_excel(excel_file)
    
    if json_output_file is None:
        json_output_file = excel_file.with_suffix('.json')
    
    save_structure_as_json(structure, json_output_file)
    
    return structure


def visualize_structure(structure: List[Dict[str, Any]]) -> str:
    """
    Visualisiert die Struktur mit Nummern und Einrückungen für bessere Lesbarkeit.

    Args:
        structure: Geparste Strukturdefinition.

    Returns:
        String mit der visualisierten Struktur.
    """
    lines = []
    for item in structure:
        indent = "  " * (item['depth'] - 1)  # Einrückung basierend auf depth
        symbol = "📁" if item['type'] == 'folder' else "📄"
        required_mark = " *" if item['required'] else ""
        line = f"{indent}{item['number']} - {item['name']}{required_mark}"
        lines.append(line)
    return "\n".join(lines)