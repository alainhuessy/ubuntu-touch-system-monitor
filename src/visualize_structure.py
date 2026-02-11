#!/usr/bin/env python3
"""
Visualisierung der Ordnerstruktur aus JSON-Dateien.

Dieses Skript lädt die JSON-Struktur und zeigt sie hierarchisch an.
"""

import json
from pathlib import Path
from typing import List, Dict, Any
import sys

# Pfad zum src-Verzeichnis hinzufügen (falls nötig)
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import logging
from src.logging_config import setup_logging


def load_structure(json_path: Path) -> List[Dict[str, Any]]:
    """Lädt die Struktur aus einer JSON-Datei."""
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def build_tree(entries: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Baut einen Baum aus den Einträgen auf basierend auf depth und number."""
    # Sortiere nach number für konsistente Reihenfolge
    entries.sort(key=lambda x: x['number'])

    tree = {}
    node_map = {}  # Map von number zu Knoten im Baum
    stack = []  # Stack für Parents: (number, depth)

    for entry in entries:
        number = entry['number']
        depth = entry['depth']
        node_map[number] = {'_data': entry}

        # Finde Parent: der letzte mit depth - 1
        while stack and stack[-1][1] >= depth:
            stack.pop()

        if stack:
            parent_number = stack[-1][0]
            if 'children' not in node_map[parent_number]:
                node_map[parent_number]['children'] = {}
            node_map[parent_number]['children'][number] = node_map[number]
        else:
            # Root level
            tree[number] = node_map[number]

        stack.append((number, depth))

    return tree


def print_tree(tree: Dict[str, Any], prefix: str = "", is_last: bool = True):
    """Druckt den Baum hierarchisch."""
    items = list(tree.items())
    for i, (key, value) in enumerate(items):
        is_last_item = i == len(items) - 1
        connector = "└── " if is_last_item else "├── "
        next_prefix = prefix + ("    " if is_last_item else "│   ")

        data = value.get('_data', {})
        name = data.get('name', key)
        typ = data.get('type', 'unknown')
        required = data.get('required', False)
        required_str = " (erforderlich)" if required else ""

        print(f"{prefix}{connector}{key}: {name} [{typ}]{required_str}")

        # Rekursiv für Kinder
        children = value.get('children', {})
        if children:
            print_tree(children, next_prefix, is_last_item)


def tree_to_nested_dict(tree: Dict[str, Any]) -> Dict[str, Any]:
    """Konvertiert den internen Baum in ein verschachteltes Dict für JSON-Export."""
    result = {}
    for key, value in tree.items():
        if key == '_data':
            # Füge Daten zum aktuellen Knoten hinzu
            data = value
            result.update({
                'number': data.get('number'),
                'name': data.get('name'),
                'type': data.get('type'),
                'required': data.get('required'),
                'depth': data.get('depth')
            })
        else:
            # Rekursiv für Unterelemente
            subtree = {k: v for k, v in value.items()}
            child_dict = tree_to_nested_dict(subtree)
            # Füge das Kind unter dem Schlüssel hinzu
            result[key] = child_dict
    return result


def save_tree_as_json(tree: Dict[str, Any], output_path: Path):
    """Speichert den Baum als verschachtelte JSON-Datei."""
    nested = tree_to_nested_dict(tree)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(nested, f, ensure_ascii=False, indent=2)


def main():
    """Hauptfunktion für die Visualisierung."""
    # Logging einrichten
    log_file = Path(__file__).parent.parent / "scripts_log.txt"
    setup_logging(log_file)
    logging.info("Starte Visualisierung der Ordnerstruktur")

    base_path = Path(__file__).parent.parent / 'tests' / 'data'

    # KBOB-Struktur
    kbob_path = base_path / 'structure_kbob.json'
    kbob_nested_path = base_path / 'structure_kbob_nested.json'
    if kbob_path.exists():
        print("=== KBOB-Struktur ===")
        kbob_entries = load_structure(kbob_path)
        kbob_tree = build_tree(kbob_entries)
        print_tree(kbob_tree)
        
        # Speichere verschachtelte JSON
        save_tree_as_json(kbob_tree, kbob_nested_path)
        print(f"\nVerschachtelte JSON gespeichert: {kbob_nested_path}")
        print()

    # 12er-Struktur (falls vorhanden)
    er12_path = base_path / 'structure_12er.json'
    if er12_path.exists():
        print("=== 12er-Struktur ===")
        er12_entries = load_structure(er12_path)
        er12_tree = build_tree(er12_entries)
        print_tree(er12_tree)
        print()


if __name__ == "__main__":
    main()